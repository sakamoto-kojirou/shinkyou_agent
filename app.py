"""Streamlit entry point for the shinkyou_agent (診鏡 Shinkyō Agent)."""

from __future__ import annotations

from typing import Any

import streamlit as st

from agent.llm_analyzer import LLMAnalyzer
from agent.meti_framework import DIMENSIONS, get_text
from agent.questionnaire import QuestionnaireEngine, run_demo_techbridge
from agent.scoring_engine import ScoringEngine
from report.pdf_generator import PDFGenerator
from report.radar_chart import generate_radar_chart


def get_ui_text(key: str, language: str) -> str:
	"""Return localized UI text for the application."""

	texts: dict[str, dict[str, str]] = {
		"en": {
			"app_title": "shinkyou_agent (診鏡 Shinkyō Agent)",
			"page_title": "shinkyou_agent (診鏡 Shinkyō Agent) | Digital Transformation Maturity Diagnostic",
			"welcome_title": "Digital Transformation Maturity Diagnostic",
			"welcome_body": (
				"An academic assessment tool for SME managers based on the METI DX Promotion Index. "
				"It combines structured interview answers, quantitative scoring, and LLM-supported analysis."
			),
			"meti_badge": "Based on the METI DX Promotion Index (2019)",
			"start_diagnostic": "Start Diagnostic",
			"language_label": "Select language",
			"profile_title": "Company Profile",
			"company_name": "Company Name",
			"sector": "Sector",
			"employees": "Number of Employees",
			"country": "Country",
			"demo_mode": "Demo Mode",
			"begin_assessment": "Begin Assessment",
			"questionnaire_title": "Diagnostic Interview",
			"next_question": "Next Question",
			"open_response": "Open response",
			"likert_help": "0 = not started, 4 = fully developed within the METI DX maturity scale.",
            "score": "Score",
            "weight": "Weight",
            "weighted": "Weighted",
            "dimension": "Dimension",
			"optional_open_response": (
				"Optional: briefly explain your answer. This helps the qualitative analysis capture context, constraints, and current practices."
			),
			"analysis_title": "Analyzing Results",
			"analysis_message": "Analyzing your responses and preparing the diagnostic report...",
			"results_title": "Assessment Results",
			"maturity_level": "Overall Maturity Level",
			"generate_pdf": "Generate PDF Report",
			"download_pdf": "Download PDF Report",
			"start_new": "Start New Assessment",
			"benchmark": "Benchmark Comparison",
			"method": "Methodology",
			"no_question": "No current question is available.",
			"error_generic": "Something went wrong while generating the report.",
			"error_missing_profile": "Please complete the company profile before starting the assessment.",
			"error_missing_response": "Please provide a Likert rating before moving to the next question.",
			"company_label": "Company",
			"question_label": "Question",
			"score_table": "Score Table",
			"gaps": "Gaps",
			"recommendations": "Recommendations",
			"pdf_ready": "PDF report is ready for download.",
			"sector_other": "Other",
			"employees_lt10": "<10",
			"employees_10_49": "10-49",
			"employees_50_249": "50-249",
			"employees_250_plus": "250+",
			"lang_en": "English",
			"lang_pt": "Português",
			"lang_ja": "日本語",
			"welcome_about_title": "About this tool",
			"welcome_about_body": (
				"**診鏡 Shinkyō Agent** is an academic prototype developed as part of a research portfolio "
				"for postgraduate studies at Tohoku University (Graduate School of Economics and Management), "
				"under the research theme: *'AI Automation of Operational Processes in SMEs — An Empirical Analysis Using Data Science'*.\n\n"
				"It is designed as a structured diagnostic instrument, not a commercial product. "
				"The assessment framework is the **METI DX Promotion Index (DX推進指標, 2019)** — "
				"Japan's official government framework for evaluating digital transformation maturity in organizations."
			),
			"welcome_how_title": "How it works",
			"welcome_how_step1": "**1. Company profile** — Enter basic information about your organization (name, sector, size, country).",
			"welcome_how_step2": "**2. Diagnostic interview** — Answer 16 questions across 5 dimensions of the METI DX Index. Each question uses a 0–4 maturity scale plus an optional open field.",
			"welcome_how_step3": "**3. AI-generated report** — An LLM analyzes your responses and generates a structured PDF report with maturity scores, identified gaps, and prioritized recommendations.",
			"welcome_dimensions_title": "The 5 assessment dimensions (METI DX Index)",
			"welcome_dim1": "Strategy & Vision",
			"welcome_dim2": "Business Process",
			"welcome_dim3": "Organization & Human Capital",
			"welcome_dim4": "Digital Foundation & Data",
			"welcome_dim5": "Governance & Risk",
			"welcome_ethics_title": "Privacy & data ethics",
			"welcome_ethics_body": (
				"🔒 **This tool does not collect, store, or transmit any data.** "
				"All responses exist only in your browser session and are permanently discarded when you close the page or start a new assessment. "
				"No information is sent to any database, server log, or third party beyond the AI analysis API call (Groq). "
				"This prototype is intended for demonstration and academic evaluation purposes only."
			),
			"welcome_author": "Developed by",
			"welcome_institution": "Portfolio project for MEXT Scholarship application · Tohoku University",
		},
		"pt": {
			"app_title": "shinkyou_agent (診鏡 Shinkyō Agent)",
			"page_title": "shinkyou_agent (診鏡 Shinkyō Agent) | Diagnóstico de Maturidade em Transformação Digital",
			"welcome_title": "Diagnóstico de Maturidade em Transformação Digital",
			"welcome_body": (
				"Uma ferramenta acadêmica de avaliação para gestores de PMEs com base no METI DX Promotion Index. "
				"Ela combina respostas de entrevista estruturada, pontuação quantitativa e análise assistida por LLM."
			),
			"meti_badge": "Baseado no METI DX Promotion Index (2019)",
			"start_diagnostic": "Iniciar Diagnóstico",
			"language_label": "Selecionar idioma",
			"profile_title": "Perfil da Empresa",
			"company_name": "Nome da Empresa",
			"sector": "Setor",
			"employees": "Número de Colaboradores",
			"country": "País",
			"demo_mode": "Modo Demo",
			"begin_assessment": "Iniciar Avaliação",
			"questionnaire_title": "Entrevista Diagnóstica",
			"next_question": "Próxima Pergunta",
			"open_response": "Resposta aberta",
			"likert_help": "0 = não iniciado, 4 = totalmente desenvolvido na escala de maturidade DX da METI.",
			"score": "Pontuação",
			"weight": "Peso",
			"weighted": "Ponderado",
			"dimension": "Dimensão",
			"optional_open_response": (
				"Opcional: explique brevemente sua resposta. Isso ajuda a análise qualitativa a capturar contexto, restrições e práticas atuais."
			),
			"analysis_title": "Analisando Resultados",
			"analysis_message": "Analisando suas respostas e preparando o relatório diagnóstico...",
			"results_title": "Resultados da Avaliação",
			"maturity_level": "Nível Geral de Maturidade",
			"generate_pdf": "Gerar Relatório em PDF",
			"download_pdf": "Baixar Relatório em PDF",
			"start_new": "Iniciar Nova Avaliação",
			"benchmark": "Comparação com Referência",
			"method": "Metodologia",
			"no_question": "Nenhuma pergunta atual está disponível.",
			"error_generic": "Ocorreu um erro ao gerar o relatório.",
			"error_missing_profile": "Preencha o perfil da empresa antes de iniciar a avaliação.",
			"error_missing_response": "Informe uma nota Likert antes de avançar para a próxima pergunta.",
			"company_label": "Empresa",
			"question_label": "Pergunta",
			"score_table": "Tabela de Pontuação",
			"gaps": "Lacunas",
			"recommendations": "Recomendações",
			"pdf_ready": "O relatório em PDF está pronto para download.",
			"sector_other": "Outro",
			"employees_lt10": "<10",
			"employees_10_49": "10-49",
			"employees_50_249": "50-249",
			"employees_250_plus": "250+",
			"lang_en": "Inglês",
			"lang_pt": "Português",
			"lang_ja": "Japonês",
			"welcome_about_title": "Sobre esta ferramenta",
			"welcome_about_body": (
				"**診鏡 Shinkyō Agent** é um protótipo acadêmico desenvolvido como parte de um portfólio de pesquisa "
				"para pós-graduação na Universidade de Tohoku (Graduate School of Economics and Management), "
				"alinhado ao tema: *'Automação de Processos Operacionais em PMEs por IA — Análise Empírica Utilizando Data Science'*.\n\n"
				"É concebido como instrumento de diagnóstico estruturado, não como produto comercial. "
				"O framework utilizado é o **METI DX Promotion Index (DX推進指標, 2019)** — "
				"o instrumento oficial do governo japonês para avaliar a maturidade em transformação digital nas organizações."
			),
			"welcome_how_title": "Como funciona",
			"welcome_how_step1": "**1. Perfil da empresa** — Informe dados básicos sobre sua organização (nome, setor, porte, país).",
			"welcome_how_step2": "**2. Entrevista diagnóstica** — Responda 16 perguntas em 5 dimensões do METI DX Index. Cada pergunta usa escala de maturidade 0–4 com campo aberto opcional.",
			"welcome_how_step3": "**3. Relatório gerado por IA** — Um LLM analisa suas respostas e gera um relatório PDF estruturado com scores de maturidade, lacunas identificadas e recomendações priorizadas.",
			"welcome_dimensions_title": "As 5 dimensões avaliadas (METI DX Index)",
			"welcome_dim1": "Estratégia e Visão",
			"welcome_dim2": "Processos de Negócio",
			"welcome_dim3": "Organização e Capital Humano",
			"welcome_dim4": "Base Digital e Dados",
			"welcome_dim5": "Governança e Riscos",
			"welcome_ethics_title": "Privacidade e ética de dados",
			"welcome_ethics_body": (
				"🔒 **Esta ferramenta não coleta, armazena nem transmite nenhum dado.** "
				"Todas as respostas existem apenas na sessão do seu navegador e são descartadas permanentemente ao fechar a página ou iniciar uma nova avaliação. "
				"Nenhuma informação é enviada a banco de dados, log de servidor ou terceiros além da chamada à API de análise por IA (Groq). "
				"Este protótipo destina-se exclusivamente a fins de demonstração e avaliação acadêmica."
			),
			"welcome_author": "Desenvolvido por",
			"welcome_institution": "Projeto de portfólio para candidatura à Bolsa MEXT · Universidade de Tohoku",
		},
		"ja": {
			"app_title": "shinkyou_agent (診鏡 Shinkyō Agent)",
			"page_title": "shinkyou_agent (診鏡 Shinkyō Agent) | デジタル変革成熟度診断",
			"welcome_title": "デジタル変革成熟度診断",
			"welcome_body": (
				"METI DX推進指標に基づく、中小企業経営者向けの学術的な評価ツールです。 "
				"構造化されたインタビュー回答、定量評価、LLMによる定性分析を組み合わせます。"
			),
			"meti_badge": "METI DX推進指標（2019）に基づく",
			"start_diagnostic": "診断を開始",
			"language_label": "言語を選択",
			"profile_title": "企業情報",
			"company_name": "会社名",
			"sector": "業種",
			"employees": "従業員数",
			"country": "国名",
			"demo_mode": "デモモード",
			"begin_assessment": "評価を開始",
			"questionnaire_title": "診断インタビュー",
			"next_question": "次の質問へ",
			"open_response": "自由記述",
			"likert_help": "0 = 未着手、4 = METI DX成熟度の最高段階です。",
			"score": "スコア",
			"weight": "重み",
			"weighted": "加重値",
			"dimension": "観点",
			"optional_open_response": (
				"任意: 回答の背景を簡潔にご記入ください。定性分析が現状の制約や実務を把握しやすくなります。"
			),
			"analysis_title": "分析中",
			"analysis_message": "回答を分析し、診断レポートを作成しています...",
			"results_title": "評価結果",
			"maturity_level": "総合成熟度レベル",
			"generate_pdf": "PDFレポートを生成",
			"download_pdf": "PDFレポートをダウンロード",
			"start_new": "新しい評価を開始",
			"benchmark": "ベンチマーク比較",
			"method": "方法論",
			"no_question": "現在の質問はありません。",
			"error_generic": "レポート作成中にエラーが発生しました。",
			"error_missing_profile": "評価を開始する前に企業情報を入力してください。",
			"error_missing_response": "次の質問へ進む前にLikert評価を入力してください。",
			"company_label": "企業",
			"question_label": "質問",
			"score_table": "スコア表",
			"gaps": "ギャップ",
			"recommendations": "改善提案",
			"pdf_ready": "PDFレポートの準備ができました。",
			"sector_other": "その他",
			"employees_lt10": "10人未満",
			"employees_10_49": "10〜49人",
			"employees_50_249": "50〜249人",
			"employees_250_plus": "250人以上",
			"lang_en": "英語",
			"lang_pt": "ポルトガル語",
			"lang_ja": "日本語",
			"welcome_about_title": "このツールについて",
			"welcome_about_body": (
				"**診鏡 Shinkyō Agent** は、東北大学大学院（経済学研究科）への進学を目指した研究ポートフォリオとして開発された学術プロトタイプです。"
				"研究テーマは「中小企業における業務プロセスのAI自動化 — データサイエンスを活用した実証分析」です。\n\n"
				"本ツールは商業製品ではなく、構造化された診断手法として設計されています。"
				"評価フレームワークには、**METI DX推進指標（2019年）** — 経済産業省が公表した組織のデジタル変革成熟度評価のための公式指標 — を使用しています。"
			),
			"welcome_how_title": "使い方",
			"welcome_how_step1": "**1. 企業情報の入力** — 組織の基本情報（名称・業種・規模・所在国）を入力します。",
			"welcome_how_step2": "**2. 診断インタビュー** — METI DX推進指標の5つの観点に基づく16の設問に回答します。各設問は0〜4の成熟度スケールと任意の自由記述欄で構成されています。",
			"welcome_how_step3": "**3. AIによるレポート生成** — LLMが回答を分析し、成熟度スコア・課題・優先度付きの改善提案を含む構造化されたPDFレポートを生成します。",
			"welcome_dimensions_title": "評価の5つの観点（METI DX推進指標）",
			"welcome_dim1": "戦略・ビジョン",
			"welcome_dim2": "業務プロセス",
			"welcome_dim3": "組織・人材",
			"welcome_dim4": "デジタル基盤・データ",
			"welcome_dim5": "ガバナンス・リスク管理",
			"welcome_ethics_title": "プライバシーとデータ倫理",
			"welcome_ethics_body": (
				"🔒 **本ツールは、いかなるデータも収集・保存・送信しません。** "
				"すべての回答はブラウザのセッション内にのみ存在し、ページを閉じるか新しい評価を開始した時点で完全に削除されます。"
				"AI分析API（Groq）への呼び出しを除き、データベース・サーバーログ・第三者へ情報が送られることはありません。"
				"本プロトタイプは、デモンストレーションおよび学術評価を目的としたものです。"
			),
			"welcome_author": "開発者",
			"welcome_institution": "MEXTスカラーシップ申請ポートフォリオ · 東北大学",
		},
	}

	normalized = language if language in texts else "en"
	return texts[normalized].get(key, key)


