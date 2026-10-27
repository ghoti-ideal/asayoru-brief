"""docs/data/editions/*.json から docs/data/index.json を作り直す。

index.json は版の一覧（新しい順）で、過去の版の検索に使う見出しと要点も含む。
`--check <版のID>` を付けると、その版の記事の偏り（国内外の件数、分野の数、出典の集中）も検査する。
"""
import json
import pathlib
import sys
from collections import Counter
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
ED_DIR = ROOT / "docs" / "data" / "editions"
OUT = ROOT / "docs" / "data" / "index.json"

REGIONS = {"domestic", "international"}
CATS = {"politics", "economy", "society", "tech", "science", "health", "environment"}

# 偏りの検査の基準
MIN_PER_REGION = 6       # 国内・海外それぞれの最低件数
MAX_REGION_GAP = 2       # 国内と海外の件数の差
MIN_CATS = 5             # 版全体で使う分野の数
MIN_HOSTS = 8            # 出典の媒体（ドメイン）の数
MAX_ITEMS_PER_HOST = 3   # 1つの媒体を出典にできる記事数



def check(eid, d):
    errs = []
    for k in ("date", "slot", "key", "generatedAt", "items"):
        if k not in d:
            errs.append(f"{k} がありません")
    if d.get("slot") not in ("am", "pm"):
        errs.append("slot は am か pm")
    if eid != f"{d.get('date')}-{d.get('slot')}":
        errs.append("ファイル名と date/slot が一致しません")
    # 旧形式（region なし）の版は検査しない
    if all("region" in it for it in d.get("items", [])):
        for i, it in enumerate(d["items"]):
            if it.get("region") not in REGIONS:
                errs.append(f"items[{i}].region が不正")
            if it.get("cat") not in CATS:
                errs.append(f"items[{i}].cat が不正")
            if not it.get("title"):
                errs.append(f"items[{i}].title がありません")
    return errs


def host(url):
    h = (urlparse(url).hostname or "").lower()
    return h[4:] if h.startswith("www.") else h


def check_balance(d):
    errs = []
    items = d.get("items", [])
    n = Counter(it.get("region") for it in items)
    dom, intl = n["domestic"], n["international"]
    if dom < MIN_PER_REGION or intl < MIN_PER_REGION:
        errs.append(f"国内{dom}件・海外{intl}件（それぞれ{MIN_PER_REGION}件以上必要）")
    if abs(dom - intl) > MAX_REGION_GAP:
        errs.append(f"国内と海外の件数の差が{abs(dom - intl)}件（{MAX_REGION_GAP}件以内にする）")
    cats = {it.get("cat") for it in items}
    if len(cats) < MIN_CATS:
        errs.append(f"分野が{len(cats)}種類（{MIN_CATS}種類以上にする）")
    per_host = Counter()
    for i, it in enumerate(items):
        hs = {host(s.get("url", "")) for s in it.get("sources", []) if s.get("url")}
        if not hs:
            errs.append(f"items[{i}] に出典がありません")
        per_host.update(hs)
    if len(per_host) < MIN_HOSTS:
        errs.append(f"出典の媒体が{len(per_host)}種類（{MIN_HOSTS}種類以上にする）")
    for h, c in per_host.items():
        if c > MAX_ITEMS_PER_HOST:
            errs.append(f"{h} を出典にした記事が{c}件（{MAX_ITEMS_PER_HOST}件以内にする）")
    for r in ("domestic", "international"):
        leads = [it for it in items if it.get("region") == r and it.get("lead")]
        if not 1 <= len(leads) <= 2:
            errs.append(f"{r} の lead が{len(leads)}件（1〜2件にする）")
        if any(not (it.get("visual") or {}).get("figure") for it in leads):
            errs.append(f"{r} の lead に visual.figure がありません")
    return errs


def main():
    target = None
    if len(sys.argv) == 3 and sys.argv[1] == "--check":
        target = sys.argv[2]
    elif len(sys.argv) != 1:
        sys.exit("使い方: build_index.py [--check <版のID>]")
    entries, problems = [], []
    for f in sorted(ED_DIR.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        errs = check(f.stem, d)
        if errs:
            problems.append(f"{f.name}: " + " / ".join(errs))
            continue
        # 偏りは報告するが、版は一覧に残す
        if f.stem == target:
            bal = check_balance(d)
            if bal:
                problems.append(f"{f.name}（偏り）: " + " / ".join(bal))
        entries.append({
            "id": f.stem,
            "date": d["date"],
            "slot": d["slot"],
            "key": d["key"],
            "brief": d.get("brief", []),
            "titles": [it.get("title", "") for it in d["items"]],
        })
    if target and not (ED_DIR / f"{target}.json").exists():
        problems.append(f"{target}.json がありません")
    entries.sort(key=lambda e: e["key"], reverse=True)
    OUT.write_text(json.dumps({"editions": entries}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"index.json: {len(entries)} 版")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
