# Attack run — after~

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-07 11:24
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `3c434daa-4904-489b-939f-a44c081f36f0` | human | 0.337 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `7b75b5d8-2fe8-43a7-9f82-5bc90737e703` | human | 0.406 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `33425549-a151-488b-b959-749673e96dc5` | unsure | 0.065 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `acdf8cbf-3a5b-46b3-95af-4f8acbc3da27` | unsure | 0.111 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `da7eb2dc-da22-4aaf-a1f7-8ccf8a8d87f6` | human | 0.548 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `283dca24-a9bb-435a-b53c-934b10eec19a` | human | 0.427 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `f642a296-b1d0-476f-9097-04275f1b8321` | unsure | 0.280 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `c4609bbe-46c8-422f-a548-ae0241fcdfae` | human | 0.302 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `7c968973-1519-41e6-ad29-6fb201f5ed81` | unsure | 0.075 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `7a1349f2-29a3-4857-868c-c7e1cb82f493` | unsure | 0.274 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `b42ad956-e914-4adf-ae99-80b7bb62c5a8` | unsure | 0.179 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `b33ece9c-6a45-4019-8138-1a672b65001e` | unsure | 0.239 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `abee1ddc-1e0b-46bc-92fb-310e71d8f0a4` | unsure | 0.193 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `03e451f6-d094-4eeb-8555-8fe4370bbde5` | unsure | 0.166 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `d0d514b8-d719-4f8f-b03e-6cfa2780b40d` | unsure | 0.262 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `fdb23911-ec5e-405e-86f5-3a8b9f682e9b` | unsure | 0.003 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `05f9fe81-80f6-4ab5-bf5e-50ae34fe5aaf` | unsure | 0.118 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `d5fb42cd-68e2-4e81-8bcd-0a3d97881199` | human | 0.439 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `57c1c2ba-4ea9-49d6-b22c-a4464471ee78` | human | 0.537 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `a7c66c4c-8eb0-434a-ac0e-3cd3c5d7a3a6` | human | 0.768 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `f9f1d813-180f-4dd0-9757-6b530040112e` | unsure | 0.052 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `3fed96ca-49d7-45df-87bc-9f9fcc799a03` | unsure | 0.030 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `9bd8cbb2-8768-414b-9197-ef5adcdd3695` | ai | 0.324 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `4d3b9b8e-5fa2-4cfc-aa9e-e8ba0e7d46ed` | unsure | 0.221 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 200 | `f90b231c-aedc-4e2c-89dc-6d44a5c598b4` | human | 0.489 |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `87dba64b-694d-4de5-8aa5-3eee94b1908a` | unsure | 0.280 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `78e81783-49a4-426f-97fd-272a719ffe61` | human | 0.721 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5a70f630-29fb-48bc-801e-4a07a69d11c7` | human | 0.721 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `98d2cb84-e510-43d8-bbbd-233d19f3bd44` | human | 0.721 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2721aaa7-cdb7-4cd1-ba18-a4eb38be25ba` | human | 0.721 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5f949fd1-2651-4ae3-b0f0-da20dcef28e7` | human | 0.721 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `14942c55-0007-431b-9f65-163c5b412e4f` | human | 0.721 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `818e844f-c0e0-4449-96fd-400a97b76768` | human | 0.721 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2b0801cf-3d43-4b98-acc8-fc07f5de8a18` | human | 0.721 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "3c434daa-4904-489b-939f-a44c081f36f0",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3366,
  "model_score": 0.1635,
  "style_score": 0.5,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "7b75b5d8-2fe8-43a7-9f82-5bc90737e703",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.4056,
  "model_score": 0.5943,
  "style_score": 0.0,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "33425549-a151-488b-b959-749673e96dc5",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.0652,
  "model_score": 0.6662,
  "style_score": 0.2686,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "acdf8cbf-3a5b-46b3-95af-4f8acbc3da27",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.1114,
  "model_score": 0.6114,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "da7eb2dc-da22-4aaf-a1f7-8ccf8a8d87f6",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.5478,
  "model_score": 0.3212,
  "style_score": 0.1311,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "283dca24-a9bb-435a-b53c-934b10eec19a",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.4274,
  "model_score": 0.5727,
  "style_score": 0.0,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "f642a296-b1d0-476f-9097-04275f1b8321",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.5862,
  "style_score": 0.75,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c4609bbe-46c8-422f-a548-ae0241fcdfae",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3016,
  "model_score": 0.2452,
  "style_score": 0.4531,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "7c968973-1519-41e6-ad29-6fb201f5ed81",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.075,
  "model_score": 0.7042,
  "style_score": 0.2208,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "7a1349f2-29a3-4857-868c-c7e1cb82f493",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.2736,
  "model_score": 0.9792,
  "style_score": 0.2944,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "b42ad956-e914-4adf-ae99-80b7bb62c5a8",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.1788,
  "model_score": 0.6175,
  "style_score": 0.2036,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "b33ece9c-6a45-4019-8138-1a672b65001e",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.2388,
  "model_score": 0.7387,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "abee1ddc-1e0b-46bc-92fb-310e71d8f0a4",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.1934,
  "model_score": 0.8051,
  "style_score": 0.3883,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "03e451f6-d094-4eeb-8555-8fe4370bbde5",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.1662,
  "model_score": 0.8329,
  "style_score": 0.3333,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "d0d514b8-d719-4f8f-b03e-6cfa2780b40d",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.262,
  "model_score": 0.8005,
  "style_score": 0.4616,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "fdb23911-ec5e-405e-86f5-3a8b9f682e9b",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.003,
  "model_score": 0.8814,
  "style_score": 0.1155,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "05f9fe81-80f6-4ab5-bf5e-50ae34fe5aaf",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.1184,
  "model_score": 0.8816,
  "style_score": 0.0,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "d5fb42cd-68e2-4e81-8bcd-0a3d97881199",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.4392,
  "model_score": 0.3223,
  "style_score": 0.2386,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "57c1c2ba-4ea9-49d6-b22c-a4464471ee78",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.5374,
  "model_score": 0.4625,
  "style_score": 0.0,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "a7c66c4c-8eb0-434a-ac0e-3cd3c5d7a3a6",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.7678,
  "model_score": 0.2044,
  "style_score": 0.0278,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "f9f1d813-180f-4dd0-9757-6b530040112e",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.0524,
  "model_score": 0.5943,
  "style_score": 0.458,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "3fed96ca-49d7-45df-87bc-9f9fcc799a03",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.0304,
  "model_score": 0.4998,
  "style_score": 0.5306,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "9bd8cbb2-8768-414b-9197-ef5adcdd3695",
  "creator_id": "attacker_PI05",
  "guess": "ai",
  "confidence": 0.3238,
  "model_score": 0.6401,
  "style_score": 0.6837,
  "label": "This writing shows strong signs of being generated by AI. If you wrote it yourself, you can appeal.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "4d3b9b8e-5fa2-4cfc-aa9e-e8ba0e7d46ed",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.2208,
  "model_score": 0.5583,
  "style_score": 0.2208,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "f90b231c-aedc-4e2c-89dc-6d44a5c598b4",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.4888,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "87dba64b-694d-4de5-8aa5-3eee94b1908a",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "78e81783-49a4-426f-97fd-272a719ffe61",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7212,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "5a70f630-29fb-48bc-801e-4a07a69d11c7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7212,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "98d2cb84-e510-43d8-bbbd-233d19f3bd44",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7212,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "2721aaa7-cdb7-4cd1-ba18-a4eb38be25ba",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7212,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "5f949fd1-2651-4ae3-b0f0-da20dcef28e7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7212,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "14942c55-0007-431b-9f65-163c5b412e4f",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7212,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "818e844f-c0e0-4449-96fd-400a97b76768",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7212,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "2b0801cf-3d43-4b98-acc8-fc07f5de8a18",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.7212,
  "model_score": 0.0287,
  "style_score": 0.25,
  "label": "We think this was probably written by a human.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
