---
name: presentation-creator
description: Create a Marp-based presentation in Markdown format from user-provided structure and content, asking questions to unify the overall tone and style before generating the slides.
---

# プレゼン資料作成スキル

## 概要

このスキルは、ユーザーが提供したプレゼンの構成・内容をもとに、[Marp](https://marp.app/) を活用して Markdown 形式のプレゼン資料を作成するものである。

作成されるプレゼン資料は以下の要件を満たす。

- スライド全体のトンマナ（トーン＆マナー）が統一されている
- 各スライドの右下にフッター画像が表示される
- Marp で変換可能な Markdown 形式で出力される

## 基本方針

- ユーザーから提供された構成・内容を忠実に反映する
- トンマナの決定においては、ユーザーへの質問を通じて認識を合わせる
- スライドの内容は簡潔かつ視覚的に整理されたものにする
- 1 スライドに詰め込みすぎず、1 スライド 1 メッセージを心がける
- フッター画像はスキルの `assets` ディレクトリに格納されているものを使用する

## 注意点

- ユーザーの意図した内容を勝手に変更・削除しない
- トンマナの質問はまとめて一度に行い、ユーザーの負担を最小限にする
- フェーズは順番に実行する

## フェーズ構成

以下のフェーズを一つずつ順に実行する。

### フェーズ1: プレゼン構成・内容の収集

このフェーズでは、ユーザーからプレゼンの構成と内容を収集する。

ユーザーに以下を入力してもらう。

- プレゼンのタイトル
- スライドの構成（章・セクション・スライドの見出し一覧）
- 各スライドに載せたい内容（箇条書きや文章など、形式は問わない）

ユーザーが構成や内容を一部しか提供しない場合でも、そのまま次のフェーズに進む。
不足している部分はフェーズ3 のスライド生成時に適切に補完する。

### フェーズ2: トンマナの確認

このフェーズでは、プレゼン資料全体のトーン＆マナーを統一するために、以下の質問をまとめてユーザーに投げかける。

1. **対象オーディエンス**: プレゼンの聴衆は誰ですか？（例: 社内チーム、顧客、投資家、学術関係者など）
2. **スタイル**: プレゼンのスタイルはどのようなものを希望しますか？（例: フォーマル／カジュアル、技術的／ビジネス寄り）
3. **配色**: 使用する配色のイメージを教えてください。（例: コーポレートカラー指定、ダーク系、ライト系、特定の色）
4. **デザインテイスト**: デザインのテイストを教えてください。（例: シンプル・ミニマル、インパクト重視、クラシック・フォーマル）
5. **フォント雰囲気**: 文字のイメージを教えてください。（例: 細くスタイリッシュ、太くはっきり、手書き風）

ユーザーの回答を受け取ったら、すべての質問への回答が揃っているか確認し、次のフェーズに進む。
回答が「特になし」や「おまかせ」の場合は、プレゼン内容に適したデフォルトを採用する。

### フェーズ3: Marp Markdown スライドの生成

このフェーズでは、収集した構成・内容とトンマナをもとに、Marp 形式の Markdown スライドを生成する。

#### Marp フロントマターの設定

スライド冒頭の YAML フロントマターに以下を設定する。

```yaml
---
marp: true
theme: [フェーズ2 の回答に基づいて選択: default / gaia / uncover]
paginate: true
style: |
  section {
    font-family: [フェーズ2 の回答に基づいてフォントスタックを指定];
    background-color: [フェーズ2 の回答に基づいて背景色を指定];
    color: [フェーズ2 の回答に基づいてテキスト色を指定];
  }
  .footer-image {
    position: absolute;
    bottom: 20px;
    right: 20px;
    height: 36px;
    width: auto;
  }
---
```

#### スライド構成のルール

- タイトルスライドを必ず最初に置く
- スライドの区切りは `---` を使用する
- 各スライドの右下にフッター画像を表示するために、スライドの末尾（`---` の直前）に以下の HTML を挿入する

```html
<img src="./assets/footer.png" class="footer-image" alt="footer" />
```

- フッター画像のパスは、出力する Markdown ファイルと同じディレクトリを基準とした相対パスで記述する
- 出力 Markdown ファイルと同じ場所に `assets/footer.png` が存在するよう、スキルの `assets/footer.png` をコピーする

#### スライド内容のルール

- 各スライドのタイトルは `#` で記述する
- 本文は箇条書き（`-`）を基本とする
- 1 スライドの箇条書きは最大 5 項目程度に抑える
- コードを示す場合はコードブロックを使用する
- トンマナに合わせた絵文字の使用は任意とする

#### 出力例

```markdown
---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    background-color: #ffffff;
    color: #333333;
  }
  .footer-image {
    position: absolute;
    bottom: 20px;
    right: 20px;
    height: 36px;
    width: auto;
  }
---

# プレゼンタイトル

発表者名 / 日付

<img src="./assets/footer.png" class="footer-image" alt="footer" />

---

# アジェンダ

- トピック 1
- トピック 2
- トピック 3

<img src="./assets/footer.png" class="footer-image" alt="footer" />

---

# トピック 1

- ポイント A
- ポイント B
- ポイント C

<img src="./assets/footer.png" class="footer-image" alt="footer" />

---

# まとめ

- キーメッセージ 1
- キーメッセージ 2

<img src="./assets/footer.png" class="footer-image" alt="footer" />
```

### フェーズ4: ファイルの出力

このフェーズでは、生成した Marp Markdown をファイルとして出力する。

#### 出力先の決定

ユーザーに出力先のパスを尋ねる。指定がない場合はカレントディレクトリに出力する。

#### ファイル名のルール

- ファイル名はプレゼンのタイトルを元にスネークケースで作成する（例: `my_presentation.md`）
- ファイルの拡張子は `.md` とする

#### assets のコピー

出力先ディレクトリに `assets/` ディレクトリを作成し、このスキルの `assets/footer.png` をコピーする。

```
<出力先>/
├── <ファイル名>.md
└── assets/
    └── footer.png
```

#### 完了通知

ファイルの出力が完了したら、以下をユーザーに通知する。

- 出力した Markdown ファイルのパス
- `assets/footer.png` のコピー先パス
- Marp でスライドに変換するためのコマンド例

```bash
# Marp CLI を使用して HTML に変換する場合
npx @marp-team/marp-cli <ファイル名>.md --html

# PDF に変換する場合
npx @marp-team/marp-cli <ファイル名>.md --pdf
```
