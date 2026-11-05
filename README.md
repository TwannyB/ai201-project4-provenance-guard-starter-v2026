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

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

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



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
