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
各記事は `region`（`domestic`=国内 / `international`=海外）と `cat`（`politics` / `economy` / `society` / `tech` / `science` / `health` / `environment`）を持ちます。
`lead: true` の記事は見出し記事として図つきで大きく表示され、`visual`（`kicker`・`figure`・`unit`・`caption`）が図の文字になります。

## 偏りの検査
`python3 scripts/build_index.py --check <版のID>` は、その版について次を検査します（基準はスクリプト冒頭の定数）。
国内・海外それぞれ6件以上で差は2件以内、分野は5種類以上、出典の媒体は8種類以上、1つの媒体を出典にする記事は3件以内、国内・海外それぞれに図つきの見出し記事が1〜2件。

---

# きざみ（マイクロスケジュール）

`docs/schedule/` にある、5分単位で一日を組み立てるスケジュール帳です。公開後は `https://ghoti-ideal.github.io/asayoru-brief/schedule/` で開け、スマホ・PCとも「アプリをインストール」/「ホーム画面に追加」で入れられます。

## ファイル構成
- `docs/schedule/index.html` … アプリ本体（データは端末の localStorage に `kizami:` で始まる名前で保存）
- `docs/schedule/manifest.webmanifest`・`docs/schedule/sw.js` … インストールとオフライン表示
- `docs/schedule/icons/` … アイコン（`python3 scripts/make_schedule_icons.py` で作り直せます）

## できること
- すばやく追加: 「資料作成 25」→次の空き時間に25分。「10:30 会議 60」「13:00-13:45 移動」も可
- タイムライン: タップ/ドラッグで追加、PCはドラッグ・スマホは長押しで移動、下端で長さ変更。刻みは1/5/10/15分
- いまの予定: 残り時間、完了（早く終わったら後ろを詰める）、延長・遅れの反映（後ろの予定を空き時間まで押し出す。「固定」の予定は動かさない）
- やること（時間未定の用事）を空き時間へ入れる、型（いつもの流れ）の保存と適用、週ビュー
- Googleカレンダーの .ics 取り込み・.ics 書き出し・JSONバックアップ
- スマホとPCの同期: GitHub の非公開 Gist（`gist` 権限のトークン）を同期先にする。項目ごとに新しい変更を残す
- 通知はアプリを開いている間だけ（サーバーを使わないため）
