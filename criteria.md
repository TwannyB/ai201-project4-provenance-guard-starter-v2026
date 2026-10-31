# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.
For each trial run, out of the 10 paragraphs I wrote myself, at most 1 is labelled as high confidence AI.



**Why this target:**
I chose this target to ensure that false positives are held to a standard, and specifically chose at most 1 being labelled incorrectly as AI because I understand that it's difficult to be compleletely accurate when basing the classification on only stylometry and perplexity when humans can write text that's predictable in style and wording. I chose 9/10 to be the goal since a false accusation costs the writer a lot, and because commercial detectors seem to have a false positive rate between 1 and 10 percent. 


---

## 2.
For each trial, the average combined score of 5 texts I know are AI-generated is at least 0.45 higher than the average combined score of 5 texts I know a human wrote.



**Why this target:**
The unsure range is from 0.35 to 0.65, so a band of 0.45 is slightly larger. 0.45 means that on average, my known-AI texts and known-human texts land outside the unsure band and get a solid classification with about 0.075 to spare. A smaller gap would mean signals barely separate the two, and the label could be left up to chance.



---

## 3.

For each of three trials, I submit 5 texts and appeal each one using the `content_id` it returned. All 5 appeals return `200` with `status: "under_review"`, and `/log` shows a new `under_review` entry for each of those `content_id`s, with the original `decided` entry still in place. An appeal with a made-up `content_id` returns `404` and adds nothing to the log. (Tested by hand with curl — `run_eval.py` only calls `/submit`.)


**Why this target:**
It's really important for the user's appeal to be recognized by the system because it's the only way a wrongly accused writer can push back. An AI or a model isn't involved, so this should be something deterministic and not left up to chance.



---

## 4.

For each of three trials, all 6 malformed requests in my "bad input" scenario are refused with the status my contract in `README.md` gives them, and none returns a `500` or a label. The 6 are: empty `text`, whitespace-only `text`, no `text` field, `text` set to `null`, a two-word `text`, and a 50,000-word `text`. The oversized one gets `413`; the other five get `400`.


**Why this target:**
Each of the malformed request leaves nothing to evaluate properly, so the system should refuse it and tell the user what to fix rather than crash. This check doesn't involve the model, so it should hold for all 6 every time.

---

## 5.

For each of three trials, my "label coverage" scenario (3 known-AI texts, 3 known-human texts, 3 borderline texts) produces all three labels, and each label is reached by at least one text from its own group: a known-AI text gets "ai", a known-human text gets "human", and a borderline text gets "unsure".



**Why this target:**
A label that no text can produce is broken since the writer never sees it. Requiring the right group prevents the criterion from being reached when a wrong classification is given. The human label is most likely to be missing, since averaging pulls scores toward the middle.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
