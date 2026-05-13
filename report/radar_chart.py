"""Radar chart generation for the DX maturity assessment."""

from __future__ import annotations

import importlib
from io import BytesIO
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

try:
	importlib.import_module("japanize_matplotlib")
except ImportError:  # pragma: no cover - optional font support
	pass

from agent.meti_framework import DIMENSIONS, get_text
from agent.scoring_engine import ScoringResult


def get_dimension_labels(language: str) -> list[str]:
	"""Return the five METI dimension labels in the requested language."""

	return [get_text(dimension, language) for dimension in DIMENSIONS]


def _get_chart_strings(language: str, company_name: str) -> dict[str, str]:
	"""Return localized labels for the chart."""

	chart_strings = {
		"en": {
			"title": "DX Maturity Assessment",
			"company": "Your Company",
			"benchmark": "SME Average (METI 2022)",
		},
		"pt": {
			"title": "Avaliação de Maturidade DX",
			"company": "Sua Empresa",
			"benchmark": "Média de PMEs (METI 2022)",
		},
		"ja": {
			"title": "DX成熟度アセスメント",
			"company": "貴社",
			"benchmark": "中小企業平均（METI 2022）",
		},
	}
	strings = chart_strings.get(language, chart_strings["en"])
	return {
		"title": strings["title"],
		"company": company_name.strip() or strings["company"],
		"benchmark": strings["benchmark"],
	}


def _get_dimension_score_map(scoring_result: ScoringResult) -> dict[int, float]:
	"""Map dimension identifiers to composite scores."""

	scores: dict[int, float] = {}
	for item in scoring_result.get("dimension_scores", []):
		dimension_id = int(item["dimension_id"])
		scores[dimension_id] = float(item["composite_score"])
	return scores


def generate_radar_chart(scoring_result: ScoringResult, language: str, company_name: str = "Your Company") -> bytes:
	"""Generate a radar chart as PNG bytes for the assessment report."""

	labels = get_dimension_labels(language)
	chart_strings = _get_chart_strings(language, company_name)
	dimension_scores = _get_dimension_score_map(scoring_result)
	benchmark_gaps = scoring_result.get("benchmark_gaps", {})

	company_values = [dimension_scores.get(dimension.id, 0.0) for dimension in DIMENSIONS]
	benchmark_values = [
		company_values[index] + float(benchmark_gaps.get(dimension.id, 0.0))
		for index, dimension in enumerate(DIMENSIONS)
	]

	angles = np.linspace(0, 2 * np.pi, len(DIMENSIONS), endpoint=False).tolist()
	angles += angles[:1]
	company_plot_values = company_values + company_values[:1]
	benchmark_plot_values = benchmark_values + benchmark_values[:1]

	fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True}, dpi=150)
	fig.patch.set_facecolor("white")
	ax.set_facecolor("white")

	ax.set_theta_offset(np.pi / 2)
	ax.set_theta_direction(-1)

	ax.set_xticks(angles[:-1])
	ax.set_xticklabels(labels, fontsize=10)

	ax.set_ylim(0, 4)
	ax.set_yticks([1, 2, 3, 4])
	ax.set_yticklabels(["1", "2", "3", "4"], fontsize=9)
	ax.set_rlabel_position(90)
	ax.grid(color="#D0D0D0", linestyle="-", linewidth=0.8)

	ax.plot(angles, company_plot_values, color="#1f77b4", linewidth=2.2, label=chart_strings["company"])
	ax.fill(angles, company_plot_values, color="#1f77b4", alpha=0.2)

	ax.plot(
		angles,
		benchmark_plot_values,
		color="#ff7f0e",
		linewidth=2.0,
		linestyle="--",
		label=chart_strings["benchmark"],
	)

	ax.set_title(
		f"{chart_strings['title']} — {chart_strings['company']}",
		fontsize=14,
		pad=22,
		fontweight="normal",
	)
	ax.legend(loc="upper right", bbox_to_anchor=(1.22, 1.12), frameon=False)

	buffer = BytesIO()
	plt.tight_layout()
	fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
	plt.close(fig)
	buffer.seek(0)
	return buffer.getvalue()
