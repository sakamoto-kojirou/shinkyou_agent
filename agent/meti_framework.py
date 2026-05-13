"""METI DX Promotion Index framework definitions and questionnaire content.

This module centralizes the academic framework used by the shinkyou_agent (診鏡 Shinkyō Agent).
It provides the five assessment dimensions, the interview questions in three
languages, and the maturity scale used for scoring and reporting.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Dimension:
	"""Represent one DX assessment dimension."""

	id: int
	weight: float
	name_en: str
	name_pt: str
	name_ja: str


@dataclass(frozen=True)
class Question:
	"""Represent one structured interview question."""

	id: int
	dimension_id: int
	text_en: str
	text_pt: str
	text_ja: str
	likert_scale: tuple[int, int] = (0, 4)
	has_open_field: bool = False
	hint_en: str = ""
	hint_pt: str = ""
	hint_ja: str = ""


@dataclass(frozen=True)
class MaturityLevel:
	"""Represent one METI maturity level."""

	level: int
	label_en: str
	label_pt: str
	label_ja: str
	description_en: str


DIMENSIONS: list[Dimension] = [
	Dimension(
		id=1,
		weight=0.20,
		name_en="Strategy & Vision",
		name_pt="Estratégia e Visão",
		name_ja="戦略・ビジョン",
	),
	Dimension(
		id=2,
		weight=0.30,
		name_en="Business Process",
		name_pt="Processos de Negócio",
		name_ja="業務プロセス",
	),
	Dimension(
		id=3,
		weight=0.20,
		name_en="Organization & Human Capital",
		name_pt="Organização e Capital Humano",
		name_ja="組織・人材",
	),
	Dimension(
		id=4,
		weight=0.20,
		name_en="Digital Foundation & Data",
		name_pt="Base Digital e Dados",
		name_ja="デジタル基盤・データ",
	),
	Dimension(
		id=5,
		weight=0.10,
		name_en="Governance & Risk",
		name_pt="Governança e Riscos",
		name_ja="ガバナンス・リスク管理",
	),
]


QUESTIONS: list[Question] = [
	Question(
		id=1,
		dimension_id=1,
		text_en="How clearly has your company defined its DX vision and linked it to business strategy?",
		text_pt="Até que ponto sua empresa definiu claramente a visão de DX e a vinculou à estratégia de negócios?",
		text_ja="貴社のDXビジョンはどの程度明確に定義され、経営戦略と結びついていますか。",
		has_open_field=True,
		hint_en=(
			"DX Vision (Digital Transformation Vision) is a formal declaration of how the company "
			"intends to use technology to transform its business model, operations, or value creation. "
			"It answers: 'Where do we want to be in 5 years as a digital organization, and why?'"
		),
		hint_pt=(
			"Visão de DX (Transformação Digital) é uma declaração formal de como a empresa pretende "
			"usar tecnologia para transformar seu modelo de negócio, operações ou criação de valor. "
			"Responde à pergunta: 'Onde queremos estar em 5 anos como organização digital, e por quê?'"
		),
		hint_ja=(
			"DXビジョンとは、企業がテクノロジーを活用して事業モデル・業務・価値創造をどのように変革するかを示す正式な方針です。"
			"「デジタル組織として5年後にどこを目指すのか、なぜそれが重要か」という問いへの回答です。"
		),
	),
	Question(
		id=2,
		dimension_id=1,
		text_en="How consistently does top management communicate DX priorities and expected outcomes?",
		text_pt="Com que consistência a alta administração comunica as prioridades de DX e os resultados esperados?",
		text_ja="経営層はDXの優先事項と期待成果を、どの程度一貫して社内に発信していますか。",
		has_open_field=True,
	),
	Question(
		id=3,
		dimension_id=1,
		text_en="To what extent are DX initiatives measured through strategic objectives and performance indicators?",
		text_pt="Em que medida as iniciativas de DX são avaliadas por meio de objetivos estratégicos e indicadores de desempenho?",
		text_ja="DX施策は、戦略目標や業績指標を用いてどの程度測定されていますか。",
		has_open_field=True,
	),
	Question(
		id=4,
		dimension_id=2,
		text_en="What is the current level of process automation in your core operations?",
		text_pt="Qual é o nível atual de automação dos processos nas operações principais da empresa?",
		text_ja="主要業務における業務プロセスの自動化は、現在どの程度進んでいますか。",
		has_open_field=True,
	),
	Question(
		id=5,
		dimension_id=2,
		text_en="How often are operational decisions supported by data rather than intuition or personal experience?",
		text_pt="Com que frequência as decisões operacionais são apoiadas por dados, em vez de intuição ou experiência pessoal?",
		text_ja="業務上の意思決定は、勘や個人経験ではなく、データに基づいて行われることがどの程度ありますか。",
		has_open_field=True,
	),
	Question(
		id=6,
		dimension_id=2,
		text_en="How would you describe the balance between manual workflows and digital workflows in daily operations?",
		text_pt="Como você descreveria o equilíbrio entre fluxos de trabalho manuais e digitais nas operações diárias?",
		text_ja="日常業務における手作業とデジタル化された業務フローの比率を、どのように捉えていますか。",
		has_open_field=True,
	),
	Question(
		id=7,
		dimension_id=2,
		text_en="To what extent are AI or software tools actively used to improve operational efficiency or service quality?",
		text_pt="Em que medida ferramentas de IA ou software são ativamente utilizadas para melhorar a eficiência operacional ou a qualidade do serviço?",
		text_ja="業務効率やサービス品質の向上に向けて、AIやソフトウェアツールはどの程度積極的に活用されていますか。",
		has_open_field=True,
		hint_en=(
			"Rate the overall adoption level (0 = no tools used, 4 = AI/software deeply integrated in core operations). "
			"In the text field below, list the main tools used (e.g. spreadsheets, ERP, CRM, chatbots, RPA, analytics platforms)."
		),
		hint_pt=(
			"Avalie o nível geral de adoção (0 = nenhuma ferramenta, 4 = IA/software profundamente integrado nas operações principais). "
			"No campo de texto abaixo, liste as principais ferramentas utilizadas (ex: planilhas, ERP, CRM, chatbots, RPA, plataformas de análise)."
		),
		hint_ja=(
			"総合的な活用レベルを評価してください（0＝ツール未使用、4＝AIやソフトウェアが中核業務に深く統合）。"
			"下のテキスト欄に、主な使用ツールをご記入ください（例：表計算ソフト、ERP、CRM、チャットボット、RPA、分析ツールなど）。"
		),
	),
	Question(
		id=8,
		dimension_id=3,
		text_en="How developed are employee digital skills and DX-related training opportunities?",
		text_pt="Quão desenvolvidas são as competências digitais dos colaboradores e as oportunidades de capacitação em DX?",
		text_ja="従業員のデジタルスキルやDX関連の教育機会は、どの程度整備されていますか。",
		has_open_field=True,
	),
	Question(
		id=9,
		dimension_id=3,
		text_en="How effectively do teams collaborate across departments when implementing DX initiatives?",
		text_pt="Com que eficácia as equipes colaboram entre departamentos na implementação de iniciativas de DX?",
		text_ja="DX施策の推進にあたり、部門横断での連携はどの程度機能していますか。",
		has_open_field=True,
	),
	Question(
		id=10,
		dimension_id=3,
		text_en="Are there clear roles or responsible persons for DX promotion, data management, and change support?",
		text_pt="Existem funções ou responsáveis claros para a promoção de DX, gestão de dados e apoio à mudança?",
		text_ja="DX推進、データ管理、変革支援について、明確な役割や責任者は定められていますか。",
		has_open_field=True,
	),
	Question(
		id=11,
		dimension_id=4,
		text_en="How integrated are your core systems and data sources across departments?",
		text_pt="Quão integrados estão os sistemas centrais e as fontes de dados entre os departamentos?",
		text_ja="基幹システムやデータソースは、部門間でどの程度統合されていますか。",
		has_open_field=True,
	),
	Question(
		id=12,
		dimension_id=4,
		text_en="How would you assess the quality, consistency, and accessibility of company data?",
		text_pt="Como você avalia a qualidade, a consistência e a acessibilidade dos dados da empresa?",
		text_ja="社内データの品質、一貫性、アクセスしやすさは、どの程度確保されていますか。",
		has_open_field=True,
	),
	Question(
		id=13,
		dimension_id=4,
		text_en="How mature is your digital infrastructure for cloud use, secure sharing, and scalable growth?",
		text_pt="Quão madura é a infraestrutura digital para uso em nuvem, compartilhamento seguro e crescimento escalável?",
		text_ja="クラウド活用、安全な情報共有、将来の拡張に対応できるデジタル基盤はどの程度整っていますか。",
		has_open_field=True,
	),
	Question(
		id=14,
		dimension_id=5,
		text_en="How well are DX decisions governed through formal policies, responsibilities, and approval processes?",
		text_pt="Com que nível de governança as decisões de DX são conduzidas por políticas formais, responsabilidades e processos de aprovação?",
		text_ja="DXに関する意思決定は、正式な方針、責任分担、承認プロセスを通じて、どの程度適切に統制されていますか。",
		has_open_field=True,
	),
	Question(
		id=15,
		dimension_id=5,
		text_en="How systematically does the company manage cybersecurity, privacy, and compliance risks?",
		text_pt="Com que sistematicidade a empresa gerencia riscos de cibersegurança, privacidade e conformidade?",
		text_ja="サイバーセキュリティ、個人情報保護、法令遵守に関するリスクは、どの程度体系的に管理されていますか。",
		has_open_field=True,
	),
	Question(
		id=16,
		dimension_id=5,
		text_en="Are technology, vendor, and AI-related risks monitored with contingency plans in place?",
		text_pt="Os riscos relacionados à tecnologia, fornecedores e IA são monitorados com planos de contingência definidos?",
		text_ja="技術、ベンダー、AIに関するリスクは監視されており、必要な代替策や事業継続策は用意されていますか。",
		has_open_field=True,
	),
]


MATURITY_LEVELS: list[MaturityLevel] = [
	MaturityLevel(
		level=0,
		label_en="Not started",
		label_pt="Não iniciado",
		label_ja="未着手",
		description_en="No DX awareness or initiatives are in place.",
	),
	MaturityLevel(
		level=1,
		label_en="Partially initiated",
		label_pt="Iniciado parcialmente",
		label_ja="一部着手",
		description_en="DX activities exist as ad hoc or isolated experiments.",
	),
	MaturityLevel(
		level=2,
		label_en="Under consideration",
		label_pt="Em consideração",
		label_ja="検討中",
		description_en="The organization is planning expansion and beginning cross-functional coordination.",
	),
	MaturityLevel(
		level=3,
		label_en="Company-wide deployment",
		label_pt="Implantação em toda a empresa",
		label_ja="全社展開",
		description_en="DX is being implemented systematically across the organization.",
	),
	MaturityLevel(
		level=4,
		label_en="Industry leader",
		label_pt="Líder do setor",
		label_ja="トップランナー",
		description_en="The company operates as a global benchmark with continuous innovation.",
	),
]


def get_text(obj: Any, language: str) -> str:
	"""Return the best matching localized text for an object.

	The function searches for common language-specific field names in a
	pragmatic order so it works across the framework dataclasses.
	"""

	normalized_language = language.strip().lower()
	if normalized_language not in {"en", "pt", "ja"}:
		raise ValueError(f"Unsupported language: {language}")

	field_candidates = [
		f"text_{normalized_language}",
		f"name_{normalized_language}",
		f"label_{normalized_language}",
	]

	if normalized_language == "en":
		field_candidates.append("description_en")
	else:
		field_candidates.append("description_en")

	for field_name in field_candidates:
		if hasattr(obj, field_name):
			value = getattr(obj, field_name)
			if isinstance(value, str):
				return value

	if normalized_language != "en":
		for fallback_field in ("text_en", "name_en", "label_en", "description_en"):
			if hasattr(obj, fallback_field):
				value = getattr(obj, fallback_field)
				if isinstance(value, str):
					return value

	raise AttributeError(
		f"Object of type {type(obj).__name__} does not expose localized text fields."
	)


def get_dimension_by_id(dimension_id: int) -> Dimension:
	"""Return the Dimension matching the given id.

	Raises ValueError if the dimension is not found.
	"""
	for dimension in DIMENSIONS:
		if dimension.id == dimension_id:
			return dimension
	raise ValueError(f"Dimension with id={dimension_id} not found.")


def validate_weights() -> bool:
	"""Assert that all dimension weights sum to 1.0."""
	total = sum(d.weight for d in DIMENSIONS)
	assert abs(total - 1.0) < 1e-9, f"Dimension weights sum to {total}, expected 1.0"
	return True


# Run validation at import time
validate_weights()


def get_questions_for_dimension(dimension_id: int) -> list[Question]:
	"""Return all questionnaire items for one dimension."""

	return [question for question in QUESTIONS if question.dimension_id == dimension_id]