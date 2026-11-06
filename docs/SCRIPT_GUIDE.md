# Script guide

Goal: a complete beginner (or someone confused by other materials) understands the topic from ONE everyday analogy,
then learns the real terms and the exam-relevant facts. Friendly, spoken, no jargon before the idea makes sense.

* Length: 5-7 scenes, 250-340 spoken words (about 1:45-2:15).
* Scene order: `hook` -> `story` (the analogy mapped to real terms) -> 1-3 of `flow` (steps), `versus` (two things compared),
  `terminal` (commands/formulas) -> `traps` (3 mix-ups, wrong vs right) -> `recap` (3 points + call to action).
* Use the chapter's own analogy (`analogy_title`/`analogy_body`) when it is sound; simplify it.
* Facts must come from the chapter (key_takeaways, misconceptions, step_by_step). Never invent numbers or commands.
* Narration is spoken by TTS: conversational, contractions ("you'll", "it's"), short sentences. Spell acronyms with
  spaces ("V L A N", "O S P F", "D H C P"); the caption collapses them. Say numbers/symbols in words ("slash twenty-six",
  "eight oh two dot one Q"). Avoid abbreviations with full stops (e.g.), decimals and IP addresses inside narration.
* Sentences are split on `. ? !` -> each item's `cue` is the index of the sentence that should trigger it. Cues must be
  strictly increasing and < number of sentences. Colons/commas do not split. Run `python3 -I tools/validate.py topics/<id>/script.json`.
* On-screen text is short (story/real <= ~30 chars, step titles <= ~16 chars, sub <= ~40, traps sentences <= ~60).
* Icons: person people building key envelope book door clock lock laptop server router switch cloud mic scale ruler map
  bell shield gear list box wifi link wrench question tree road stamp.
* End the recap with `cta` like "Try the Courseiva <topic> lab" and ctaCue = the sentence "Try the Courseiva ... lab."
* Author with `tools/mk.py` helpers (see `tools/batches/`).