def _initialize_state() -> None:
	"""Ensure Streamlit session state has the required defaults."""

	defaults: dict[str, Any] = {
		"language": "en",
		"phase": "welcome",
		"company_profile": {},
		"questionnaire_engine": None,
		"llm_analysis": None,
		"scoring_result": None,
		"radar_chart_bytes": None,
		"pdf_bytes": None,
		"current_answer": "",
		"current_score": 0,
		"sector_choice": "Logistics services",
		"employees_choice": "10-49",
	}
	for key, value in defaults.items():
		if key not in st.session_state:
			st.session_state[key] = value


def _translate_sector_options(language: str) -> list[str]:
	"""Return localized sector dropdown options."""

	return {
		"en": ["Logistics services", "Manufacturing", "Retail", "Professional services", "Other"],
		"pt": ["Serviços de logística", "Manufatura", "Varejo", "Serviços profissionais", "Outro"],
		"ja": ["物流サービス", "製造業", "小売業", "専門サービス", "その他"],
	}.get(language, ["Logistics services", "Manufacturing", "Retail", "Professional services", "Other"])


def _employee_options(language: str) -> list[str]:
	"""Return localized employee-size options."""

	return [
		get_ui_text("employees_lt10", language),
		get_ui_text("employees_10_49", language),
		get_ui_text("employees_50_249", language),
		get_ui_text("employees_250_plus", language),
	]


