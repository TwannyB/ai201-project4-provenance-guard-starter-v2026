# Criterion 3: appeal path, three trials (after the change)

- Requests sent with curl to `app.py::submit`, `app.py::appeal` and `app.py::get_log` · 2026-11-07 11:33
- Each trial: 5 new submissions under one creator_id, 5 appeals, a /log check, and one made-up content_id

## Trial 1 (creator_id `appeal_after_r1`)

### Submissions

```json
// HTTP 200
{"content_id": "c09b6fe5-8e3c-4308-9be2-a9bd180bc532", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it."}
// HTTP 200
{"content_id": "500f1b86-d4e3-4890-8ce2-b5b1351cf68a", "guess": "human", "label": "We think this was probably written by a human."}
// HTTP 200
{"content_id": "9b521ccb-2467-4ba5-8dc9-ec334a5c5b9b", "guess": "human", "label": "We think this was probably written by a human."}
// HTTP 200
{"content_id": "29471e82-200b-4d34-b8f6-02f8adc84d0f", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it."}
// HTTP 200
{"content_id": "d3dce521-6f45-4f63-a5f2-64a6bb35b79f", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it."}
```

### Appeals

```json
// HTTP 200
{"content_id": "c09b6fe5-8e3c-4308-9be2-a9bd180bc532", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "500f1b86-d4e3-4890-8ce2-b5b1351cf68a", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "9b521ccb-2467-4ba5-8dc9-ec334a5c5b9b", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "29471e82-200b-4d34-b8f6-02f8adc84d0f", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "d3dce521-6f45-4f63-a5f2-64a6bb35b79f", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
```

### /log entries for these content_ids

```json
{"combined_score": 0.4257, "confidence": 0.1486, "content_id": "c09b6fe5-8e3c-4308-9be2-a9bd180bc532", "creator_id": "appeal_after_r1", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "model_score": 0.6014, "status": "decided", "style_score": 0.25, "timestamp": "2026-11-07T16:33:14+00:00"}
{"content_id": "c09b6fe5-8e3c-4308-9be2-a9bd180bc532", "creator_id": "appeal_after_r1", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:16+00:00"}
{"combined_score": 0.312, "confidence": 0.376, "content_id": "500f1b86-d4e3-4890-8ce2-b5b1351cf68a", "creator_id": "appeal_after_r1", "guess": "human", "label": "We think this was probably written by a human.", "model_score": 0.3398, "status": "decided", "style_score": 0.2841, "timestamp": "2026-11-07T16:33:14+00:00"}
{"content_id": "500f1b86-d4e3-4890-8ce2-b5b1351cf68a", "creator_id": "appeal_after_r1", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:16+00:00"}
{"combined_score": 0.3377, "confidence": 0.3246, "content_id": "9b521ccb-2467-4ba5-8dc9-ec334a5c5b9b", "creator_id": "appeal_after_r1", "guess": "human", "label": "We think this was probably written by a human.", "model_score": 0.4038, "status": "decided", "style_score": 0.2717, "timestamp": "2026-11-07T16:33:15+00:00"}
{"content_id": "9b521ccb-2467-4ba5-8dc9-ec334a5c5b9b", "creator_id": "appeal_after_r1", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:16+00:00"}
{"combined_score": 0.4023, "confidence": 0.1954, "content_id": "29471e82-200b-4d34-b8f6-02f8adc84d0f", "creator_id": "appeal_after_r1", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "model_score": 0.5206, "status": "decided", "style_score": 0.2841, "timestamp": "2026-11-07T16:33:15+00:00"}
{"content_id": "29471e82-200b-4d34-b8f6-02f8adc84d0f", "creator_id": "appeal_after_r1", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:17+00:00"}
{"combined_score": 0.4967, "confidence": 0.0066, "content_id": "d3dce521-6f45-4f63-a5f2-64a6bb35b79f", "creator_id": "appeal_after_r1", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "model_score": 0.7434, "status": "decided", "style_score": 0.25, "timestamp": "2026-11-07T16:33:16+00:00"}
{"content_id": "d3dce521-6f45-4f63-a5f2-64a6bb35b79f", "creator_id": "appeal_after_r1", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:17+00:00"}
```

### Made-up content_id

```json
// HTTP 404
{"error": "not_found", "message": "No submission found with content_id 'made-up-id-r1-0000'."}
```

