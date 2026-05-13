"""Groq-backed qualitative analysis for the DX diagnostic interview."""

from __future__ import annotations

import json
import os
import re
from typing import Any, TypedDict

import httpx
from dotenv import load_dotenv
from groq import Groq

from agent.meti_framework import DIMENSIONS, Dimension, get_text


class DimensionAnalysis(TypedDict):
	"""Structured qualitative analysis for one dimension."""

	dimension_id: int
	qualitative_score: float
	justification: str
	gaps: list[str]
	recommendations: list[str]


class FullAnalysis(TypedDict):
	"""Complete analysis payload for the DX diagnostic report."""

	dimensions: list[DimensionAnalysis]
	overall_level: int
	overall_score: float
	executive_summary: str


class LLMAnalyzer:
	"""Use Groq to generate qualitative DX maturity analysis from interview data."""

	MODEL_NAME = "llama-3.1-70b-versatile"
	MAX_RETRIES = 2

	def __init__(self, language: str):
		"""Initialize the analyzer with the target output language."""

		load_dotenv()
		self.language = self._normalize_language(language)
		api_key = os.getenv("GROQ_API_KEY", "").strip()
		# Pass an explicit httpx.Client to avoid the 'proxies' keyword error
		# that occurs when HTTP_PROXY/HTTPS_PROXY env vars are set on the system.
		if api_key:
			self.client = Groq(api_key=api_key, http_client=httpx.Client())
		else:
			self.client = None

	def _normalize_language(self, language: str) -> str:
		"""Normalize the configured language code."""

		normalized = language.strip().lower()
		if normalized not in {"en", "pt", "ja"}:
			return "en"
		return normalized

	def _language_instruction(self) -> str:
		"""Return a language-specific instruction for model output."""

		if self.language == "pt":
			return "Responda em português do Brasil."
		if self.language == "ja":
			return "日本語で回答してください。"
		return "Respond in English."

	def _localize_label(self, dimension: Dimension) -> str:
		"""Return the dimension label in the configured language."""

		return get_text(dimension, self.language)

	def _serialize_profile(self, company_profile: dict) -> str:
		"""Serialize company context for prompt injection."""

		return json.dumps(company_profile, ensure_ascii=False, indent=2, sort_keys=True)

	def _serialize_responses(self, text_responses: list[str]) -> str:
		"""Serialize free-text interview responses for prompt injection."""

		payload = {"responses": text_responses}
		return json.dumps(payload, ensure_ascii=False, indent=2)

	def _build_system_prompt(self) -> str:
		"""Build the global instruction prompt for the model."""

		return (
			"You are an academic researcher specializing in Digital Transformation "
			"assessment for SMEs, using the METI DX Promotion Index (Japan, 2019). "
			"Respond ONLY in valid JSON. Do not use markdown, code fences, commentary, "
			"or any preamble. Return exactly the schema requested by the user prompt."
		)

	def _build_dimension_prompt(
		self,
		dimension: Dimension,
		text_responses: list[str],
		company_profile: dict,
	) -> str:
		"""Build a dimension-level prompt for qualitative scoring."""

		dimension_name = self._localize_label(dimension)
		profile_text = self._serialize_profile(company_profile)
		responses_text = self._serialize_responses(text_responses)
		language_rule = self._language_instruction()
		schema_hint = (
			'{"dimension_id": 1, "qualitative_score": 0.0, "justification": "", '
			'"gaps": [], "recommendations": []}'
		)

		return (
			f"Assess the following DX dimension for an SME interview. {language_rule} "
			f"Write justification, gaps, and recommendations in the same language.\n\n"
			f"Dimension ID: {dimension.id}\n"
			f"Dimension Name: {dimension_name}\n"
			f"Dimension Weight: {dimension.weight}\n\n"
			f"Company Context:\n{profile_text}\n\n"
			f"Interview Responses:\n{responses_text}\n\n"
			"Score the dimension from 0.0 to 4.0 using the METI DX Promotion Index scale. "
			"Return JSON that matches this schema exactly:\n"
			f"{schema_hint}"
		)

	def _build_summary_prompt(
		self,
		dimension_analyses: list[DimensionAnalysis],
		company_profile: dict,
		quantitative_scores: dict,
		overall_score: float,
		overall_level: int,
	) -> str:
		"""Build the final executive summary prompt."""

		profile_text = self._serialize_profile(company_profile)
		analyses_text = json.dumps(dimension_analyses, ensure_ascii=False, indent=2)
		scores_text = json.dumps(quantitative_scores, ensure_ascii=False, indent=2, sort_keys=True)
		language_rule = self._language_instruction()

		return (
			f"Create a concise executive summary for an SME DX diagnostic report. {language_rule} "
			"The summary must be written in the same language as the interview language.\n\n"
			f"Company Context:\n{profile_text}\n\n"
			f"Dimension Analyses:\n{analyses_text}\n\n"
			f"Quantitative Scores:\n{scores_text}\n\n"
			f"Overall Score: {overall_score:.2f}\n"
			f"Overall Level: {overall_level}\n\n"
			'Return JSON exactly as: {"executive_summary": "..."}'
		)

	def _extract_json_object(self, raw_text: str) -> dict[str, Any]:
		"""Extract and parse a JSON object from model output."""

		candidate = raw_text.strip()
		if candidate.startswith("```"):
			candidate = re.sub(r"^```(?:json)?\s*", "", candidate)
			candidate = re.sub(r"\s*```$", "", candidate)

		try:
			parsed = json.loads(candidate)
			if isinstance(parsed, dict):
				return parsed
		except json.JSONDecodeError:
			pass

		match = re.search(r"\{.*\}", candidate, re.DOTALL)
		if match:
			parsed = json.loads(match.group(0))
			if isinstance(parsed, dict):
				return parsed

		raise ValueError("Model output did not contain valid JSON object.")

	def _coerce_float_score(self, value: Any) -> float:
		"""Coerce a numeric score into the METI 0.0-4.0 range."""

		try:
			score = float(value)
		except (TypeError, ValueError) as exc:
			raise ValueError("Score must be numeric.") from exc
		return max(0.0, min(4.0, score))

	def _fallback_dimension_analysis(
		self,
		dimension: Dimension,
		text_responses: list[str],
		company_profile: dict,
	) -> DimensionAnalysis:
		"""Build a deterministic fallback analysis when the API cannot be used."""

		response_count = len([response for response in text_responses if response.strip()])
		if response_count == 0:
			score = 0.5
		elif response_count <= 2:
			score = 1.0
		elif response_count <= 4:
			score = 1.5
		else:
			score = 2.0

		localized_dimension_name = self._localize_label(dimension)
		language_text = {
			"en": (
				f"The available responses indicate an early-stage view of {localized_dimension_name.lower()}. "
				"Evidence remains limited and qualitative detail is still shallow."
			),
			"pt": (
				f"As respostas disponíveis indicam uma visão inicial de {localized_dimension_name.lower()}. "
				"A evidência ainda é limitada e o detalhamento qualitativo permanece superficial."
			),
			"ja": (
				f"回答内容からは、{localized_dimension_name} に関して初期段階の状況が示されています。 "
				"証拠は限定的で、定性的な記述もまだ浅い状態です。"
			),
		}
		gap_text = {
			"en": "Process visibility is incomplete and measurement practices are not yet standardized.",
			"pt": "A visibilidade dos processos é incompleta e as práticas de medição ainda não estão padronizadas.",
			"ja": "業務の可視化が不十分で、測定の仕組みもまだ標準化されていません。",
		}
		recommendation_text = {
			"en": "Define one practical improvement initiative, assign an owner, and track results monthly.",
			"pt": "Defina uma iniciativa prática de melhoria, atribua um responsável e acompanhe os resultados mensalmente.",
			"ja": "具体的な改善施策を1つ定め、責任者を置き、月次で成果を確認してください。",
		}

		return {
			"dimension_id": dimension.id,
			"qualitative_score": score,
			"justification": language_text[self.language],
			"gaps": [gap_text[self.language]],
			"recommendations": [recommendation_text[self.language]],
		}

	def _fallback_summary(
		self,
		overall_score: float,
		overall_level: int,
		company_profile: dict,
	) -> str:
		"""Build a language-specific executive summary fallback."""

		company_name = company_profile.get("company_name", "the company")
		text_map = {
			"en": (
				f"{company_name} is showing an early-to-developing DX profile, with the strongest need "
				f"for structured process improvement, data-driven decision-making, and clearer governance. "
				f"The overall score of {overall_score:.2f} corresponds to maturity level {overall_level}, "
				"indicating that the next stage should focus on practical standardization and measurable gains."
			),
			"pt": (
				f"{company_name} apresenta um perfil de DX entre inicial e em desenvolvimento, com maior necessidade "
				f"de melhoria estruturada de processos, tomada de decisão baseada em dados e governança mais clara. "
				f"A pontuação geral de {overall_score:.2f} corresponde ao nível de maturidade {overall_level}, "
				"indicando que a próxima etapa deve priorizar padronização prática e ganhos mensuráveis."
			),
			"ja": (
				f"{company_name} は、DXの取り組みが初期から発展途上にある段階であり、特に業務プロセスの標準化、データに基づく意思決定、ガバナンスの明確化が重要です。"
				f" 総合スコア {overall_score:.2f} は成熟度レベル {overall_level} に相当し、次の段階では実務に即した標準化と定量的な改善成果の創出が求められます。"
			),
		}
		return text_map[self.language]

	def _call_groq_json(self, prompt: str) -> dict[str, Any] | None:
		"""Call Groq and return the parsed JSON payload, or None on failure."""

		if self.client is None:
			return None

		last_error: Exception | None = None
		for _attempt in range(self.MAX_RETRIES + 1):
			try:
				response = self.client.chat.completions.create(
					model=self.MODEL_NAME,
					messages=[
						{"role": "system", "content": self._build_system_prompt()},
						{"role": "user", "content": prompt},
					],
					temperature=0.2,
					max_tokens=1000,
				)
				content = response.choices[0].message.content or ""
				return self._extract_json_object(content)
			except Exception as exc:  # pragma: no cover - defensive integration path
				last_error = exc

		if last_error is not None:
			return None
		return None

	def analyze_dimension(
		self,
		dimension: Dimension,
		text_responses: list[str],
		company_profile: dict,
	) -> DimensionAnalysis:
		"""Analyze one dimension with Groq and return a structured result."""

		prompt = self._build_dimension_prompt(dimension, text_responses, company_profile)
		raw_payload = self._call_groq_json(prompt)

		if raw_payload is None:
			return self._fallback_dimension_analysis(dimension, text_responses, company_profile)

		try:
			dimension_id = int(raw_payload.get("dimension_id", dimension.id))
			qualitative_score = self._coerce_float_score(raw_payload.get("qualitative_score", 0.0))
			justification = str(raw_payload.get("justification", "")).strip()
			gaps = raw_payload.get("gaps", [])
			recommendations = raw_payload.get("recommendations", [])

			if not justification:
				raise ValueError("Missing justification.")
			if not isinstance(gaps, list) or not all(isinstance(item, str) for item in gaps):
				raise ValueError("gaps must be a list of strings.")
			if not isinstance(recommendations, list) or not all(
				isinstance(item, str) for item in recommendations
			):
				raise ValueError("recommendations must be a list of strings.")

			return {
				"dimension_id": dimension_id,
				"qualitative_score": qualitative_score,
				"justification": justification,
				"gaps": gaps,
				"recommendations": recommendations,
			}
		except Exception:
			return self._fallback_dimension_analysis(dimension, text_responses, company_profile)

	def _coerce_quantitative_scores(self, quantitative_scores: dict, dimension_id: int) -> float | None:
		"""Extract a usable quantitative score for one dimension when available."""

		value = quantitative_scores.get(dimension_id)
		if value is None:
			value = quantitative_scores.get(str(dimension_id))
		if value is None:
			return None
		if isinstance(value, (int, float)):
			return self._coerce_float_score(value)
		if isinstance(value, list) and value:
			numeric_values = [self._coerce_float_score(item) for item in value if item is not None]
			if numeric_values:
				return sum(numeric_values) / len(numeric_values)
		if isinstance(value, dict):
			for key in ("score", "average", "mean", "value"):
				if key in value:
					return self._coerce_float_score(value[key])
		return None

	def _calculate_overall_score(
		self,
		dimension_analyses: list[DimensionAnalysis],
		quantitative_scores: dict,
	) -> float:
		"""Calculate a weighted overall DX score."""

		weighted_total = 0.0
		total_weight = 0.0

		for dimension in DIMENSIONS:
			analysis = next(
				(item for item in dimension_analyses if item["dimension_id"] == dimension.id),
				None,
			)
			if analysis is None:
				continue

			qualitative_score = self._coerce_float_score(analysis["qualitative_score"])
			quantitative_score = self._coerce_quantitative_scores(quantitative_scores, dimension.id)
			if quantitative_score is None:
				combined_score = qualitative_score
			else:
					combined_score = (0.6 * quantitative_score) + (0.4 * qualitative_score)

			weighted_total += combined_score * dimension.weight
			total_weight += dimension.weight

		if total_weight == 0:
			return 0.0
		return max(0.0, min(4.0, weighted_total / total_weight))

	def _calculate_overall_level(self, overall_score: float) -> int:
		"""Convert the overall score to the METI maturity level scale."""

		return max(0, min(4, int(round(overall_score))))

	def analyze_all(
		self,
		responses: dict,
		company_profile: dict,
		quantitative_scores: dict,
	) -> FullAnalysis:
		"""Analyze all dimensions and return the final report payload."""

		dimension_analyses: list[DimensionAnalysis] = []
		for dimension in DIMENSIONS:
			bucket = responses.get(dimension.id, responses.get(str(dimension.id), {}))
			text_responses = bucket.get("text_responses", []) if isinstance(bucket, dict) else []
			analysis = self.analyze_dimension(dimension, text_responses, company_profile)
			dimension_analyses.append(analysis)

		overall_score = self._calculate_overall_score(dimension_analyses, quantitative_scores)
		overall_level = self._calculate_overall_level(overall_score)

		summary_prompt = self._build_summary_prompt(
			dimension_analyses=dimension_analyses,
			company_profile=company_profile,
			quantitative_scores=quantitative_scores,
			overall_score=overall_score,
			overall_level=overall_level,
		)
		summary_payload = self._call_groq_json(summary_prompt)

		executive_summary = self._fallback_summary(overall_score, overall_level, company_profile)
		if summary_payload is not None:
			candidate_summary = summary_payload.get("executive_summary")
			if isinstance(candidate_summary, str) and candidate_summary.strip():
				executive_summary = candidate_summary.strip()

		return {
			"dimensions": dimension_analyses,
			"overall_level": overall_level,
			"overall_score": overall_score,
			"executive_summary": executive_summary,
		}