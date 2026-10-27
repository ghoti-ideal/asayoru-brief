# 朝夜ブリーフ（インストールできるWebアプリ版）

`docs/` の中身を GitHub Pages で公開すると、Android の Chrome から「アプリをインストール」でホーム画面に追加できます。

## ファイル構成
- `docs/index.html` … アプリ本体（ニュースの表示）
- `docs/manifest.webmanifest` … アプリ名・アイコンなどの設定
- `docs/sw.js` … オフライン表示用（前回読み込んだ版を圏外でも表示）
- `docs/icons/` … アイコン
- `docs/data/index.json` … 版の一覧（新しい順、すべての版。過去の版の検索に使う見出しと要点を含む）
- `scripts/build_index.py` … 記事ファイルから `index.json` を作り直すスクリプト
- `docs/data/editions/<YYYY-MM-DD-am|pm>.json` … 各版の記事データ

## 更新の流れ
毎日 6:53 と 18:53（日本時間）の定期タスクが、新しい版の JSON を `docs/data/editions/` に追加し、
`python3 scripts/build_index.py` で `docs/data/index.json` を作り直してリポジトリに push します。GitHub Pages への反映には数分かかります。

## 記事データの形式
各記事は `region`（`domestic`=国内 / `international`=海外）と `cat`（`politics` / `economy` / `tech` / `science`）を持ちます。
`lead: true` の記事は見出し記事として図つきで大きく表示され、`visual`（`kicker`・`figure`・`unit`・`caption`）が図の文字になります。
