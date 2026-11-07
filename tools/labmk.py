"""Config-lab episode helpers. from labmk import *"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from mk import story, flow, traps, recap, rc, S, F, V, T, TR, H, hook, LIME, CY, OR, RED, _j

def nsent(t): return len([x for x in re.split(r"(?<=[.?!])\s+", t.strip()) if x])

def INTRO(intro_text, objectives):
    """objectives = [(on_screen, spoken sentence)]"""
    n = nsent(intro_text)
    return dict(id="intro", type="labintro", narration=_j(intro_text, *[o[1] for o in objectives]),
                items=[dict(t=o[0], cue=n + i) for i, o in enumerate(objectives)])

def CLI(sid, device, intro, rows, heading=None, topology=None):
    """rows = [(spoken sentence, plain-English note, lines, opts)] ; lines are 'cmd' strings or dicts {c, p, d, out}.
    opts: dict(p=mode, hl=[substr], dev=device, clear=True, node=id)"""
    n = nsent(intro)
    steps = []
    for i, r in enumerate(rows):
        opts = r[3] if len(r) > 3 else {}
        st = dict(cue=n + i, note=r[1], lines=r[2])
        st.update(opts)
        steps.append(st)
    d = dict(id=sid, type="cli", device=device, heading=heading, narration=_j(intro, *[r[0] for r in rows]), steps=steps)
    if topology: d["topology"] = topology
    return d

def save_lab(topic, title, lab_title, lab_sub, kicker_name, part, parts, level, topology, scenes):
    d = dict(topic=topic, title=title, kicker=f"CONFIGURATION LAB · {kicker_name.upper()} · PART {part}", labTitle=lab_title, labSub=lab_sub,
             part=part, parts=parts, level=level, topology=topology, voice="af_heart", lang="en-us", speed=0.95, version="1.0", scenes=scenes)
    os.makedirs(f"topics/{topic}", exist_ok=True)
    json.dump(d, open(f"topics/{topic}/script.json", "w"), indent=1)

def check(topic):
    d = json.load(open(f"topics/{topic}/script.json"))
    bad = 0
    for sc in d["scenes"]:
        if sc["type"] == "cli":
            for st in sc["steps"]:
                for ln in st["lines"]:
                    ln = {"c": ln} if isinstance(ln, str) else ln
                    if len(ln["c"]) > 58: print("LONG CMD", topic, ln["c"]); bad += 1
                    for o in ln.get("out", []):
                        if len(o) > 72: print("LONG OUT", topic, len(o), o); bad += 1
                if len(st["note"]) > 150: print("LONG NOTE", topic, st["note"][:40]); bad += 1
    words = sum(len(s["narration"].split()) for s in d["scenes"])
    print(topic, "words", words, "~min", round(words / 150, 1), "OK" if not bad else "FIX")
    return bad
