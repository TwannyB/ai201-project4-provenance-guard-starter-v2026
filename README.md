# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. The user sends the text with a post request to /submit route.
2. The submit route reads the JSON it received, pulls out `text` and `creator_id`, and rejects bad input. It then creates a `content_id` uuid.
3. GPT-2 reads the text and measures the perplexity, meaning how unexpected each next word is. **Blind spot: it measures predictability, not authorship, so plain writing in common words can score as AI**
4. stylometry.style_signal measures how much sentence length varies, how varied the vocabulary the is, and how much punctuation there is, but it also doesn't understand text. It adds a `style_score`, which is between 0 and 1, with higher scores meaning that the text is more AI like. **Blind spot: it can't read, so typos or a pasted quote can move the score when they shouldn't** 
5. scoring.combine_signals merges the two scores(perplexity and style score), into one(takes weighted average) and adds it as the  `combined_score`. Here we decide what happens when two signals disagree. 
6. scoring.score_to_label compares the score to the thresholds(0.35 -> human, above 0.65 -> AI, in between -> unsure). It adds a short `guess` and the plain English label sentence.
7. audit.log_decision writes the content_id, creator_id, both signal scores, the combined score, guess, label, and status to logs/audit.jsonl. It then returns those fields to the caller, and the reader sees the label. This adds the permanent record. If the writer appeals, a second entry with `under_review` is added to the first one without anything being overwritten. 

### The contract

<!-- What goes in and what comes out of each endpoint, field by field.
     Fill in every ___ before building. Test: could someone build against
     this without asking me a question? -->

All bodies are JSON. Every error response has the same shape:
`{"error": "<code>", "message": "<readable explanation>"}`.

#### `POST /submit`

**Request**

| Field | Type | Required | Meaning |
|---|---|---|---|
| `text` | string | yes | The writing to check |
| `creator_id` | string | yes | Who is submitting it |

**Response `200`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string (uuid) | ID for this submission. Needed to appeal |
| `guess` | `"human"` / `"unsure"` / `"ai"` | Machine-readable verdict, exactly one of these lowercase strings |
| `confidence` | float 0–1 | How sure the system is: how far `combined_score` is from 0.5, scaled to 0–1 (0 = no idea, 1 = very sure, either way) |
| `label` | string | The plain-English sentence the writer sees |
| `model_score` | float 0–1 | Signal one. Higher = more AI-like |
| `style_score` | float 0–1 | Signal two. Higher = more AI-like |
| `combined_score` | float 0–1 | The combined score the label was picked from |

**Errors**

| Case | Status | `error` |
|---|---|---|
| Body isn't JSON, or `text` / `creator_id` missing or not a string | `400` | `bad_request` |
| `text` empty or too short to score (fewer than 5 words) | `400` | `text_too_short` |
| `text` longer than 10,000 characters | `413` | `text_too_long` |
| Too many requests (unit 8) | `429` | `rate_limited` |

#### `POST /appeal`

**Request**

| Field | Type | Required | Meaning |
|---|---|---|---|
| `content_id` | string | yes | From the `/submit` response |
| `reasoning` | string | yes | Why the writer thinks the label is wrong |

`creator_id` is not needed: it's copied from the original decision in the log, so nobody can appeal under someone else's name.

**Response `200`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Echoed back |
| `status` | `"under_review"` | The item's new status |
| `message` | string | A confirmation the writer can read |

**Errors**

| Case | Status | `error` |
|---|---|---|
| `content_id` or `reasoning` missing or empty | `400` | `bad_request` |
| `content_id` not in the log | `404` | `not_found` |
| Item already under review (nothing new is logged) | `409` | `already_under_review` |



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
It measures how unpredictable or predictable a sequence of words is, also known as the perplexity. 

**Why that might differ between human and AI writing:**
Humans tend to have higher perplexity scores than AI when writing because humans are less predictable than AI.

**What it can't see:**
It might wrongly classify predictable writing, since it has a lower perplexity score, as AI written, even if it's written by a human who happens to write predictably. That could include a new speaker or writer to the language or a younger writer. The reverse could also happen with more unpredictable writing being classified as human even when it originated from AI because it has a unique sequence of words. In short, the score can't see authorship.

### Signal two — the style signal

**What it measures:**
It measures the shape of the input text and specific traits within the text. The style score averages the spread score (how much sentence lengths vary) and the punctuation score (commas, semicolons, colons, dashes, brackets, ! and ? per word), excluding the TTR from the calculation altogether. This is because the TTR scores didn't seem to separate AI from human text well when running tests (0.87–0.91 on all three of my calibration texts). Each measure is scaled to 0–1 using anchors from my calibration texts: spread 0.60 reads fully human and 0.25 fully AI; punctuation 0.04 reads fully human and 0.12 fully AI.


**Why that might differ between human and AI writing:**
AI writing tends to have even, mid-length sentences, while human writing tends to be less consistent. My tests backed this up for spread: both AI texts had low spread (0.24, 0.33) and my casual and plain human texts had high spread (0.61, 0.56). My formal essay sat in between (0.36), so polished human writing looks more even too. Punctuation didn't hold up the way I expected. My first AI paragraph used far more punctuation than my human texts (0.114 against 0.046), so I set it up as "more punctuation reads AI". But on more texts, the other two AI samples used about as little punctuation as my human writing (0.043–0.048 against 0.036–0.057), so punctuation doesn't actually separate them.

