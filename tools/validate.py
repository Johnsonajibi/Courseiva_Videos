"""python3 -I tools/validate.py topics/<id>/script.json : checks cue indices against sentence counts."""
import json, re, sys
ok = True
s = json.load(open(sys.argv[1]))
for sc in s["scenes"]:
    n = len([x for x in re.split(r"(?<=[.?!])\s+", sc["narration"].strip()) if x])
    lists = [sc.get(k) for k in ("lines", "items", "steps", "rows", "points")]
    items = next((l for l in lists if l), [])
    cues = [i["cue"] for i in items]
    bad = [c for c in cues if c >= n or c < 0]
    if bad or cues != sorted(cues) or len(set(cues)) != len(cues):
        ok = False
        print("PROBLEM", sc["id"], "sentences:", n, "cues:", cues)
    if sc.get("ctaCue", 0) >= n:
        ok = False; print("PROBLEM ctaCue", sc["id"])
    words = len(sc["narration"].split())
    print(f'{sc["id"]:10s} {sc["type"]:9s} {n:2d} sentences {words:3d} words')
print("OK" if ok else "FIX NEEDED")
sys.exit(0 if ok else 1)
