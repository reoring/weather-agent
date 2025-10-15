## 目的と構成
- **目的**: Assistants API 依存のサンプルを、移行先の **Responses API** に対応させ、最小構成で実行・拡張できる形にする。
- **構成**: `OpenAIResponsesClient` + 単一設定引数（`AppConfig` 内に `ModelConfig` を内包）。実行は `uv`、エントリは console script。

## Assistants API → Responses API 移行ポイント
- 背景: Assistants API は移行フェーズ。Responses API へ置換。
- 差し替え: `OpenAIAssistantsClient` → `OpenAIResponsesClient`。
- モデル指定: `OPENAI_RESPONSES_MODEL_ID` を優先。なければ `OPENAI_CHAT_MODEL_ID`、最後に既定。
- ストリーミング: `agent.run_stream(...)` はそのまま利用可（Responses でも text を逐次表示）。
- 注意: Assistants 専用・非対応モデルがあり、`unsupported_model` が出た場合はモデルを見直す。

## Reasoning Effort の設定
- 指定方法: `additional_chat_options={"reasoning": {"effort": "low|medium|high", "summary": "concise|detailed"}}`。
- 実装: `ModelConfig.build_additional_chat_options()` が常に `effort` を含め、`summary` は設定時のみ追加。
- 既定: `reasoning_effort` は **low** をデフォルト（Enum で型安全に管理）。
- 環境変数: `OPENAI_REASONING_EFFORT`, `OPENAI_REASONING_SUMMARY` を Enum にマップ（無効値は無視）。
- 参考: `https://platform.openai.com/docs/api-reference/responses/create#responses-create-reasoning`

## 設定オブジェクト設計
- 単一引数に集約: `non_streaming_example(config: AppConfig)`, `streaming_example(config: AppConfig)`。
- 責務分離:
  - `ModelConfig.resolve_model_id()` でモデル名を解決（env → 既定）。
  - `AppConfig.resolve_api_key()` で API Key を解決。
  - `ModelConfig.build_additional_chat_options()` で provider 固有の追加オプションを生成。
- Enum: `ReasoningEffort(low/medium/high)`, `ReasoningSummary(concise/detailed)` を導入し、型安全性とデフォルト管理を強化。

## 実行・パッケージング（uv）
- コンソールスクリプト: `pyproject.toml` の `[project.scripts]` で `weather-agent` を登録。
- 実行: `uv sync` → `uv run weather-agent`。
- ヒント: `package=true`（uv）が未設定だと console script が生成されず `Failed to spawn` になる。

## 環境変数・.env
- 必須: `OPENAI_API_KEY`、（推奨）`OPENAI_RESPONSES_MODEL_ID`。
- 代替: `OPENAI_CHAT_MODEL_ID`（Responses モデル未指定のときのフォールバック）。
- 追加: `OPENAI_REASONING_EFFORT`, `OPENAI_REASONING_SUMMARY`, `ENV_FILE_PATH`（任意）。

## VS Code / Pyright の未解決インポート対応
- 症状: 実行は可能だが `Import "agent_framework.openai" could not be resolved` 警告。
- 対処:
  - エディタの Python インタプリタをプロジェクトの `.venv` に固定。
  - `pyproject.toml` に `[tool.pyright]` を追加（`venvPath`, `venv`）。
  - `.vscode/settings.json` で `python.defaultInterpreterPath` を `.venv/bin/python` に、`python.analysis.extraPaths` にローカルの `agent-framework-core` を追加。

## よくある落とし穴
- モデル非対応: Assistants/Responses で使用可能モデルが異なる。`unsupported_model` が出たらモデルを見直す。
- 環境の不一致: VS Code とターミナルで別 venv を参照していると型解析だけ失敗する。インタプリタを合わせる。
- console script 未生成: `package=true` を忘れると `uv run weather-agent` が失敗。

## 次の拡張アイデア
- CLI 引数: `--model-id`, `--reasoning-effort` 等で `AppConfig` を上書き生成。
- Structured Output: `response_format` を使った Pydantic モデルの構造化出力デモ追加。
- E2E テスト: サンプルの smoke test（env があるときのみ実行）を用意。
- ドキュメント: モデル対応表とトラブルシュート表を README に追記。

## 参考リンク
- `https://platform.openai.com/docs/assistants/migration`
- `https://platform.openai.com/docs/api-reference/responses/create#responses-create-reasoning`