def _language_buttons() -> None:
	"""Render the language selector on the welcome screen."""

	col1, col2, col3 = st.columns(3)
	if col1.button(get_ui_text("lang_en", st.session_state.language), use_container_width=True):
		st.session_state.language = "en"
	if col2.button(get_ui_text("lang_pt", st.session_state.language), use_container_width=True):
		st.session_state.language = "pt"
	if col3.button(get_ui_text("lang_ja", st.session_state.language), use_container_width=True):
		st.session_state.language = "ja"


def _start_diagnostic() -> None:
	"""Move the app into the profile phase."""

	st.session_state.phase = "profile"


def _reset_assessment() -> None:
	"""Reset the workflow to its initial state."""

	st.session_state.phase = "welcome"
	st.session_state.company_profile = {}
	st.session_state.questionnaire_engine = None
	st.session_state.llm_analysis = None
	st.session_state.scoring_result = None
	st.session_state.radar_chart_bytes = None
	st.session_state.pdf_bytes = None
	st.session_state.current_answer = ""
	st.session_state.current_score = 0
	st.session_state.sector_choice = "Logistics services"
	st.session_state.employees_choice = "10-49"


def _build_company_profile_from_form(language: str, company_name: str, sector: str, employees: str, country: str) -> dict[str, Any]:
	"""Create a normalized company profile dictionary from form fields."""

	return {
		"company_name": company_name.strip(),
		"sector": sector,
		"employees": employees,
		"country": country.strip(),
		"language": language,
	}