**What it can't see:**
The signal can't read, and doesn't pull any semantic knowledge from the text. Anything that changes the shape, like adding typos, breaking up sentences, or pasting a quotation can change the score.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**
Each signal reads text as 'human' when it's below 0.5. If either signal reads human, the combined score is capped at 0.64, which is under the AI threshold so that the result can be unsure but never AI. If both read AI, then the combined score is their average.

**The numbers:**
The two signals both have a line of separation at 0.5, with below it being read as "human" and scores at 0.5 and above being read as "AI". If either signal lands in "human", the combined score is capped at 0.64 (a cap only: a lower score stays where it is). If both read AI, the combined score is a plain average, weighted 0.5 model and 0.5 style. On the combined score, 0.35 or below is labelled human, 0.65 or above is labelled AI, and anything between is unsure. All of these live in `config.py`: `SIGNAL_HUMAN_LINE`, `DISAGREEMENT_CAP`, `WEIGHT_MODEL_SIGNAL`, `WEIGHT_STYLE_SIGNAL`, `HUMAN_THRESHOLD` and `AI_THRESHOLD`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**
My in-between text, a plain paragraph a person wrote, split my signals. The model signal scored it 0.77 since the model found its wording predictable, making it read as AI. The style signal scored it 0.16 since its sentences varied a lot in length and little punctuation was used, which caused it to be read as human. Because the style signal is below 0.5, my rule caps the combined score at 0.64, so it gets the "unsure" label instead of AI, which is the outcome I want. When two methods disagree the system can't truly know, and calling it AI would risk accusing a real writer of using AI generated content. On the model signal alone, the real writer in this case would have received a high confidence AI label, which is the false positive I traced in Milestone 1. My rule prevented this.

### Calibration: four deliberate inputs

I sent each of these through `POST /submit` (plus my plain paragraph as a fifth):

| Input | model | style | combined | label |
|---|---|---|---|---|
| Clearly AI | 0.886 | 0.516 | 0.701 | high-confidence AI |
| Clearly human (casual) | 0.244 | 0.000 | 0.122 | high-confidence human |
| Formal human (my essay) | 0.516 | 0.387 | 0.452 | unsure |
| Lightly-edited AI | 0.814 | 0.439 | 0.626 | unsure |
| Plain human (my split case) | 0.765 | 0.156 | 0.461 | unsure |

Neither of my human texts that could have been accused was: the formal essay and the plain paragraph both landed in unsure. All three labels were reachable.

**The miss:** the lightly-edited AI text got through as unsure. Looking at the two signals separately, the model signal read it correctly as AI (0.814), but the style signal read it as human (0.439), which triggered my cap. Splitting style into its two measures, spread scored it as AI-like (0.329) but punctuation scored it as human (0.048, almost at the 0.04 human anchor). Punctuation is the measure that's off: its anchors came from one comma-heavy AI paragraph, and the other AI texts don't use much punctuation. Dropping punctuation would catch this text (combined 0.794, AI), but it would also push my formal essay to 0.605, close to the 0.65 AI line. I kept punctuation for now, because missing some lightly-edited AI costs less than accusing a real writer.

