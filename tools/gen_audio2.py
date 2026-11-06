"""Natural narration: synthesize each scene in ONE pass (better prosody), then
recover per-sentence cue times by snapping estimated boundaries to real pauses.
usage: python3 -I tools/gen_audio2.py topics/<topic>"""
import json, os, re, sys
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

LEAD, TAIL, FPS = 0.5, 0.9, 30
d = sys.argv[1]
script = json.load(open(os.path.join(d, "script.json")))
os.makedirs(os.path.join(d, "audio"), exist_ok=True)
k = Kokoro("tts-models/kokoro-v1.0.onnx", "tts-models/voices-v1.0.bin")
kw = dict(voice=script["voice"], speed=script.get("speed", 1.0), lang=script["lang"])

def pauses(x, sr, min_len=0.12):
    hop = int(sr * 0.01)
    n = len(x) // hop
    rms = np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1))
    quiet = rms < max(0.015, rms.max() * 0.04)
    runs, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if (j - i) * 0.01 >= min_len:
                runs.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    return runs

timing = {"fps": FPS, "lead": LEAD, "tail": TAIL, "scenes": []}
start = 0
for sc in script["scenes"]:
    text = sc["narration"].strip()
    sents = [s for s in re.split(r"(?<=[.?!])\s+", text) if s]
    full, sr = k.create(text, **kw)
    # trim edge silence
    nz = np.where(np.abs(full) > 0.01)[0]
    full = full[nz[0] : nz[-1] + 1]
    total = len(full) / sr
    # proportional estimate from per-sentence synthesis
    lens = [len(k.create(s, **kw)[0]) for s in sents]
    cum = np.cumsum(lens) / sum(lens) * total
    runs = pauses(full, sr)
    used, bounds = set(), []  # (speech_end, next_speech_start)
    for i in range(len(sents) - 1):
        best, bd = None, 1.0
        for ri, (a, b) in enumerate(runs):
            if ri in used:
                continue
            dd = abs((a + b) / 2 - cum[i])
            if dd < bd:
                best, bd = ri, dd
        if best is not None:
            used.add(best)
            bounds.append(runs[best])
        else:
            bounds.append((cum[i], cum[i]))
    bounds.sort()
    cues, s_t = [], 0.0
    for i, s in enumerate(sents):
        e_t = bounds[i][0] if i < len(bounds) else total
        cues.append({"text": s, "start": round(LEAD + s_t, 3), "end": round(LEAD + e_t, 3)})
        s_t = bounds[i][1] if i < len(bounds) else total
    samples = np.concatenate([np.zeros(int(LEAD * sr)), full, np.zeros(int(TAIL * sr))]).astype(np.float32)
    sf.write(os.path.join(d, "audio", sc["id"] + ".wav"), samples, sr)
    dur = len(samples) / sr
    frames = int(round(dur * FPS))
    timing["scenes"].append({"id": sc["id"], "voiceSeconds": round(total, 3), "seconds": round(dur, 3), "frames": frames,
                             "startFrame": start, "audio": "audio/" + sc["id"] + ".wav", "cues": cues})
    start += frames
    print(sc["id"], round(total, 1), "s", frames, "frames", [round(c["start"], 1) for c in cues], flush=True)
timing["totalFrames"] = start
timing["totalSeconds"] = round(start / FPS, 2)
json.dump(timing, open(os.path.join(d, "timing.json"), "w"), indent=2)
print("TOTAL", timing["totalSeconds"])
