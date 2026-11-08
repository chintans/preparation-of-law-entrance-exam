#!/usr/bin/env python3
"""Build the hook map and the current-affairs view from research/ca-items.json.

Usage:  python3 tools/hookmap.py --today YYYY-MM-DD

Reads   research/ca-items.json   (source of truth — edit this, never the generated files)
Writes  research/hook-map.md     (hook → items, test record, confusions, recall candidates)
        research/current-affairs.md (readable dated log, generated)

Item fields: id, logged (date briefed/taught), kind (brief|lesson|static), category, label,
topics [topic IDs], hooks ["Art 22", "BNSS 58", "Act: ...", "Body: ...", "Case: ...", ...],
fact, sources, tests [{date, q, result: right|wrong|blank|pending, chose?}].
"""
import argparse, datetime as dt, json, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "research" / "ca-items.json"
RESULTS = {"right", "wrong", "blank", "pending"}
KINDS = {"brief", "lesson", "static"}
MARK = {"right": "✓", "wrong": "✗", "blank": "–", "pending": "…"}


def load():
    d = json.loads(DATA.read_text())
    ids, errs = set(), []
    for it in d["items"]:
        for f in ("id", "logged", "kind", "label", "topics", "hooks", "fact", "tests"):
            if f not in it:
                errs.append(f"{it.get('id')}: missing {f}")
        if it["id"] in ids:
            errs.append(f"duplicate id {it['id']}")
        ids.add(it["id"])
        if it.get("kind") not in KINDS:
            errs.append(f"{it['id']}: bad kind {it.get('kind')}")
        for t in it.get("tests", []):
            if t.get("result") not in RESULTS:
                errs.append(f"{it['id']}: bad result {t}")
    if errs:
        sys.exit("ca-items.json invalid:\n  " + "\n  ".join(errs))
    return d["items"]


def hook_group(h):
    if h.startswith("Art ") or h == "Tenth Schedule":
        return "Constitution"
    if re.match(r"^(BNS|BNSS|BSA|IPC|CrPC|CPC) ", h):
        return "Code sections (old ↔ new)"
    return h.split(":")[0] + "s" if ":" in h else "Other"


def art_key(h):
    m = re.match(r"Art (\d+)([A-Z]*)", h)
    return (int(m.group(1)), m.group(2)) if m else (9999, h)


def record(it):
    return "".join(MARK[t["result"]] for t in it["tests"]) or "·"


def recall_candidates(items, today):
    """Briefed/taught ≥ 3 days ago; no pending test; never tested first, then last result wrong/blank."""
    out = []
    for it in items:
        if it["kind"] == "static":
            continue
        if (today - dt.date.fromisoformat(it["logged"])).days < 3:
            continue
        res = [t["result"] for t in it["tests"]]
        if "pending" in res:
            continue
        if not res:
            out.append((0, it["logged"], it))
        elif res[-1] in ("wrong", "blank"):
            out.append((1, it["logged"], it))
    return [x[2] for x in sorted(out, key=lambda x: (x[0], x[1]))]


def build_hookmap(items, today):
    by_hook = defaultdict(list)
    for it in items:
        for h in it["hooks"]:
            by_hook[h].append(it)
    groups = defaultdict(list)
    for h in by_hook:
        groups[hook_group(h)].append(h)
    L = [f"# Hook map", "",
         f"Generated {today} by `tools/hookmap.py` from `research/ca-items.json` — do not edit by hand.",
         "Record: ✓ right · ✗ wrong · – left blank · … awaiting answers · · never tested.", "",
         "Use: before writing a CA or polity question, look up its hook here — test a **neighbour** of a hook he has",
         "already got right, re-test hooks with ✗/–, and avoid items already tested twice running ✓.", ""]
    # recall candidates
    rc = recall_candidates(items, today)
    L += ["## Recall candidates (briefed ≥ 3 days ago, nothing pending)", "",
          "Never tested first (oldest first), then items whose last attempt was wrong or blank.", ""]
    for it in rc[:12]:
        L.append(f"- `{it['id']}` {it['label']} — {', '.join(it['topics'])} · {record(it)}")
    if not rc:
        L.append("- none")
    # confusions
    conf = [(it, t) for it in items for t in it["tests"] if t.get("chose")]
    L += ["", "## Confusions he has made (the wrong option he picked)", ""]
    for it, t in sorted(conf, key=lambda x: x[1]["date"]):
        L.append(f"- {t['date']} · {it['label']}: chose **{t['chose']}**")
    # hooks
    order = ["Constitution", "Code sections (old ↔ new)", "Acts", "Cases", "Bodys", "Persons",
             "Reports", "Treatys", "Events", "Doctrines", "Other"]
    for g in sorted(groups, key=lambda g: order.index(g) if g in order else 99):
        L += ["", f"## {g.replace('Bodys', 'Bodies').replace('Treatys', 'Treaties')}", "",
              "| Hook | Items (record) |", "|---|---|"]
        keyf = art_key if g == "Constitution" else (lambda h: h)
        for h in sorted(groups[g], key=keyf):
            cells = "; ".join(f"{it['label']} `{it['id']}` {record(it)}" for it in by_hook[h])
            L.append(f"| {h.split(': ', 1)[-1]} | {cells} |")
    # topic summary
    tally = defaultdict(lambda: [0, 0])
    for it in items:
        for t in it["tests"]:
            if t["result"] in ("right", "wrong", "blank"):
                for tp in it["topics"][:1]:
                    tally[tp][1] += 1
                    tally[tp][0] += t["result"] == "right"
    L += ["", "## Item-level record by topic (first topic only; blank counts as a miss)", ""]
    for tp, (r, n) in sorted(tally.items()):
        L.append(f"- {tp}: {r}/{n}")
    return "\n".join(L) + "\n"


def build_log(items):
    L = ["# Current-affairs log", "",
         "Generated by `tools/hookmap.py` from `research/ca-items.json` — **edit the JSON, not this file**.",
         "Newest first. Format: `logged (kind) · category · fact · sources` then the test record.", "",
         "CLAT/AILET 2027 window: roughly Nov 2025 – Nov 2026. NLSAT/CUET 2027: roughly Apr 2026 – Mar 2027.", ""]
    for it in sorted(items, key=lambda x: (x["logged"], x["id"]), reverse=True):
        L.append(f"{it['logged']} ({it['kind']}) · {it['category']} · {it['fact']} · {it.get('sources', '')}  ")
        tests = ", ".join(f"{t['date']} {t['q']} {MARK[t['result']]}" + (f" (chose {t['chose']})" if t.get("chose") else "")
                          for t in it["tests"])
        L.append(f"  `{it['id']}` · {', '.join(it['topics'])} · hooks: {', '.join(it['hooks']) or '—'}" +
                 (f" · tested: {tests}" if tests else " · not yet tested"))
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=dt.date.today().isoformat())
    a = ap.parse_args()
    today = dt.date.fromisoformat(a.today)
    items = load()
    (ROOT / "research" / "hook-map.md").write_text(build_hookmap(items, today))
    (ROOT / "research" / "current-affairs.md").write_text(build_log(items))
    print(f"{len(items)} items → research/hook-map.md, research/current-affairs.md")


if __name__ == "__main__":
    main()
