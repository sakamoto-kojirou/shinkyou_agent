# shinkyou_agent（診鏡 Shinkyō Agent）

中小企業のデジタル変革成熟度を、METI DX推進指標に基づいて診断する研究向けエージェントです。

## できること

- 5つのDX成熟度観点に沿った構造化インタビュー
- METIの0〜4段階でのスコアリング
- レーダーチャートとPDF診断レポートの生成
- 英語・ポルトガル語（ブラジル）・日本語に対応

## 技術スタック

- Python 3.11+
- Streamlit
- Groq API
- ReportLab
- Matplotlib

## ディレクトリ構成

- `app.py` — Streamlitの起点
- `agent/` — フレームワーク、質問、スコアリング、LLM分析
- `report/` — レーダーチャートとPDF生成
- `data/` — ベンチマーク参照データ
- `tests/` — スコアリングのテスト

## ローカル実行

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## 補足

- 本プロジェクトは METI DX推進指標に準拠しています。
- ユーザー向け文字列は i18n 経由で管理します。
- デモ企業: TechBridge Ltda.（物流サービス、45名、ブラジル）