def _render_welcome(language: str) -> None:
	"""Render the welcome phase with full project context and ethics notice."""

	# ── Header ──────────────────────────────────────────────────────────
	st.title(get_ui_text("welcome_title", language))
	st.caption(get_ui_text("meti_badge", language))
	st.divider()

	# ── Language selector (top, always visible) ──────────────────────────
	st.write(f"**{get_ui_text('language_label', language)}**")
	_language_buttons()
	st.divider()

	# ── Two-column layout: About + How it works ──────────────────────────
	col_left, col_right = st.columns([1, 1], gap="large")

	with col_left:
		st.subheader(get_ui_text("welcome_about_title", language))
		st.markdown(get_ui_text("welcome_about_body", language))

	with col_right:
		st.subheader(get_ui_text("welcome_how_title", language))
		st.markdown(get_ui_text("welcome_how_step1", language))
		st.markdown(get_ui_text("welcome_how_step2", language))
		st.markdown(get_ui_text("welcome_how_step3", language))

	st.divider()

	# ── 5 Dimensions ────────────────────────────────────────────────────
	st.subheader(get_ui_text("welcome_dimensions_title", language))
	d_col1, d_col2, d_col3, d_col4, d_col5 = st.columns(5)
	for col, key, color in [
		(d_col1, "welcome_dim1", "#163A63"),
		(d_col2, "welcome_dim2", "#1A5276"),
		(d_col3, "welcome_dim3", "#1F618D"),
		(d_col4, "welcome_dim4", "#2471A3"),
		(d_col5, "welcome_dim5", "#2980B9"),
	]:
		col.markdown(
			f"<div style='background:{color}; color:white; padding:10px 12px; border-radius:8px; "
			f"font-size:0.82rem; font-weight:600; text-align:center; min-height:64px; "
			f"display:flex; align-items:center; justify-content:center;'>"
			f"{get_ui_text(key, language)}</div>",
			unsafe_allow_html=True,
		)

	st.divider()

	# ── Ethics / Privacy notice ──────────────────────────────────────────
	st.subheader(get_ui_text("welcome_ethics_title", language))
	st.success(get_ui_text("welcome_ethics_body", language))

	st.divider()

	# ── CTA ─────────────────────────────────────────────────────────────
	st.button(
		get_ui_text("start_diagnostic", language),
		type="primary",
		use_container_width=True,
		on_click=_start_diagnostic,
	)


