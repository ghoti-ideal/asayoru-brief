# 朝夜ブリーフ（インストールできるWebアプリ版）

`docs/` の中身を GitHub Pages で公開すると、Android の Chrome から「アプリをインストール」でホーム画面に追加できます。

## ファイル構成
- `docs/index.html` … アプリ本体（ニュースの表示）
- `docs/manifest.webmanifest` … アプリ名・アイコンなどの設定
- `docs/sw.js` … オフライン表示用（前回読み込んだ版を圏外でも表示）
- `docs/icons/` … アイコン
- `docs/data/index.json` … 版の一覧（新しい順、最大28件）
- `docs/data/editions/<YYYY-MM-DD-am|pm>.json` … 各版の記事データ

## 更新の流れ
毎日 6:53 と 18:53（日本時間）の定期タスクが、新しい版の JSON を `docs/data/editions/` に追加し、
`docs/data/index.json` を書き換えてリポジトリに push します。GitHub Pages への反映には数分かかります。
