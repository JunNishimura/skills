# Agent Skills

このリポジトリは、Codex で利用するスキル（`SKILL.md` ベースの手順集）を管理するためのものです。  
主に「日次振り返り支援」と「定期振り返りレポート作成」の2つの実用スキルを収録しています。

## 含まれるスキル

- `daily-reflection`  
  コルブの経験学習モデルに沿って、日々の振り返りを段階的に深めるスキル。
- `periodic-reflection-report`  
  Notion 上の振り返り記録を集約し、指定期間の振り返りレポートを生成するスキル。

## ディレクトリ構成

```text
.
├── daily-reflection/
│   └── SKILL.md
├── periodic-reflection-report/
│   └── SKILL.md
└── README.md
```

## 補足

- 振り返り系スキルは Notion MCP 連携を前提にした手順を含みます。
- 想定される主な環境変数:
  - `DAILY_REFLECTION_DB_URL`
  - `PERIODIC_REFLECTION_PAGE_ID`