def _render_profile(language: str) -> None:
	"""Render the company profile phase."""

	st.header(get_ui_text("profile_title", language))

	if st.button(get_ui_text("demo_mode", language), use_container_width=True):
		demo_engine = run_demo_techbridge()
		st.session_state.company_profile = {
			"company_name": "TechBridge Ltda.",
			"sector": "Logistics services",
			"employees": "10-49",
			"country": "Brazil",
			"language": language,
		}
		st.session_state.questionnaire_engine = demo_engine
		st.session_state.phase = "analyzing"
		st.rerun()

	with st.form("company_profile_form", clear_on_submit=False):
		company_name = st.text_input(get_ui_text("company_name", language), value=st.session_state.company_profile.get("company_name", ""))
		sector_options = _translate_sector_options(language)
		sector_default = st.session_state.company_profile.get("sector", sector_options[0])
		sector = st.selectbox(get_ui_text("sector", language), sector_options, index=sector_options.index(sector_default) if sector_default in sector_options else 0)
		employee_options = _employee_options(language)
		employee_default = st.session_state.company_profile.get("employees", employee_options[1]) if len(employee_options) > 1 else employee_options[0]
		employees = st.selectbox(get_ui_text("employees", language), employee_options, index=employee_options.index(employee_default) if employee_default in employee_options else 0)
		country = st.text_input(get_ui_text("country", language), value=st.session_state.company_profile.get("country", ""))

		submitted = st.form_submit_button(get_ui_text("begin_assessment", language), use_container_width=True)
		if submitted:
			if not company_name.strip() or not country.strip():
				st.error(get_ui_text("error_missing_profile", language))
			else:
				st.session_state.company_profile = _build_company_profile_from_form(language, company_name, sector, employees, country)
				st.session_state.questionnaire_engine = QuestionnaireEngine(language=language, company_profile=st.session_state.company_profile)
				st.session_state.phase = "questionnaire"