Log entry count before the fake appeal: 435, after: 435.

**Trial 1: 5/5 appeals returned 200 under_review · 5/5 have decided then under_review in /log · fake id → 404 · log grew by 0 · PASS**

## Trial 2 (creator_id `appeal_after_r2`)

### Submissions

```json
// HTTP 200
{"content_id": "6c310f2b-3ead-4297-b1d6-c8cab04438bd", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it."}
// HTTP 200
{"content_id": "b4aa4c06-2c4d-416d-8293-56693f52f986", "guess": "human", "label": "We think this was probably written by a human."}
// HTTP 200
{"content_id": "3a0406bd-3803-49ed-9c56-33bb02c0532b", "guess": "human", "label": "We think this was probably written by a human."}
// HTTP 200
{"content_id": "23d7c228-7431-4f08-a962-e4e19e584158", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it."}
// HTTP 200
{"content_id": "953df316-665e-4d8c-a3ba-695ca635c4f9", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it."}
```

### Appeals

```json
// HTTP 200
{"content_id": "6c310f2b-3ead-4297-b1d6-c8cab04438bd", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "b4aa4c06-2c4d-416d-8293-56693f52f986", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "3a0406bd-3803-49ed-9c56-33bb02c0532b", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "23d7c228-7431-4f08-a962-e4e19e584158", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "953df316-665e-4d8c-a3ba-695ca635c4f9", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
```

### /log entries for these content_ids

```json
{"combined_score": 0.4257, "confidence": 0.1486, "content_id": "6c310f2b-3ead-4297-b1d6-c8cab04438bd", "creator_id": "appeal_after_r2", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "model_score": 0.6014, "status": "decided", "style_score": 0.25, "timestamp": "2026-11-07T16:33:18+00:00"}
{"content_id": "6c310f2b-3ead-4297-b1d6-c8cab04438bd", "creator_id": "appeal_after_r2", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:20+00:00"}
{"combined_score": 0.312, "confidence": 0.376, "content_id": "b4aa4c06-2c4d-416d-8293-56693f52f986", "creator_id": "appeal_after_r2", "guess": "human", "label": "We think this was probably written by a human.", "model_score": 0.3398, "status": "decided", "style_score": 0.2841, "timestamp": "2026-11-07T16:33:18+00:00"}
{"content_id": "b4aa4c06-2c4d-416d-8293-56693f52f986", "creator_id": "appeal_after_r2", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:20+00:00"}
{"combined_score": 0.3377, "confidence": 0.3246, "content_id": "3a0406bd-3803-49ed-9c56-33bb02c0532b", "creator_id": "appeal_after_r2", "guess": "human", "label": "We think this was probably written by a human.", "model_score": 0.4038, "status": "decided", "style_score": 0.2717, "timestamp": "2026-11-07T16:33:19+00:00"}
{"content_id": "3a0406bd-3803-49ed-9c56-33bb02c0532b", "creator_id": "appeal_after_r2", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:20+00:00"}
{"combined_score": 0.4023, "confidence": 0.1954, "content_id": "23d7c228-7431-4f08-a962-e4e19e584158", "creator_id": "appeal_after_r2", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "model_score": 0.5206, "status": "decided", "style_score": 0.2841, "timestamp": "2026-11-07T16:33:19+00:00"}
{"content_id": "23d7c228-7431-4f08-a962-e4e19e584158", "creator_id": "appeal_after_r2", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:20+00:00"}
{"combined_score": 0.4967, "confidence": 0.0066, "content_id": "953df316-665e-4d8c-a3ba-695ca635c4f9", "creator_id": "appeal_after_r2", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "model_score": 0.7434, "status": "decided", "style_score": 0.25, "timestamp": "2026-11-07T16:33:20+00:00"}
{"content_id": "953df316-665e-4d8c-a3ba-695ca635c4f9", "creator_id": "appeal_after_r2", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:21+00:00"}
```

### Made-up content_id

```json
// HTTP 404
{"error": "not_found", "message": "No submission found with content_id 'made-up-id-r2-0000'."}
```

Log entry count before the fake appeal: 445, after: 445.

**Trial 2: 5/5 appeals returned 200 under_review · 5/5 have decided then under_review in /log · fake id → 404 · log grew by 0 · PASS**

## Trial 3 (creator_id `appeal_after_r3`)

### Submissions

