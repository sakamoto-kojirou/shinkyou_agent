"""Scoring engine for the DX diagnostic interview."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

from agent.llm_analyzer import FullAnalysis
from agent.meti_framework import DIMENSIONS, MATURITY_LEVELS


class DimensionScore(TypedDict):
	"""Structured score for one assessment dimension."""

	dimension_id: int
	likert_average: float
	qualitative_score: float
	composite_score: float
	weight: float
	weighted_contribution: float


class ScoringResult(TypedDict):
	"""Complete scoring outcome for the diagnostic report."""

	dimension_scores: list[DimensionScore]
	overall_score: float
	maturity_level: int
	maturity_label_en: str
	maturity_label_pt: str
	maturity_label_ja: str
	benchmark_gaps: dict[int, float]


def _load_benchmark_averages() -> dict[int, float]:
	"""Load the METI SME benchmark averages from the local JSON file."""

	benchmark_path = Path(__file__).resolve().parent.parent / "data" / "meti_benchmarks.json"
	if not benchmark_path.exists():
		return {}

	try:
		payload = json.loads(benchmark_path.read_text(encoding="utf-8"))
	except json.JSONDecodeError:
		return {}

	dimension_averages = payload.get("dimension_averages", {})
	if not isinstance(dimension_averages, dict):
		return {}

	benchmark_averages: dict[int, float] = {}
	for key, value in dimension_averages.items():
		try:
			dimension_id = int(key)
			benchmark_averages[dimension_id] = float(value)
		except (TypeError, ValueError):
			continue
	return benchmark_averages


BENCHMARK_AVERAGES: dict[int, float] = _load_benchmark_averages()


class ScoringEngine:
	"""Combine Likert responses and LLM scores into final DX maturity scores."""

	def calculate_likert_average(self, scores: list[int]) -> float:
		"""Return the arithmetic mean of the provided Likert scores."""

		if not scores:
			return 0.0
		return sum(scores) / len(scores)

	def calculate_composite_score(self, likert_avg: float, qualitative_score: float) -> float:
		"""Blend quantitative and qualitative scores using the project formula."""

		return (0.6 * likert_avg) + (0.4 * qualitative_score)

	def calculate_dimension_scores(self, responses: dict, llm_analysis: FullAnalysis) -> list[DimensionScore]:
		"""Build a per-dimension scoring table from survey responses and LLM output."""

		dimension_scores: list[DimensionScore] = []
		analysis_by_dimension = {
			analysis["dimension_id"]: analysis for analysis in llm_analysis["dimensions"]
		}

		for dimension in DIMENSIONS:
			bucket = responses.get(dimension.id, responses.get(str(dimension.id), {}))
			if isinstance(bucket, dict):
				likert_scores = bucket.get("likert_scores", [])
			else:
				likert_scores = []

			if not isinstance(likert_scores, list):
				likert_scores = []

			numeric_scores = [int(score) for score in likert_scores if isinstance(score, (int, float))]
			likert_average = self.calculate_likert_average(numeric_scores)

			qualitative_score = 0.0
			analysis = analysis_by_dimension.get(dimension.id)
			if analysis is not None:
				qualitative_score = float(analysis["qualitative_score"])

			composite_score = self.calculate_composite_score(likert_average, qualitative_score)
			weighted_contribution = composite_score * dimension.weight

			dimension_scores.append(
				{
					"dimension_id": dimension.id,
					"likert_average": likert_average,
					"qualitative_score": qualitative_score,
					"composite_score": composite_score,
					"weight": dimension.weight,
					"weighted_contribution": weighted_contribution,
				}
			)

		return dimension_scores

	def calculate_overall_score(self, dimension_scores: list[DimensionScore]) -> float:
		"""Compute the weighted overall score across all dimensions."""

		if not dimension_scores:
			return 0.0

		total_weight = 0.0
		weighted_sum = 0.0

		for item in dimension_scores:
			weight = float(item["weight"])
			total_weight += weight
			weighted_sum += float(item["weighted_contribution"])

		if total_weight == 0.0:
			return 0.0
		return weighted_sum / total_weight

	def map_to_maturity_level(self, score: float) -> int:
		"""Map a score to the METI maturity level thresholds."""

		if score < 1.0:
			return 0
		if score < 2.0:
			return 1
		if score < 3.0:
			return 2
		if score < 3.5:
			return 3
		return 4

	def compare_with_benchmark(self, dimension_scores: list[DimensionScore]) -> dict[int, float]:
		"""Compare dimension scores against METI SME benchmark averages."""

		benchmark_gaps: dict[int, float] = {}
		for item in dimension_scores:
			dimension_id = item["dimension_id"]
			benchmark_average = BENCHMARK_AVERAGES.get(dimension_id)
			if benchmark_average is None:
				benchmark_gaps[dimension_id] = 0.0
				continue
			benchmark_gaps[dimension_id] = benchmark_average - float(item["composite_score"])
		return benchmark_gaps

	def build_scoring_result(self, responses: dict, llm_analysis: FullAnalysis) -> ScoringResult:
		"""Orchestrate the full scoring workflow and return the result payload."""

		dimension_scores = self.calculate_dimension_scores(responses, llm_analysis)
		overall_score = self.calculate_overall_score(dimension_scores)
		maturity_level = self.map_to_maturity_level(overall_score)
		maturity_level_obj = next(
			(level for level in MATURITY_LEVELS if level.level == maturity_level),
			MATURITY_LEVELS[0],
		)

		return {
			"dimension_scores": dimension_scores,
			"overall_score": overall_score,
			"maturity_level": maturity_level,
			"maturity_label_en": maturity_level_obj.label_en,
			"maturity_label_pt": maturity_level_obj.label_pt,
			"maturity_label_ja": maturity_level_obj.label_ja,
			"benchmark_gaps": self.compare_with_benchmark(dimension_scores),
		}