def _render_questionnaire(language: str) -> None:
	"""Render the interview phase."""

	engine: QuestionnaireEngine | None = st.session_state.questionnaire_engine
	if engine is None:
		st.error(get_ui_text("error_missing_profile", language))
		st.session_state.phase = "profile"
		return

	question = engine.get_current_question()
	dimension = engine.get_current_dimension()
	progress = engine.get_progress()

	st.header(get_ui_text("questionnaire_title", language))
	st.progress(progress["percent"] / 100.0)

	if dimension is not None:
		st.subheader(get_text(dimension, language))
	if question is None:
		st.warning(get_ui_text("no_question", language))
		st.session_state.phase = "analyzing"
		return

	st.markdown(f"**{get_ui_text('question_label', language)}:** {get_text(question, language)}")

	# Show contextual hint if available (e.g. explain "DX Vision" on Q1)
	hint = getattr(question, f"hint_{language}", "") or getattr(question, "hint_en", "")
	if hint:
		st.info(hint)

	# Use question.id as key so widgets fully reset between questions
	st.session_state.current_score = st.slider(
		label=get_ui_text("score", language),
		min_value=0,
		max_value=4,
		value=int(st.session_state.current_score),
		help=get_ui_text("likert_help", language),
		key=f"slider_q{question.id}",
	)
	st.session_state.current_answer = st.text_area(
		label=get_ui_text("open_response", language),
		value=st.session_state.current_answer,
		placeholder=get_ui_text("optional_open_response", language),
		height=120,
		key=f"open_q{question.id}",
	)

	if st.button(get_ui_text("next_question", language), type="primary", use_container_width=True):
		if st.session_state.current_score is None:
			st.error(get_ui_text("error_missing_response", language))
			return
		previous_dimension_id = question.dimension_id
		engine.submit_answer(int(st.session_state.current_score), st.session_state.current_answer)
		st.session_state.current_answer = ""
		st.session_state.current_score = 0
		if engine.state.is_complete:
			st.session_state.phase = "analyzing"
		else:
			next_dimension = engine.get_current_dimension()
			if next_dimension is not None and next_dimension.id != previous_dimension_id:
				st.balloons()
		st.rerun()