```json
// HTTP 200
{"content_id": "e8b2391e-b0c4-4a13-9489-61c033708075", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it."}
// HTTP 200
{"content_id": "693d06b9-2c86-4bc1-a438-f904203af2ca", "guess": "human", "label": "We think this was probably written by a human."}
// HTTP 200
{"content_id": "38b1bff6-655d-4299-802a-056fdd2208e5", "guess": "human", "label": "We think this was probably written by a human."}
// HTTP 200
{"content_id": "cbbbd12e-09c9-4ec3-ab1b-e5e011c725de", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it."}
// HTTP 200
{"content_id": "156316cf-56b4-4e5f-a125-c097d0468732", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it."}
```

### Appeals

```json
// HTTP 200
{"content_id": "e8b2391e-b0c4-4a13-9489-61c033708075", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "693d06b9-2c86-4bc1-a438-f904203af2ca", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "38b1bff6-655d-4299-802a-056fdd2208e5", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "cbbbd12e-09c9-4ec3-ab1b-e5e011c725de", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
// HTTP 200
{"content_id": "156316cf-56b4-4e5f-a125-c097d0468732", "message": "Your appeal has been recorded, and this result is now under review.", "status": "under_review"}
```

### /log entries for these content_ids

```json
{"combined_score": 0.4257, "confidence": 0.1486, "content_id": "e8b2391e-b0c4-4a13-9489-61c033708075", "creator_id": "appeal_after_r3", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "model_score": 0.6014, "status": "decided", "style_score": 0.25, "timestamp": "2026-11-07T16:33:22+00:00"}
{"content_id": "e8b2391e-b0c4-4a13-9489-61c033708075", "creator_id": "appeal_after_r3", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:24+00:00"}
{"combined_score": 0.312, "confidence": 0.376, "content_id": "693d06b9-2c86-4bc1-a438-f904203af2ca", "creator_id": "appeal_after_r3", "guess": "human", "label": "We think this was probably written by a human.", "model_score": 0.3398, "status": "decided", "style_score": 0.2841, "timestamp": "2026-11-07T16:33:22+00:00"}
{"content_id": "693d06b9-2c86-4bc1-a438-f904203af2ca", "creator_id": "appeal_after_r3", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:24+00:00"}
{"combined_score": 0.3377, "confidence": 0.3246, "content_id": "38b1bff6-655d-4299-802a-056fdd2208e5", "creator_id": "appeal_after_r3", "guess": "human", "label": "We think this was probably written by a human.", "model_score": 0.4038, "status": "decided", "style_score": 0.2717, "timestamp": "2026-11-07T16:33:23+00:00"}
{"content_id": "38b1bff6-655d-4299-802a-056fdd2208e5", "creator_id": "appeal_after_r3", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:24+00:00"}
{"combined_score": 0.4023, "confidence": 0.1954, "content_id": "cbbbd12e-09c9-4ec3-ab1b-e5e011c725de", "creator_id": "appeal_after_r3", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "model_score": 0.5206, "status": "decided", "style_score": 0.2841, "timestamp": "2026-11-07T16:33:23+00:00"}
{"content_id": "cbbbd12e-09c9-4ec3-ab1b-e5e011c725de", "creator_id": "appeal_after_r3", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:24+00:00"}
{"combined_score": 0.4967, "confidence": 0.0066, "content_id": "156316cf-56b4-4e5f-a125-c097d0468732", "creator_id": "appeal_after_r3", "guess": "unsure", "label": "We couldn't tell whether this was written by a human or with AI. Writing like this can go either way, so we won't draw a conclusion about it.", "model_score": 0.7434, "status": "decided", "style_score": 0.25, "timestamp": "2026-11-07T16:33:23+00:00"}
{"content_id": "156316cf-56b4-4e5f-a125-c097d0468732", "creator_id": "appeal_after_r3", "event": "appeal", "reasoning": "I wrote this myself.", "status": "under_review", "timestamp": "2026-11-07T16:33:25+00:00"}
```

### Made-up content_id

```json
// HTTP 404
{"error": "not_found", "message": "No submission found with content_id 'made-up-id-r3-0000'."}
```

Log entry count before the fake appeal: 455, after: 455.

**Trial 3: 5/5 appeals returned 200 under_review · 5/5 have decided then under_review in /log · fake id → 404 · log grew by 0 · PASS**

