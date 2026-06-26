# shinkyou_agent (診鏡 Shinkyō Agent)

A research-oriented diagnostic agent for assessing SME digital transformation maturity using Japan's METI DX Promotion Index.

## What it does

- Conducts a structured interview across five DX maturity dimensions
- Scores responses using the METI 0–4 maturity scale
- Generates a radar chart and PDF diagnostic report
- Supports English, Portuguese (Brazil), and Japanese interfaces

## Core stack

- Python 3.11+
- Streamlit UI
- Groq API for LLM analysis
- ReportLab for PDF generation
- Matplotlib for charts

## Project structure

- `app.py` — Streamlit entry point
- `agent/` — framework, questionnaire, scoring, and LLM analysis logic
- `report/` — radar chart and PDF report generation
- `data/` — benchmark reference data
- `tests/` — scoring tests

## Run locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

link direto:
https://shinkyouagent-bfsxipybce2bimdqsm8rkg.streamlit.app/

- The project follows the METI DX Promotion Index framework.
- All user-facing text should go through the i18n layer.
- Demo profile: TechBridge Ltda., logistics services, 45 employees, Brazil.