def _render_analyzing(language: str) -> None:
	"""Analyze responses and prepare the report payload."""

	engine: QuestionnaireEngine | None = st.session_state.questionnaire_engine
	if engine is None:
		st.error(get_ui_text("error_missing_profile", language))
		st.session_state.phase = "profile"
		return

	st.header(get_ui_text("analysis_title", language))
	with st.spinner(get_ui_text("analysis_message", language)):
		try:
			llm_analyzer = LLMAnalyzer(language=language)
			scoring_engine = ScoringEngine()
			quantitative_scores: dict[int, float] = {}
			for dimension in DIMENSIONS:
				bucket = engine.get_all_responses().get(dimension.id, engine.get_all_responses().get(str(dimension.id), {}))
				likert_scores = bucket.get("likert_scores", []) if isinstance(bucket, dict) else []
				if isinstance(likert_scores, list):
					numeric_scores = [int(score) for score in likert_scores if isinstance(score, int)]
					quantitative_scores[dimension.id] = scoring_engine.calculate_likert_average(numeric_scores)
				else:
					quantitative_scores[dimension.id] = 0.0
			llm_analysis = llm_analyzer.analyze_all(
				engine.get_all_responses(),
				st.session_state.company_profile,
				quantitative_scores,
			)
			scoring_result = scoring_engine.build_scoring_result(engine.get_all_responses(), llm_analysis)
			company_name = st.session_state.company_profile.get("company_name", "Your Company")
			radar_chart_bytes = generate_radar_chart(scoring_result, language, company_name=company_name)

			st.session_state.llm_analysis = llm_analysis
			st.session_state.scoring_result = scoring_result
			st.session_state.radar_chart_bytes = radar_chart_bytes
			st.session_state.phase = "results"
			st.rerun()
		except Exception as exc:  # pragma: no cover - user-facing recovery path
			st.error(f"{get_ui_text('error_generic', language)} {exc}")
			st.session_state.phase = "questionnaire"


def _scores_dataframe(scoring_result: dict[str, Any], language: str):
	"""Build a pandas dataframe for the score table."""

	import pandas as pd

	rows = []
	for item in scoring_result["dimension_scores"]:
		dimension = next(d for d in DIMENSIONS if d.id == item["dimension_id"])
		rows.append(
			{
				get_ui_text("dimension", language): get_text(dimension, language),
				get_ui_text("score", language): round(item["composite_score"], 2),
				get_ui_text("weight", language): round(item["weight"], 2),
				get_ui_text("weighted", language): round(item["weighted_contribution"], 2),
			}
		)
	return pd.DataFrame(rows)


