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
| `confidence` | float 0–1 | ___ <!-- the combined score, or how far it is from 0.5? --> |
| `label` | string | The plain-English sentence the writer sees |
| `model_score` | float 0–1 | Signal one. Higher = more AI-like |
| `style_score` | float 0–1 | Signal two. Higher = more AI-like |
| `combined_score` | float 0–1 | The combined score the label was picked from |

**Errors**

| Case | Status | `error` |
|---|---|---|
| Body isn't JSON, or `text` / `creator_id` missing or not a string | `400` | `bad_request` |
| `text` empty or too short to score (fewer than ___ words) | `400` | `text_too_short` |
| `text` longer than ___ characters | `413` | `text_too_long` |
| Too many requests (unit 8) | `429` | `rate_limited` |

#### `POST /appeal`

**Request**

| Field | Type | Required | Meaning |
|---|---|---|---|
| `content_id` | string | yes | From the `/submit` response |
| `reasoning` | string | yes | Why the writer thinks the label is wrong |

`creator_id` is ___ <!-- not needed (copied from the original log entry), or required? -->

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
| Item already under review | ___ | ___ <!-- 409 already_under_review, or accept and log a second appeal? --> |



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
It measures how unpredicatable or predictable a sequence of words is, also known as the perplexity. 

**Why that might differ between human and AI writing:**
Humans tend to have higher perplexity scores than AI when writing because humans are less predictable than AI.

**What it can't see:**
It might wrongly classify predicatable writing, since it has a lower perplexity score, as AI written, even if it's written by a human who happens to write predictably. That could include a new speaker or writer to the language or a younger writer. The reverse could also happen with more unpredicatble writing being classified as human even when it originated from AI because it has a unique sequence of words. In short, the score can't see authorship.

### Signal two — the style signal

**What it measures:**
It measures the shape of the input text and specific traits within the text.

**Why that might differ between human and AI writing:**
AI writing tends to have even, mid-length sentences from a shorter ranged vocabulary, while human writing
tends to be less consistent.

**What it can't see:**
The signal can't read, and doesn't pull any semantic knowledge from the text. Anything that changes the shape, like adding typos, breaking up sentences, or pasting a quotation can change the score.
### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? 
     

     Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.
     
     -->

**The rule:**

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

<!-- Milestone 3 run: signal one only. Re-run once labels and the second
     signal are in (Milestone 5) and replace this. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of the proposed framework requires careful consideration of several key factors. First, it is important to note that the system must be able to handle a wide variety of different inputs. Additionally, the overall performance of the solution depends on a number of important variables.", "creator_id": "sample-writer"}'
```

```json
{
  "combined_score": null,
  "confidence": 0.5,
  "content_id": "a3c9e5f4-e5a9-40ee-a536-c9e0a2539019",
  "guess": "unsure",
  "label": "PLACEHOLDER label",
  "model_score": 0.8864,
  "style_score": null
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": null,
      "content_id": "b70a5ba5-3615-44b6-a347-10d9dc30a0f4",
      "creator_id": "test",
      "guess": "unsure",
      "label": "PLACEHOLDER label",
      "model_score": 0.8809,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-10-31T20:40:48+00:00"
    },
    {
      "combined_score": null,
      "content_id": "a3c9e5f4-e5a9-40ee-a536-c9e0a2539019",
      "creator_id": "sample-writer",
      "guess": "unsure",
      "label": "PLACEHOLDER label",
      "model_score": 0.8864,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-01T04:40:32+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I was confused about where to start and where to look in order to  fill out the seven steps
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:* I wanted to confirm my knowledge of the two endpoint shapes was correct
- *What came back:*
- *What I changed:* I confirmed Claude's suggestion to add notes to the README describing the two endpoints. 

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