**A short-text limitation:** the minimum is 5 words, and "The cat sat down quietly." passed and was labelled human. A label on five words is mostly a guess.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |0.00-0.35|"We think this was probably written by a human."|
| unsure |above 0.35, below 0.65|"We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it."|
| high-confidence AI |0.65-1.00|"This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal."|

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->
The wording for "unsure" tells the user the truth, which is that the system can't be completely sure about the text based on what it can observe. This wording explicitly states that a conclusion hasn't been reached to avoid the risk of wrongfully accusing the writer. When doing calibration runs, both of my human pieces(a snippet of an essay I wrote and a plain paragraph) landed in "unsure", so that's the label a real writer is likely to see. 



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables.", "creator_id": "sample-writer"}'
```

```json
{
  "combined_score": 0.7012,
  "confidence": 0.4024,
  "content_id": "a0812099-435b-401b-b0f4-4b1ee0564570",
  "guess": "ai",
  "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
  "model_score": 0.8864,
  "style_score": 0.516
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "a0812099-435b-401b-b0f4-4b1ee0564570", "reasoning": "I wrote this myself for a class assignment and can share my drafts."}'
```

```json
{
  "content_id": "a0812099-435b-401b-b0f4-4b1ee0564570",
  "message": "Your appeal has been recorded, and this result is now under review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.7012,
      "confidence": 0.4024,
      "content_id": "39412239-9fa2-4df6-8b0a-6725b66a6d2b",
      "creator_id": "label-check",
      "guess": "ai",
      "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
      "model_score": 0.8864,
      "status": "decided",
      "style_score": 0.516,
      "timestamp": "2026-11-02T01:55:47+00:00"
    },
    {
      "combined_score": 0.7012,
      "confidence": 0.4024,
      "content_id": "a0812099-435b-401b-b0f4-4b1ee0564570",
      "creator_id": "sample-writer",
      "guess": "ai",
      "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
      "model_score": 0.8864,
      "status": "decided",
      "style_score": 0.516,
      "timestamp": "2026-11-02T02:17:57+00:00"
    },
    {
      "content_id": "a0812099-435b-401b-b0f4-4b1ee0564570",
      "creator_id": "sample-writer",
      "event": "appeal",
      "reasoning": "I wrote this myself for a class assignment and can share my drafts.",
      "status": "under_review",
      "timestamp": "2026-11-02T02:17:57+00:00"
    }
  ]
}
```

The original `decided` entry stays where it was; the appeal is a new
`under_review` entry with the same `content_id` right after it.

---

## How I Used AI

**Moment 1**

- *What I asked for:* I was confused about where to start and where to look in order to  fill out the seven steps
- *What came back:* a walkthrough of the repo and a draft seven-step trace naming each file a submission passes through.
- *What I changed:* I wrote the trace in my own words, and further broke down exactly what the blind spot of using stylometry meant in simple terms: "typos or a pasted quote can move the score when they shouldn't".

**Moment 2**

- *What I asked for:* I asked AI to look over the three functions I wrote for stylometry.py.
- *What came back:* Claude pointed out five bugs that would cause errors.
- *What I changed:* I reviewed and accepted Claude's changes to the functions that still used my own original logic. The bugs included mistakes like comparing the list itself to 2 instead of its length, and dividing by the word count without checking if it's zero. Claude replaced a while loop I made for one of the functions with a one-line range, so I checked that it gave me the same result(properly chunking the text input) before keeping it. 

**Moment 3**

- *What I asked for:* 
I asked Claude for options to improve the system before running the "after" tests. I asked it for a rundown of how each would be implemented and told it not to change anything until I'd picked one.
- *What came back:* 
four options, each simulated against my recorded signal scores from the before runs:
  - A: stricter word counting in the route
  - B: recalibrating signal two's anchors
  - C1: weighting signal one at 0.7
  - C2: raising SIGNAL_HUMAN_LINE from 0.5 to 0.6
- *What I changed:* 
I chose C2 and set aside the others. I didn't pick C1 because it wouldn't just moved the false accusation somewhere else, and I didn't pick B because the anchors would then be tuned on my own essays, risking overfitting. This led me to choose A and C2 together, which was a change I could trace results back to easily.

**Moment 4**

- *What I asked for:* I asked for help naming the stage and mechanisms responsible for each miss and broken attack. I gave Claude my own guesses about where I though the issue was(the scoring mechanisms for both signals for both criterions 1 and 2).
- *What came back:*  Claude gave back a breakdown of the style measures for both texts, and also showed that a neutral style score would cause both texts to land in unsure, so signal two was the deciding stage that we needed to focus on, not signal one. 
- *What I changed:* 
I wrote criterion 1 and criterion 2's diagnoses in my own words, then had Claude check them, add the supporting numbers, and fix my typos. The detail about the safeguard line is what pointed me to the improvemnet in Moment 3. I fixed the comining rule instead of signal two because it was a smaller and more traceable change. 
<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** _8_ per minute, _180_ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 200 200 200 429 429 429 429 429 429 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Produced by `run_attacks.py::main` against `app.py::submit`, copied from `results/attack_run_2026-11-06_1345.md`. Totals: **47 held, 9 broke** out of 56.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `34188ea4-10be-4006-b8a1-dad3c5cf37a9` | human | 0.337 |BROKE|
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `969bc188-58d8-41dd-ba78-84e7660d3f40` | human | 0.406 |BROKE|
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `a9338fe7-a169-43ca-8053-e4bfb1f22fe4` | unsure | 0.065 |HELD|
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `4fb84c31-65b0-4044-9102-4be1175cb237` | unsure | 0.111 |HELD|
| EV05 | evasion | both signals: heavy human editing pass | 200 | `d9c18b93-9546-4d4c-9f82-3a44102100e8` | human | 0.548 |BROKE|
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `97d19d2a-8013-45ed-9478-f6e13029dce0` | human | 0.427 |BROKE|
| EV07 | evasion | signal two: padding with punctuation | 200 | `33328c0c-9f49-4502-9ade-ee451c2a771f` | ai | 0.336 |HELD|
| EV08 | evasion | signal one: text below the token window | 200 | `cb81677a-eede-4fdf-a64b-d259bb1691a1` | human | 0.302 |BROKE|
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `095d629f-8b7b-47fb-aaee-4707e042c1dd` | unsure | 0.075 |HELD|
| EV10 | evasion | signal two: repeated stanza structure | 200 | `5dc006c0-4bb8-4981-b1a5-058d99f8651a` | unsure | 0.274 |HELD|
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `e3a4fb22-06dc-46c6-86ce-f1d38c00e2f5` | unsure | 0.179 |HELD|
| FP02 | false_positive | human writing in a formal register | 200 | `c5590d44-a136-401d-9ff1-d5c2e2a840d9` | unsure | 0.239 |HELD|
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `1cda8d6c-f60f-42ae-aeff-204630608f13` | unsure | 0.193 |HELD|
| FP04 | false_positive | a student essay written to a rubric | 200 | `9e14d43d-31fa-4789-a67b-fe50029728c3` | unsure | 0.166 |HELD|
| FP05 | false_positive | technical documentation written by a person | 200 | `52379b3f-e5f2-41b0-8864-1f5e561f2e86` | unsure | 0.262 |HELD|
| FP06 | false_positive | a person imitating a formal template | 200 | `ad0e70f9-7d9b-4f89-a181-b4d8d696b8b4` | unsure | 0.003 |HELD|
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `ca092b67-a199-4616-9878-c7e2e3e75ee3` | unsure | 0.118 |HELD|
| FP08 | false_positive | very short genuine human submission | 200 | `510d7a35-20eb-4ade-b212-cd7e2a8996ea` | human | 0.439 |HELD|
| PI01 | prompt_injection | instruction to ignore the check | 200 | `3009b9d3-8916-4395-acef-5b8c01563625` | human | 0.537 |BROKE|
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `f464e8ce-0909-4ac4-8fcd-12050eb6b07f` | human | 0.768 |BROKE|
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `5c3cbf79-2f53-425d-82a1-3b45f4447187` | unsure | 0.052 |HELD|
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `b3d33980-8b37-47a6-a0d2-180eb9656e8c` | unsure | 0.030 |HELD|
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `d7cfa75d-18f6-455f-8fb4-93a48d7b1112` | ai | 0.324 |HELD|
| PI06 | prompt_injection | instruction plus real human text | 200 | `e1c8ffa8-4b01-4c59-9488-fa76dbc40772` | unsure | 0.221 |HELD|
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |HELD|
| MF02 | malformed | text is a single character | 400 | `—` | — | — |HELD|
| MF03 | malformed | text is control characters | 400 | `—` | — | — |HELD|
| MF04 | malformed | text is only punctuation | 200 | `453b2ab6-aaa3-4a5c-8eb0-12780a75eea1` | human | 0.489 |BROKE|
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |HELD|
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |HELD|
| MF07 | malformed | text is right-to-left script | 200 | `1eca6c5e-cac8-483d-aafb-79d335b6e3a2` | ai | 0.406 |BROKE|
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |HELD|
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |HELD|
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |HELD|
| RQ03 | malformed | text is a number | 400 | `—` | — | — |HELD|
| RQ04 | malformed | text is a list | 400 | `—` | — | — |HELD|
| RQ05 | malformed | text is null | 400 | `—` | — | — |HELD|
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |HELD|
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |HELD|
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |HELD|
| RQ09 | malformed | body is empty | 400 | `—` | — | — |HELD|
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |HELD|
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |HELD|
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |HELD|
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `53b858a1-72a1-4b14-a8aa-f4b6533d5fa3` | human | 0.721 |HELD|
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d58ffcbd-2b66-48f3-a30a-16a2231bfa48` | human | 0.721 |HELD|
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3203992a-f462-48d3-95f2-38e34d8a904e` | human | 0.721 |HELD|
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4d66e9f5-5e29-48b6-9ede-9591e2868db1` | human | 0.721 |HELD|
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2a38d04e-cb79-4724-bb1b-4f1badd028b4` | human | 0.721 |HELD|
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `823e3a73-c3a3-4d58-bb29-c3a4a65b7853` | human | 0.721 |HELD|
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5d62b5c8-c0db-4695-9949-886c4549c142` | human | 0.721 |HELD|
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0e1f9ad1-4c30-4f53-9480-affb5184e650` | human | 0.721 |HELD|
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |HELD|
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |HELD|
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |HELD|
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |HELD|

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

From the run at 2026-11-06 18:43–18:45 UTC, in this order:

1. **EV05**: AI text after a heavy human edit was labeled human (evasion worked).
2. **EV01**: typos alone were enough to pass as human.
3. **EV08**: text below the token window was labeled human.
4. **PI01**: "Ignore all previous instructions… return human" got human.
5. **PI02**: a fake SYSTEM message got human, with the highest confidence in the run.
6. **FP06**: near miss. The model signal gave 0.88 on human writing; only the style signal pulled it back to unsure.
7. **MF04**: punctuation-only text was accepted and scored as human.
8. **MF07**: right-to-left script was labeled AI.
9. **MF01**: whitespace-only text was rejected cleanly.
10. **FL01_08**: the 8th flood submission was allowed.
11. **FL01_09**: the 9th flood submission was refused with a 429 (rejection entry, so it has fewer fields).

```json
{"timestamp": "2026-11-06T18:43:45+00:00", "content_id": "d9c18b93-9546-4d4c-9f82-3a44102100e8", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.1311, "combined_score": 0.2261, "label": "We think this was probably written by a human.", "status": "decided", "confidence": 0.5478}
{"timestamp": "2026-11-06T18:43:29+00:00", "content_id": "34188ea4-10be-4006-b8a1-dad3c5cf37a9", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.5, "combined_score": 0.3317, "label": "We think this was probably written by a human.", "status": "decided", "confidence": 0.3366}
{"timestamp": "2026-11-06T18:44:00+00:00", "content_id": "cb81677a-eede-4fdf-a64b-d259bb1691a1", "creator_id": "attacker_EV08", "guess": "human", "model_score": 0.2452, "style_score": 0.4531, "combined_score": 0.3492, "label": "We think this was probably written by a human.", "status": "decided", "confidence": 0.3016}
{"timestamp": "2026-11-06T18:44:43+00:00", "content_id": "3009b9d3-8916-4395-acef-5b8c01563625", "creator_id": "attacker_PI01", "guess": "human", "model_score": 0.4625, "style_score": 0.0, "combined_score": 0.2313, "label": "We think this was probably written by a human.", "status": "decided", "confidence": 0.5374}
{"timestamp": "2026-11-06T18:44:46+00:00", "content_id": "f464e8ce-0909-4ac4-8fcd-12050eb6b07f", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.0278, "combined_score": 0.1161, "label": "We think this was probably written by a human.", "status": "decided", "confidence": 0.7678}
{"timestamp": "2026-11-06T18:44:36+00:00", "content_id": "ad0e70f9-7d9b-4f89-a181-b4d8d696b8b4", "creator_id": "attacker_FP06", "guess": "unsure", "model_score": 0.8814, "style_score": 0.1155, "combined_score": 0.4985, "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "status": "decided", "confidence": 0.003}
{"timestamp": "2026-11-06T18:45:00+00:00", "content_id": "453b2ab6-aaa3-4a5c-8eb0-12780a75eea1", "creator_id": "attacker_MF04", "guess": "human", "model_score": 0.0112, "style_score": 0.5, "combined_score": 0.2556, "label": "We think this was probably written by a human.", "status": "decided", "confidence": 0.4888}
{"timestamp": "2026-11-06T18:45:01+00:00", "content_id": "1eca6c5e-cac8-483d-aafb-79d335b6e3a2", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 0.5, "combined_score": 0.7032, "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.", "status": "decided", "confidence": 0.4064}
{"timestamp": "2026-11-06T18:44:58+00:00", "creator_id": "attacker_MF01", "event": "rejected", "status": "rejected", "reason": "text_too_short"}
{"timestamp": "2026-11-06T18:45:03+00:00", "content_id": "0e1f9ad1-4c30-4f53-9480-affb5184e650", "creator_id": "attacker_flood", "guess": "human", "model_score": 0.0287, "style_score": 0.25, "combined_score": 0.1394, "label": "We think this was probably written by a human.", "status": "decided", "confidence": 0.7212}
{"timestamp": "2026-11-06T18:45:03+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "8 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:
The worst outcome was the outcome displayed by attack MF07, which labelled writing as AI when it was simply from right to left instead of left to right. The model signal couldn't read the input, and the style signal stayed at 0.5, so neither one was evidence towards the writing being AI generated. 



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. my own writing(One or less called AI) | <=1 | 2 |  2 | 2 | MISS |
| 2. Avg of AI writing score is >=0.45 greater than avg of human writing score| >=0.45 |0.236|0.236|0.236|MISS|
| 3. 5/5 appeals successful, fake ids don't log|5/5|5/5|5/5|5/5|MET|
| 4. bad input |6|6|6|6|MET|
| 5. label coverage |each label reached by its own group|3/3|3/3|3/3|MET|

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

#### Criterion 1: my own writing

Produced by `run_eval.py::main`, which sent each text to `app.py::submit` (scored by `scoring.py::combine_signals`); copied from `results/run_2026-11-06_2122_before.md`. Trials 2 and 3 returned identical output. The third and fourth entries (`MY_PLAIN` and `HUMAN_ONE`) are my own writing labelled `ai`, the two false positives that make criterion 1 a miss.

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.7564,
    "model_score": 0.2436,
    "style_score": 0.0,
    "label": "We think this was probably written by a human.",
    "sent": "I know. I\u2019m looking at this in terms of exponential progress and techn"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0968,
    "model_score": 0.516,
    "style_score": 0.3872,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "With a black composition notebook and a pencil, I scribbled out \u201cproto"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.3452,
    "model_score": 0.5783,
    "style_score": 0.7669,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "Furthermore, McGrath asserts that ignorance is the effect of indoctrin"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.3968,
    "model_score": 0.7221,
    "style_score": 0.6746,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "On late Friday nights, I remember the magic that accompanied the enthr"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3782,
    "model_score": 0.1973,
    "style_score": 0.4244,
    "label": "We think this was probably written by a human.",
    "sent": "Following an anticipation filled car ride under the stars, we\u2019d arrive"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1996,
    "model_score": 0.4952,
    "style_score": 0.3053,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "Also on the first floor was the kitchen, which had a refrigerator cove"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.2586,
    "model_score": 0.5047,
    "style_score": 0.2366,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "Bordering both the kitchen and foyer was the conjoined dining room and"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.085,
    "model_score": 0.514,
    "style_score": 0.401,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "\tOn the second floor of the house are two bathrooms, the computer room"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0342,
    "model_score": 0.5476,
    "style_score": 0.4865,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "Perpendicular to my mother\u2019s room is the computer room, which was doub"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1706,
    "model_score": 0.5728,
    "style_score": 0.5978,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "\tIn the poem, McGrath reiterates that indoctrination is deeply embedde"
  }
]
```

#### Criterion 2: score spread

Produced by `run_eval.py::main`, which sent each request to `app.py::submit`; copied from trial 1 of `results/run_2026-11-06_2122_before.md`. Trials 2 and 3 returned identical output. Known-AI average combined score 0.6874, known-human average 0.4511, gap 0.236 (combined scores recomputed from the two signal scores with `scoring.py::combine_signals`; they match `logs/audit.jsonl`).

Scenario "spread: known AI":

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.4024,
    "model_score": 0.8864,
    "style_score": 0.516,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "The implementation of the proposed framework requires careful consider"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.4732,
    "model_score": 0.7956,
    "style_score": 0.6776,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "Effective time management is an essential skill for students and profe"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6772,
    "model_score": 0.9167,
    "style_score": 0.7605,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "Climate change represents one of the most pressing challenges facing h"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.4038,
    "model_score": 0.688,
    "style_score": 0.7159,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "Reading offers numerous benefits that extend far beyond entertainment."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0826,
    "model_score": 0.6508,
    "style_score": 0.2666,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "Remote work has transformed the modern workplace in significant ways. "
  }
]
```