def _render_results(language: str) -> None:
	"""Render the final results phase."""

	scoring_result = st.session_state.scoring_result
	llm_analysis = st.session_state.llm_analysis
	radar_chart_bytes = st.session_state.radar_chart_bytes
	company_profile = st.session_state.company_profile

	if not scoring_result or not llm_analysis or not radar_chart_bytes:
		st.error(get_ui_text("error_generic", language))
		st.session_state.phase = "analyzing"
		return

	st.header(get_ui_text("results_title", language))

	level_color = {0: "#C0392B", 1: "#C0392B", 2: "#E67E22", 3: "#F1C40F", 4: "#2E8B57"}.get(scoring_result["maturity_level"], "#163A63")
	st.metric(
		get_ui_text("maturity_level", language),
		f"Level {scoring_result['maturity_level']} - {scoring_result['maturity_label_en']}",
	)
	st.markdown(
		f"<div style='background:{level_color}; color:white; padding:12px 16px; border-radius:10px; font-size:1.05rem; font-weight:600;'>"
		f"{scoring_result['maturity_label_en']} / {scoring_result['maturity_label_pt']} / {scoring_result['maturity_label_ja']}"
		f"</div>",
		unsafe_allow_html=True,
	)

	st.image(radar_chart_bytes, use_container_width=True)

	st.subheader(get_ui_text("score_table", language))
	st.dataframe(_scores_dataframe(scoring_result, language), use_container_width=True, hide_index=True)

	for item in scoring_result["dimension_scores"]:
		dimension = next(dimension for dimension in DIMENSIONS if dimension.id == item["dimension_id"])
		analysis = next(a for a in llm_analysis["dimensions"] if a["dimension_id"] == dimension.id)
		with st.expander(get_text(dimension, language), expanded=False):
			st.write(f"**{get_ui_text('gaps', language)}**")
			for gap in analysis["gaps"]:
				st.write(f"- {gap}")
			st.write(f"**{get_ui_text('recommendations', language)}**")
			for index, recommendation in enumerate(analysis["recommendations"][:3], start=1):
				st.write(f"{index}. {recommendation}")

	if st.button(get_ui_text("generate_pdf", language), use_container_width=True):
		try:
			pdf_generator = PDFGenerator(language)
			pdf_bytes = pdf_generator.generate(company_profile, scoring_result, llm_analysis, radar_chart_bytes)
			st.session_state.pdf_bytes = pdf_bytes
		except Exception as exc:  # pragma: no cover - user-facing recovery path
			st.error(f"{get_ui_text('error_generic', language)} {exc}")

	if st.session_state.pdf_bytes:
		company_slug = company_profile.get("company_name", "company").replace(" ", "_").lower()
		st.download_button(
			label=get_ui_text("download_pdf", language),
			data=st.session_state.pdf_bytes,
			file_name=f"dx_report_{company_slug}.pdf",
			mime="application/pdf",
			use_container_width=True,
		)
		st.success(get_ui_text("pdf_ready", language))

	if st.button(get_ui_text("start_new", language), use_container_width=True):
		_reset_assessment()
		st.rerun()


def main() -> None:
	"""Run the Streamlit application."""

	_initialize_state()
	st.set_page_config(page_title=get_ui_text("page_title", st.session_state.language), layout="wide")
	st.title(get_ui_text("app_title", st.session_state.language))

	phase = st.session_state.phase
	language = st.session_state.language

	if phase == "welcome":
		_render_welcome(language)
	elif phase == "profile":
		_render_profile(language)
	elif phase == "questionnaire":
		_render_questionnaire(language)
	elif phase == "analyzing":
		_render_analyzing(language)
	elif phase == "results":
		_render_results(language)
	else:
		st.session_state.phase = "welcome"
		st.rerun()


if __name__ == "__main__":
	main()