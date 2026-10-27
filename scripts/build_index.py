"""docs/data/editions/*.json から docs/data/index.json を作り直す。

index.json は版の一覧（新しい順）で、過去の版の検索に使う見出しと要点も含む。
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ED_DIR = ROOT / "docs" / "data" / "editions"
OUT = ROOT / "docs" / "data" / "index.json"

REGIONS = {"domestic", "international"}
CATS = {"politics", "economy", "tech", "science"}


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


def main():
    entries, problems = [], []
    for f in sorted(ED_DIR.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        errs = check(f.stem, d)
        if errs:
            problems.append(f"{f.name}: " + " / ".join(errs))
            continue
        entries.append({
            "id": f.stem,
            "date": d["date"],
            "slot": d["slot"],
            "key": d["key"],
            "brief": d.get("brief", []),
            "titles": [it.get("title", "") for it in d["items"]],
        })
    entries.sort(key=lambda e: e["key"], reverse=True)
    OUT.write_text(json.dumps({"editions": entries}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"index.json: {len(entries)} 版")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
