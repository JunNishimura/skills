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
- `assets/style.css` を Markdown から参照する運用のため、VSCode では出力ディレクトリをワークスペースとして開く前提で進める

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
3. **配色**: 使用する配色のイメージを教えてください。（例: コーポレートカラー指定、ダーク系、ライト系、特定の色、Color Hunt のURL）
4. **デザインテイスト**: デザインのテイストを教えてください。（例: シンプル・ミニマル、インパクト重視、クラシック・フォーマル）
5. **フォント雰囲気**: 文字のイメージを教えてください。（例: 細くスタイリッシュ、太くはっきり、手書き風）

ユーザーの回答を受け取ったら、すべての質問への回答が揃っているか確認し、次のフェーズに進む。
回答が「特になし」や「おまかせ」の場合は、プレゼン内容に適したデフォルトを採用する。

配色について Color Hunt のURL（`https://colorhunt.co/...`）が指定された場合は、そのURLに含まれるパレットを優先して採用する。
URLパスに16進カラーコードが含まれる場合（例: `/palette/222831393e4600adb5eeeeee`）は、そこから `#222831`, `#393e46`, `#00adb5`, `#eeeeee` のように抽出して使用する。
抽出したカラーは、可読性を確保しつつ背景色・文字色・強調色に割り当てる。

### フェーズ3: Marp Markdown スライドの生成

このフェーズでは、収集した構成・内容とトンマナをもとに、Marp 形式の Markdown スライドを生成する。

#### Marp フロントマターの設定

スライド冒頭の YAML フロントマターに以下を設定する。

```yaml
---
marp: true
theme: [フェーズ2 の回答に基づくテーマ名（例: custom）]
paginate: true
---
```

スタイル定義（フォント、背景色、文字色、`.footer-image` など）は Markdown ファイルに直接書かず、`assets/style.css` に記述する。
`assets/style.css` は Marp のカスタムテーマとして作成し、先頭に `/* @theme custom */` のようなテーマ宣言を入れる。

Color Hunt のURLが指定されている場合は、`assets/style.css` 内の `background-color` と `color` を抽出した配色から決定する。
明るい背景には暗い文字色、暗い背景には明るい文字色を選び、必要に応じて強調色も同じパレットから使う。

`assets/style.css` の例:

```css
/* @theme custom */

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
- 図解・比較・時系列・プロセス説明など、画像があると理解しやすい箇所は画像を入れる前提でスライドを設計する
- 画像を入れる想定の箇所には、画像挿入位置の近くに Markdown コメントを残す
- コメントには「どんな画像か」「必要な特徴（テイスト、被写体、構図、色味、雰囲気など）」を具体的に書く
- コメントの形式は以下を推奨する

```markdown
<!-- 画像案: [用途/意図]。画像イメージ: [被写体やシーン]。特徴: [テイスト・色味・構図・雰囲気]。 -->
```

#### 出力例

```markdown
---
marp: true
theme: custom
paginate: true
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

<!-- 画像案: 施策の全体像を直感的に示す。画像イメージ: プロセスを3段階で示したシンプルな概念図。特徴: フラットデザイン、余白多め、配色はスライドのアクセントカラーに合わせる。 -->

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
出力後は、その出力ディレクトリを VSCode でワークスペースとして開く前提とする。

#### ファイル名のルール

- ファイル名はプレゼンのタイトルを元にスネークケースで作成する（例: `my_presentation.md`）
- ファイルの拡張子は `.md` とする

#### assets のコピー

出力先ディレクトリに `assets/` ディレクトリを作成し、このスキルの `assets/footer.png` をコピーする。
また、スライドに対応する `assets/style.css` を作成し、トンマナ（配色・フォントなど）を記述する。
さらに、出力先ディレクトリに VSCode ワークスペース設定ファイル（拡張子 `.code-workspace`）を作成し、`markdown.marp.themes` に `./assets/style.css` を設定する。

```
<出力先>/
├── <ファイル名>.md
├── <任意の名前>.code-workspace
└── assets/
    ├── style.css
    └── footer.png
```

`.code-workspace` ファイル内容の例:

```json
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "markdown.marp.themes": ["./assets/style.css"]
  }
}
```

#### 完了通知

ファイルの出力が完了したら、以下をユーザーに通知する。

- 出力した Markdown ファイルのパス
- 出力した `.code-workspace` ファイルのパス
- `assets/footer.png` のコピー先パス
- `assets/style.css` の出力先パス
- VSCode で出力ディレクトリをワークスペースとして開く案内
- Marp でスライドに変換するためのコマンド例

```bash
# Marp CLI を使用して HTML に変換する場合
npx @marp-team/marp-cli <ファイル名>.md --html --theme-set ./assets/style.css

# PDF に変換する場合
npx @marp-team/marp-cli <ファイル名>.md --pdf --theme-set ./assets/style.css
```
