# Courseiva Videos

Beginner-friendly explainer videos for Courseiva's networking chapters. One video per topic, each built from a
`topics/<topic-id>/script.json` (narration + on-screen items) rendered with Remotion; narration is synthesised with
Kokoro (voice `af_heart`).

## Add or change a video
1. Create `topics/<topic-id>/script.json` (see `topics/dhcp-process/script.json`). Scene types: `hook`, `story`,
   `flow`, `versus`, `terminal`, `traps`, `recap`. Each on-screen item has a `cue` = index of the narration sentence
   that triggers it. Spell acronyms with spaces for the voice (`D H C P`); captions collapse them automatically.
2. `python3 -I tools/validate.py topics/<topic-id>/script.json`
3. Push to `main`. The **Render videos** workflow renders the changed topics; download the `.mp4` from the run's
   artifacts. Run it manually (Actions tab) with `all` to render everything.

## Local render
```bash
pip install -r requirements.txt && tools/fetch_models.sh && npm ci
python3 -I tools/prepare.py dhcp-process
npx remotion render src/index.ts Topic out/dhcp-process.mp4 --props=topics/dhcp-process/props.json
```