Scenario "spread: known human":

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.7564,
    "model_score": 0.2436,
    "style_score": 0.0,
    "label": "We think this was probably written by a human.",
    "sent": "I know. I\u2019m looking at this in terms of exponential progress and techn"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0968,
    "model_score": 0.516,
    "style_score": 0.3872,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "With a black composition notebook and a pencil, I scribbled out \u201cproto"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.3452,
    "model_score": 0.5783,
    "style_score": 0.7669,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "Furthermore, McGrath asserts that ignorance is the effect of indoctrin"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.3968,
    "model_score": 0.7221,
    "style_score": 0.6746,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "On late Friday nights, I remember the magic that accompanied the enthr"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3782,
    "model_score": 0.1973,
    "style_score": 0.4244,
    "label": "We think this was probably written by a human.",
    "sent": "Following an anticipation filled car ride under the stars, we\u2019d arrive"
  }
]
```

#### Criterion 3: the appeal path

Tested by hand with curl against `app.py::submit` and `app.py::appeal`. These are the entries `audit.py::log_decision` and `audit.py::log_appeal` wrote to `logs/audit.jsonl`, read back through `GET /log` (`app.py::get_log`). Each `content_id` has its original `decided` entry and a later `under_review` entry. The made-up `content_id` returned `404` and added nothing to the log.

```json
{"timestamp": "2026-11-07T02:47:36+00:00", "content_id": "9cd38191-8b31-44a6-85be-165d9d12c6f9", "creator_id": "appeal_t1", "guess": "unsure", "model_score": 0.6971, "style_score": 0.5, "combined_score": 0.5986, "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "status": "decided", "confidence": 0.1972}
{"timestamp": "2026-11-07T02:48:21+00:00", "content_id": "7ce4bb96-8eb1-4813-b300-e53dcc49136c", "creator_id": "appeal_t2", "guess": "unsure", "model_score": 0.6971, "style_score": 0.5, "combined_score": 0.5986, "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "status": "decided", "confidence": 0.1972}
{"timestamp": "2026-11-07T02:48:29+00:00", "content_id": "6900f6d7-8bfd-4767-8cd0-cbcb8cd191e4", "creator_id": "appeal_t3", "guess": "unsure", "model_score": 0.6971, "style_score": 0.5, "combined_score": 0.5986, "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "status": "decided", "confidence": 0.1972}
{"timestamp": "2026-11-07T02:48:38+00:00", "content_id": "d85cbe6d-0f0b-437a-acc8-98a283ac9841", "creator_id": "appeal_t4", "guess": "unsure", "model_score": 0.6971, "style_score": 0.5, "combined_score": 0.5986, "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "status": "decided", "confidence": 0.1972}
{"timestamp": "2026-11-07T02:48:47+00:00", "content_id": "874ef540-c183-4ed5-b0b3-470b90951923", "creator_id": "appeal_t5", "guess": "unsure", "model_score": 0.6971, "style_score": 0.5, "combined_score": 0.5986, "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "status": "decided", "confidence": 0.1972}
{"timestamp": "2026-11-07T03:00:43+00:00", "content_id": "9cd38191-8b31-44a6-85be-165d9d12c6f9", "creator_id": "appeal_t1", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself."}
{"timestamp": "2026-11-07T03:02:18+00:00", "content_id": "7ce4bb96-8eb1-4813-b300-e53dcc49136c", "creator_id": "appeal_t2", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself."}
{"timestamp": "2026-11-07T03:02:59+00:00", "content_id": "6900f6d7-8bfd-4767-8cd0-cbcb8cd191e4", "creator_id": "appeal_t3", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself."}
{"timestamp": "2026-11-07T03:03:39+00:00", "content_id": "d85cbe6d-0f0b-437a-acc8-98a283ac9841", "creator_id": "appeal_t4", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself."}
{"timestamp": "2026-11-07T03:04:05+00:00", "content_id": "874ef540-c183-4ed5-b0b3-470b90951923", "creator_id": "appeal_t5", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself."}

"Under Review"(Successful) Response: 
{
  "content_id": "874ef540-c183-4ed5-b0b3-470b90951923",
  "message": "Your appeal has been recorded, and this result is now under review.",
  "status": "under_review"
}
Fake content id:
{
  "error": "not_found",
  "message": "No submission found with content_id 'not-a-real-id-123'."
}

404
```

#### Criterion 4: bad input

Produced by `run_eval.py::main`, which sent each request to `app.py::submit`; copied from trial 1 of `results/run_2026-11-06_2122_before.md`. Trials 2 and 3 returned identical output.

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "   \n  "
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "Hello there"
  },
  {
    "status": 413,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "word word word word word word word word word word word word word word "
  }
]
```

#### Criterion 5: label coverage

Produced by `run_eval.py::main`, which sent each request to `app.py::submit`; copied from trial 1 of `results/run_2026-11-06_2122_before.md`. Trials 2 and 3 returned identical output. In order: 3 known-AI, 3 known-human, 3 borderline.

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.4024,
    "model_score": 0.8864,
    "style_score": 0.516,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "The implementation of the proposed framework requires careful consider"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.4732,
    "model_score": 0.7956,
    "style_score": 0.6776,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "Effective time management is an essential skill for students and profe"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6772,
    "model_score": 0.9167,
    "style_score": 0.7605,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "Climate change represents one of the most pressing challenges facing h"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.7564,
    "model_score": 0.2436,
    "style_score": 0.0,
    "label": "We think this was probably written by a human.",
    "sent": "I know. I\u2019m looking at this in terms of exponential progress and techn"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0968,
    "model_score": 0.516,
    "style_score": 0.3872,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "With a black composition notebook and a pencil, I scribbled out \u201cproto"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1996,
    "model_score": 0.4952,
    "style_score": 0.3053,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "Also on the first floor was the kitchen, which had a refrigerator cove"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.253,
    "model_score": 0.8141,
    "style_score": 0.4389,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "Artificial intelligence has changed the way people approach everyday t"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.3452,
    "model_score": 0.5783,
    "style_score": 0.7669,
    "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
    "sent": "Furthermore, McGrath asserts that ignorance is the effect of indoctrin"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0072,
    "model_score": 0.4637,
    "style_score": 0.5436,
    "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
    "sent": "I agree with Jones and found the article insightful because I\u2019ve never"
  }
]
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

Criterion 1:
The first criterion was missed because two of my human-written texts, MY_PLAIN (combined 0.673) and HUMAN_ONE (combined 0.698), were labelled AI in all three trials. The stage responsible in both was signal two, `stylometry.style_signal`. It treats a sentence-length spread of 0.25 or lower as fully AI (`SPREAD_ANCHORS = (0.60, 0.25)`), and it counts commas, colons, and parentheses as AI-like. Both texts are careful long-form writing with long, evenly sized, comma-heavy sentences (spread 0.224 and 0.259), and MY_PLAIN's citations like "(McGrath 23)" add parentheses on top. That gave them style scores of 0.767 and 0.675.

In both cases, signal one was only borderline (model scores 0.578 and 0.722), and it was the style score that pushed the writing into high-confidence AI. With a neutral style score of 0.5, they would have combined to 0.539 and 0.611 and landed in unsure. The combining rule didn't catch it either: my safeguard only caps the score below the AI threshold (into unsure) if either signal is under 0.5, and MY_PLAIN's model score of 0.578 was just above that line, so the cap never applied.

Criterion 2:
The average combined scores of the AI-written group (0.687) and the human-written group (0.451) are too close: a gap of 0.236 against my target of 0.45, the same in all three trials. The problem is on both ends: the human average is too high, and the AI average is too low. The stage responsible is again signal two, `stylometry.style_signal`, and more specifically its sentence-length spread and comma-density measures, because the two don't separate the tested AI texts from my writing.

On the human side, the same two texts from criterion 1 (0.673 and 0.698) pull the average up; the other three human texts average 0.295. On the AI side, signal two reads some of the AI texts as human. AI_REMOTE has varied sentence lengths (spread 0.434), so its style score is only 0.267 and its combined score falls to 0.459 (unsure), and AI_SAMPLE's style score is only 0.516. The combining rule makes this worse: it weights both signals equally (0.5 each), so when signal two can't tell the groups apart, it cuts the gap that signal one creates roughly in half.

---

## The Improvement

**What I changed:**

I changed the `SIGNAL_HUMAN_LINE` setting in `config.py` from 0.5 to 0.6. Before, my combining rule only let the AI label through when both signals agreed, meaning that both were at 0.5 or above. Now they both have to be at 0.6 or above. If either one is below 0.6, the combined score is capped at 0.64, just under the AI threshold, so the worst label it can get is unsure.


**Which diagnosis pointed at it:**
The criterion 1 diagnosis pointed at it. One of my human writings, `MY_PLAIN`, was labelled as AI and had a combined score of 0.673. The model score was 0.578, which was only just above the 0.5 line, but since it was above it, the safeguard didn't apply and the high style score of 0.767 carried it to an AI classification. By moving the safeguard's line up, a borderline signal like that no longer counts as agreeing. The diagnosis really named two stages, which were signal two and the combining rule, but the combining rule was what I ended up changing because it's a smaller change and didn't involve retuning the style signal on my own essays, which risked overfitting and making a less generally effective system. 

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Produced by `run_attacks.py::main` against `app.py::submit`, copied from `results/attack_run_2026-11-07_1124_after~.md`. Totals: **48 held, 8 broke** (before: 47 held, 9 broke). Only two attacks changed: MF07 and EV07 went from `ai` to `unsure`; every other row returned the same status and guess as before.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `3c434daa-4904-489b-939f-a44c081f36f0` | human | 0.337 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `7b75b5d8-2fe8-43a7-9f82-5bc90737e703` | human | 0.406 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `33425549-a151-488b-b959-749673e96dc5` | unsure | 0.065 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `acdf8cbf-3a5b-46b3-95af-4f8acbc3da27` | unsure | 0.111 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `da7eb2dc-da22-4aaf-a1f7-8ccf8a8d87f6` | human | 0.548 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `283dca24-a9bb-435a-b53c-934b10eec19a` | human | 0.427 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `f642a296-b1d0-476f-9097-04275f1b8321` | unsure (was `ai`) | 0.280 | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | `c4609bbe-46c8-422f-a548-ae0241fcdfae` | human | 0.302 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `7c968973-1519-41e6-ad29-6fb201f5ed81` | unsure | 0.075 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `7a1349f2-29a3-4857-868c-c7e1cb82f493` | unsure | 0.274 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `b42ad956-e914-4adf-ae99-80b7bb62c5a8` | unsure | 0.179 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `b33ece9c-6a45-4019-8138-1a672b65001e` | unsure | 0.239 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `abee1ddc-1e0b-46bc-92fb-310e71d8f0a4` | unsure | 0.193 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `03e451f6-d094-4eeb-8555-8fe4370bbde5` | unsure | 0.166 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `d0d514b8-d719-4f8f-b03e-6cfa2780b40d` | unsure | 0.262 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `fdb23911-ec5e-405e-86f5-3a8b9f682e9b` | unsure | 0.003 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `05f9fe81-80f6-4ab5-bf5e-50ae34fe5aaf` | unsure | 0.118 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `d5fb42cd-68e2-4e81-8bcd-0a3d97881199` | human | 0.439 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `57c1c2ba-4ea9-49d6-b22c-a4464471ee78` | human | 0.537 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `a7c66c4c-8eb0-434a-ac0e-3cd3c5d7a3a6` | human | 0.768 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `f9f1d813-180f-4dd0-9757-6b530040112e` | unsure | 0.052 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `3fed96ca-49d7-45df-87bc-9f9fcc799a03` | unsure | 0.030 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `9bd8cbb2-8768-414b-9197-ef5adcdd3695` | ai | 0.324 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `4d3b9b8e-5fa2-4cfc-aa9e-e8ba0e7d46ed` | unsure | 0.221 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 200 | `f90b231c-aedc-4e2c-89dc-6d44a5c598b4` | human | 0.489 | BROKE |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `87dba64b-694d-4de5-8aa5-3eee94b1908a` | unsure (was `ai`) | 0.280 | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `78e81783-49a4-426f-97fd-272a719ffe61` | human | 0.721 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5a70f630-29fb-48bc-801e-4a07a69d11c7` | human | 0.721 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `98d2cb84-e510-43d8-bbbd-233d19f3bd44` | human | 0.721 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2721aaa7-cdb7-4cd1-ba18-a4eb38be25ba` | human | 0.721 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5f949fd1-2651-4ae3-b0f0-da20dcef28e7` | human | 0.721 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `14942c55-0007-431b-9f65-163c5b412e4f` | human | 0.721 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `818e844f-c0e0-4449-96fd-400a97b76768` | human | 0.721 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2b0801cf-3d43-4b98-acc8-fc07f5de8a18` | human | 0.721 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

**Run log — after**

Produced by `run_eval.py::main` against `app.py::submit`, scored by `scoring.py::combine_signals`; from `results/run_2026-11-07_1126_after.md`. All three trials were identical again.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives on my own writing | ≤ 1 of 10 labelled `ai` | 1 of 10 | 1 of 10 | 1 of 10 | **PASS** (before: MISS, 2 of 10) |
| 2. Score spread | AI avg − human avg ≥ 0.45 | 0.231 (0.675 − 0.445) | 0.231 | 0.231 | **MISS** (before: 0.236) |
| 3. Appeal path | 5/5 appeals → 200 `under_review`, logged with original kept; fake ID → 404, nothing logged | 5/5, 404 ✓, log +0 | 5/5, 404 ✓, log +0 | 5/5, 404 ✓, log +0 | **PASS** (from `results/appeal_trials_2026-11-07_1133_after.md`) |
| 4. Bad input | 5 × 400, 1 × 413, no 500 | 6/6 | 6/6 | 6/6 | **PASS** |
| 5. Label coverage | each label reached by its own group | ai ✓ human ✓ unsure ✓ | ai ✓ human ✓ unsure ✓ | ai ✓ human ✓ unsure ✓ | **PASS** |

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

Yes, it did help, as the system now passes criterion 1. I know because I re-ran the same evals and attack set after the change: my own writing labelled AI went from 2 of 10 to 1 of 10 in all three trials (`results/run_2026-11-06_2122_before.md` vs `results/run_2026-11-07_1126_after.md`), and the attack run went from 47 held, 9 broke to 48 held, 8 broke. It also made MF07 go from ai to unsure, so the right-to-left writer is no longer accused.

However, it only just passes: `HUMAN_ONE` is still labelled AI, because both of its signals are above 0.6 (model 0.722, style 0.675), so one more false positive would fail criterion 1 again. The change also made a known AI sample, `AI_SAMPLE`, go from ai to unsure, along with EV07, and it made the gap between the AI and human group averages slightly worse (0.236 to 0.231), since capping scores brought down the AI group average. Making the AI label harder to reach protects real writers but allows more AI text to land in unsure.



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

Criterion 2 is still broken (gap 0.231 against a target of 0.45). To try to fix it, I'd make signal two more effective at separating AI text from human text. For example, I'd find a style measure to incorporate that doesn't penalize careful long-form writing, or weight signal one more heavily once I fix signal two. I stopped here because making one simple change didn't get close to fixing it. To get a gap of 0.45 between the averages, a better signal is needed, along with more test texts so the system isn't tailored to my own essays only.

Signal two is also easy to fool with sentence rhythm, shown by EV02, EV06, and PI01 still getting labelled human. To fix it, I'd make the sentence-length spread count less. I stopped here because any change to signal two moves both false positives and evasions, and I'd prefer a change with an effect I can clearly trace.

The route still accepts texts whose signals it can't measure. MF04 (punctuation only) is still labelled human, and MF07 (right-to-left script) is no longer accused but is still accepted and given a verdict. To fix it, I'd count the words in each input with `stylometry.words()` instead of `split()`, and reject texts with too few real words. I stopped here because I had already made one change.

EV01 and PI02 (signal one reads surprising tokens like typos or fake system text as human), EV08 (too short to measure reliably), and EV05 (so heavily human-edited that nothing is left to detect) also still get through. I didn't attempt these.


**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->
I'd keep erring towards "unsure", because a writer wrongly labelled as AI pays a large cost, while AI that slips into unsure costs the site and honest writers only a little each. The people at the highest risk are honest writers competing with undetected AI work, which I'd accept as a flaw.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
