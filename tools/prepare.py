"""python3 -I tools/prepare.py <topic_id>: generate audio+timing, copy audio to public/, write props.json"""
import json, os, shutil, subprocess, sys
t = sys.argv[1]
d = f"topics/{t}"
subprocess.run([sys.executable, "-I", "tools/gen_audio2.py", d], check=True)
dst = f"public/{t}/audio"
shutil.rmtree(dst, ignore_errors=True)
os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copytree(f"{d}/audio", dst)
json.dump({"script": json.load(open(f"{d}/script.json")), "timing": json.load(open(f"{d}/timing.json"))}, open(f"{d}/props.json", "w"))
print("ready", t)
