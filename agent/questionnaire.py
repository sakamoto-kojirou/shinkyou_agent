"""State machine for the DX diagnostic interview."""

from __future__ import annotations

from dataclasses import dataclass, field
from numbers import Real

from agent.meti_framework import DIMENSIONS, QUESTIONS, Dimension, Question


@dataclass
class QuestionnaireState:
	"""Capture the current interview state and collected answers."""

	language: str
	company_profile: dict
	current_dimension_idx: int = 0
	current_question_idx: int = 0
	responses: dict = field(default_factory=dict)
	is_complete: bool = False


class QuestionnaireEngine:
	"""Drive the questionnaire flow across dimensions and questions."""

	def __init__(self, language: str, company_profile: dict):
		"""Initialize the engine with language and company context."""

		self.state = QuestionnaireState(
			language=language,
			company_profile=dict(company_profile),
		)
		self._initialize_response_store()

	def _initialize_response_store(self) -> None:
		"""Create an empty response bucket for each framework dimension."""

		self.state.responses = {
			dimension.id: {"likert_scores": [], "text_responses": []}
			for dimension in DIMENSIONS
		}

	def _get_dimension_index_for_question(self, question_idx: int) -> int:
		"""Return the index of the dimension that owns a question."""

		question = QUESTIONS[question_idx]
		for index, dimension in enumerate(DIMENSIONS):
			if dimension.id == question.dimension_id:
				return index
		raise LookupError(f"No dimension found for question id {question.id}")

	def _total_questions(self) -> int:
		"""Return the total number of questionnaire items."""

		return len(QUESTIONS)

	def _update_completion_state(self) -> None:
		"""Mark the questionnaire complete when all questions have been answered."""

		if self.state.current_question_idx >= self._total_questions():
			self.state.is_complete = True
			self.state.current_dimension_idx = len(DIMENSIONS)
			self.state.current_question_idx = self._total_questions()

	def get_current_question(self) -> Question | None:
		"""Return the current question or None when the interview is complete."""

		if self.state.is_complete:
			return None
		if self.state.current_question_idx >= self._total_questions():
			return None
		return QUESTIONS[self.state.current_question_idx]

	def get_current_dimension(self) -> Dimension | None:
		"""Return the current dimension or None when the interview is complete."""

		if self.state.is_complete:
			return None
		if self.state.current_dimension_idx >= len(DIMENSIONS):
			return None
		return DIMENSIONS[self.state.current_dimension_idx]

	def submit_answer(self, likert_score: int, text_response: str) -> None:
		"""Store the answer for the current question and advance the interview."""

		if self.state.is_complete:
			return

		current_question = self.get_current_question()
		if current_question is None:
			self._update_completion_state()
			return

		minimum_score, maximum_score = current_question.likert_scale
		if not isinstance(likert_score, Real):
			raise TypeError("likert_score must be numeric")
		if not float(likert_score).is_integer():
			raise ValueError("likert_score must be an integer value")
		likert_score = int(likert_score)
		if likert_score < minimum_score or likert_score > maximum_score:
			raise ValueError(
				f"likert_score must be between {minimum_score} and {maximum_score}"
			)

		bucket = self.state.responses[current_question.dimension_id]
		bucket["likert_scores"].append(likert_score)
		bucket["text_responses"].append(text_response)

		self.state.current_question_idx += 1
		if self.state.current_question_idx < self._total_questions():
			self.state.current_dimension_idx = self._get_dimension_index_for_question(
				self.state.current_question_idx
			)
		self._update_completion_state()

	def is_dimension_complete(self) -> bool:
		"""Return True if the last submitted answer finished a dimension."""

		if self.state.is_complete:
			return True
		current_q_idx = self.state.current_question_idx
		if current_q_idx == 0:
			return False
		previous_question = QUESTIONS[current_q_idx - 1]
		current_question = self.get_current_question()
		if current_question is None:
			return True
		return previous_question.dimension_id != current_question.dimension_id

	def get_progress(self) -> dict:
		"""Return a compact progress summary for the interview."""

		total_questions = self._total_questions()
		current_question = min(self.state.current_question_idx, total_questions)
		percent = 100.0 if total_questions == 0 else (current_question / total_questions) * 100.0
		return {
			"current_dim": len(DIMENSIONS) if self.state.is_complete else self.state.current_dimension_idx + 1,
			"total_dims": len(DIMENSIONS),
			"current_q": current_question,
			"total_q": total_questions,
			"percent": percent,
		}

	def get_all_responses(self) -> dict:
		"""Return the full response map collected so far."""

		return self.state.responses

	def reset(self) -> None:
		"""Reset the questionnaire to its initial state."""

		self.state.current_dimension_idx = 0
		self.state.current_question_idx = 0
		self.state.is_complete = False
		self._initialize_response_store()


def run_demo_techbridge() -> QuestionnaireEngine:
	"""Run the questionnaire with demo responses for TechBridge Ltda."""

	demo_profile = {
		"company_name": "TechBridge Ltda.",
		"sector": "Logistics services",
		"employees": 45,
		"country": "Brazil",
		"dx_stage": "Early digitalization",
	}
	engine = QuestionnaireEngine(language="en", company_profile=demo_profile)

	demo_answers = [
		(1, "The company has started discussing DX but has not formalized a company-wide vision yet."),
		(1, "Leadership communicates digital improvements informally, mostly tied to immediate operational needs."),
		(1, "Progress is monitored through basic operational goals, but there is no mature DX scorecard."),
		(2, "Scheduling and route planning have been partially digitized using a basic TMS tool."),
		(2, "Operational decisions use weekly reports, but real-time data visibility is still limited."),
		(1, "The operation uses a mixed model, with paper records still common alongside digital tools."),
		(2, "A spreadsheet-based tracking system is in use; no AI or predictive tools are deployed yet."),
		(1, "Digital training is occasional and focused on basic tool adoption rather than structured capability building."),
		(1, "Coordination happens when needed, but DX work is not yet managed through a cross-functional routine."),
		(1, "DX responsibilities are informal and not assigned through a dedicated governance structure."),
		(2, "Customer and operational systems are partially connected, but data is still fragmented across tools."),
		(2, "Data quality is acceptable for day-to-day work, although consistency and accessibility remain uneven."),
		(1, "Infrastructure is mostly on-premise with limited cloud usage and modest scalability."),
		(1, "DX decisions are reviewed by management, but formal policies and approval processes are still emerging."),
		(0, "Cybersecurity and privacy are recognized concerns, yet controls and documentation are still developing."),
		(1, "Vendor and technology risks are monitored informally, with limited contingency planning."),
	]

	for score, text in demo_answers:
		engine.submit_answer(score, text)

	return engine
