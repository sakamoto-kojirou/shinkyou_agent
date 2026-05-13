# System Architecture

## Data Flow
User Input (Streamlit)
│
▼
Company Profile → dict{name, sector, employees, country, language}
│
▼
Questionnaire State Machine (questionnaire.py)
│  16 questions: 5 dimensions × (2-4 questions each)
│  Format: Likert 0-4 scale + open text field
▼
Raw Responses → dict{dimension: {likert_scores[], text_responses[]}}
│
├──→ Scoring Engine (scoring_engine.py)
│       • Averages Likert scores per dimension
│       • Applies dimension weights
│       • Returns quantitative_score per dimension
│
└──→ LLM Analyzer (llm_analyzer.py)
• Sends text responses to Groq API
• Structured prompt → returns JSON
• JSON contains: qualitative_score, gaps[], recommendations[]
│
▼
Composite Score = (0.6 × quantitative) + (0.4 × qualitative)
│
▼
Overall Maturity Level (0-4, METI scale)
│
┌───────────┴───────────┐
▼                       ▼
Streamlit Display       PDF Generator (pdf_generator.py)
• Radar chart           • Cover page
• Score table           • Executive summary + radar chart
• Recommendations       • Per-dimension analysis (×5)
• Benchmark comparison
• 90-day roadmap
• Download button

## Session State (Streamlit)
```python
st.session_state = {
    "language": "en" | "pt" | "ja",
    "company_profile": dict,
    "current_dimension": int,   # 0-4
    "current_question": int,    # within dimension
    "responses": dict,          # all answers collected
    "analysis_result": dict,    # from LLM + scoring
    "pdf_bytes": bytes          # generated PDF
}
```

## LLM Prompt Strategy
- System prompt: sets role as academic DX researcher + JSON-only output rule
- User prompt: injects dimension name + text responses + company profile
- Output schema: enforced JSON with keys: qualitative_score, justification, gaps, recommendations
- Fallback: if JSON parsing fails → retry once → fallback to quantitative-only score

## PDF Structure (ReportLab)
1. Cover (logo placeholder, company name, date, framework citation)
2. Executive Summary (overall level, score table, radar chart)
3. Dimension Analysis ×5 (score, justification, gaps, recommendations)
4. SME Benchmark Comparison (bar chart vs METI 2022 averages)
5. 90-Day Action Roadmap (top 5 priority actions)
6. Methodology note (METI DX Promotion Index reference)