"""Compact helpers to author topic scripts.  Usage (see tools/batches/*.py):
    from mk import *
    save("vlans", "VLANs", "Hotel floors", [hook(...), story(...), ...])
Narration rules: see docs/SCRIPT_GUIDE.md"""
import json, os, sys

def _items(rows, keys):
    return [dict(zip(keys, r)) for r in rows]

def hook(icon, lines, narration):
    return dict(id="hook", type="hook", icon=icon, narration=narration,
                lines=[dict(t=l[0], cue=l[1], **({"color": l[2]} if len(l) > 2 else {})) for l in lines])

def story(heading, narration, rows, id="story"):
    return dict(id=id, type="story", heading=heading, narration=narration, items=_items(rows, ["icon", "story", "real", "cue"]))

def flow(heading, narration, rows, id="flow"):
    return dict(id=id, type="flow", heading=heading, narration=narration, steps=_items(rows, ["icon", "title", "sub", "cue"]))

def versus(heading, left, right, narration, rows, id="versus"):
    return dict(id=id, type="versus", heading=heading, narration=narration,
                left=dict(title=left, color="#FB923C"), right=dict(title=right, color="#A3E635"),
                rows=_items(rows, ["label", "l", "r", "cue"]))

def term(heading, narration, rows, id="commands"):
    out = []
    for r in rows:
        d = dict(t=r[0], note=r[1], cue=r[2])
        if len(r) > 3: d["color"] = r[3]
        out.append(d)
    return dict(id=id, type="terminal", heading=heading, narration=narration, lines=out)

def traps(narration, rows, heading="Common mix-ups"):
    return dict(id="traps", type="traps", heading=heading, narration=narration, items=_items(rows, ["wrong", "right", "cue"]))

def recap(narration, rows, cta, cta_cue):
    return dict(id="recap", type="recap", heading="Remember this", cta=cta, ctaCue=cta_cue, narration=narration, points=_items(rows, ["t", "cue"]))

def save(topic, title, kicker_name, scenes):
    d = dict(topic=topic, title=f"{title}: The Complete Beginner's Guide", kicker=f"BEGINNER'S GUIDE · {kicker_name.upper()}",
             voice="af_heart", lang="en-us", speed=0.95, version="1.0", scenes=scenes)
    os.makedirs(f"topics/{topic}", exist_ok=True)
    json.dump(d, open(f"topics/{topic}/script.json", "w"), indent=1)

LIME, CY, OR, RED = "#A3E635", "#22D3EE", "#FB923C", "#F87171"

def rc(label, pts):
    """Standard recap. pts = [(spoken, on_screen)] x3 -> narration 'So, to recap. a. b. c. Ready to practise? Try the Courseiva <label> lab.'"""
    nar = "So, to recap. " + " ".join(p[0] for p in pts) + f" Ready to practise? Try the Courseiva {label} lab."
    return recap(nar, [(pts[i][1], i + 1) for i in range(len(pts))], f"Try the Courseiva {label} lab", len(pts) + 1)

# ---- auto-cue helpers: narration = intro + one sentence per row; cues assigned automatically ----
def _j(*s): return " ".join(x.strip() for x in s if x and x.strip())

def H(icon, items):
    """items=[(on_screen, sentence[, color])] -> 1 sentence per line (cue i)."""
    return hook(icon, [(it[0], i, *(it[2:])) for i, it in enumerate(items)], _j(*[it[1] for it in items]))

def S(heading, intro, rows):
    """rows=[(icon, sentence, story, real)] -> cue i+1."""
    return story(heading, _j(intro, *[r[1] for r in rows]), [(r[0], r[2], r[3], i + 1) for i, r in enumerate(rows)])

def F(heading, intro, rows):
    """rows=[(icon, sentence, title, sub)]"""
    return flow(heading, _j(intro, *[r[1] for r in rows]), [(r[0], r[2], r[3], i + 1) for i, r in enumerate(rows)])

def V(heading, left, right, intro, rows):
    """rows=[(label, l, r, sentence)]"""
    return versus(heading, left, right, _j(intro, *[r[3] for r in rows]), [(r[0], r[1], r[2], i + 1) for i, r in enumerate(rows)])

def T(heading, intro, rows):
    """rows=[(code, note, sentence[, color])]"""
    return term(heading, _j(intro, *[r[2] for r in rows]), [(r[0], r[1], i + 1, *(r[3:])) for i, r in enumerate(rows)])

def TR(intro, rows):
    """rows=[(wrong, right, sentence)]"""
    return traps(_j(intro, *[r[2] for r in rows]), [(r[0], r[1], i + 1) for i, r in enumerate(rows)])
