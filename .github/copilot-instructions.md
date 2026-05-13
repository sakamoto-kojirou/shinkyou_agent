# GitHub Copilot — Project Instructions

## Project Identity
## Project Name
- **Japanese:** 診鏡エージェント
- **Romanized:** Shinkyō Agent
- **GitHub repo:** shinkyou_agent
- **Meaning:** "Diagnostic Mirror" — 診 (diagnosis) + 鏡 (mirror, ref. Yata no Kagami)
- **Tagline:** "A diagnostic mirror for SME digital transformation maturity"
This is **診鏡 Shinkyō Agent** (shinkyou_agent), an academic AI-powered diagnostic tool for assessing
Digital Transformation (DX) maturity in SMEs (Small and Medium Enterprises).
It is part of a portfolio for a MEXT scholarship application to Tohoku University
(Graduate School of Economics and Management), aligned with research on
"AI Automation of Operational Processes in SMEs using Data Science".

## Research Grounding
The agent is based on Japan's official **METI DX Promotion Index (DX推進指標, 2019)**,
a government-issued self-assessment framework for organizational digital maturity.
All scoring logic, dimension names, and maturity levels MUST follow this framework.

## Maturity Scale (METI Standard)
- Level 0: 未着手 (Not started)
- Level 1: 一部着手 (Partially initiated)
- Level 2: 検討中 (Under consideration / expanding)
- Level 3: 全社展開 (Company-wide deployment)
- Level 4: トップランナー (Industry leader / global benchmark)

## Five Assessment Dimensions
1. Strategy & Vision (戦略・ビジョン)
2. Business Process (業務プロセス) ← PRIMARY FOCUS (AI automation research)
3. Organization & Human Capital (組織・人材)
4. Digital Foundation & Data (デジタル基盤・データ)
5. Governance & Risk (ガバナンス・リスク管理)

## Tech Stack
- Language: Python 3.11+
- LLM: Groq API (model: llama-3.1-70b-versatile) — FREE tier
- Interface: Streamlit
- PDF: ReportLab
- Charts: Matplotlib (radar chart embedded in PDF and Streamlit)
- i18n: 3 languages — English (en), Portuguese Brazil (pt), Japanese (ja)
- Environment: python-dotenv for API key management

## Code Rules for Copilot
1. ALL user-facing strings must use the i18n system (never hardcode text)
2. ALL functions must have docstrings in English
3. Return types must be annotated
4. LLM responses must always be parsed as JSON (never raw text)
5. Every scoring function must be independently testable (pure functions preferred)
6. PDF sections must mirror the METI DX Index report structure
7. Use dataclasses or TypedDict for structured data (no raw dicts in function signatures)

## File Responsibilities
- `agent/meti_framework.py` → Framework constants, questions, translations, maturity labels
- `agent/questionnaire.py`  → State machine for interview flow
- `agent/llm_analyzer.py`   → Groq API call + prompt + JSON parsing
- `agent/scoring_engine.py` → Score calculation, weighting, aggregation
- `report/radar_chart.py`   → Matplotlib radar chart → returns PNG bytes
- `report/pdf_generator.py` → ReportLab PDF assembly
- `app.py`                  → Streamlit UI, session state, orchestration

## Demo Company Profile (for testing)
Company: TechBridge Ltda.
Sector: Logistics services
Employees: 45
Country: Brazil
DX Stage: Early digitalization (transitioning from paper to digital)
Use this profile in all test functions and demo modes.