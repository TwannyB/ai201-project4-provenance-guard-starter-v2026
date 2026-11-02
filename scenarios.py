"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

# ── Texts I wrote myself ─────────────────────────────────────────────────────

MY_CASUAL = (
    "I know. I’m looking at this in terms of exponential progress and technological "
    "escalation. There’s definitely a variation of this code that isn’t as agreeable out "
    "there.\n\n"
    "Remember the Will Smith eating spaghetti AI clip from 2014? Back then everybody laughed "
    "about it saying how silly AI looks, and in a little over a decades time, AI had become "
    "wayyy harder to differentiate from reality. \n\n"
    "I’m just thinking about when they inevitably decide to combine this with walking AI vessels"
)

MY_ESSAY = (
    "With a black composition notebook and a pencil, I scribbled out “prototypes” of my "
    "inventions. From practical appliances such as electric hand-warming gloves and portable "
    "power outlet cubes to fantastical imaginings including mind-reading robot servants and "
    "automatic kitchens, my seven-year-old mind was fascinated with inventing solutions to "
    "everyday problems. My parents, both holding bachelor's degrees in electrical engineering, "
    "encouraged this curiosity by introducing me to engineering and providing me with a "
    "children's electricity kit. Although many of my childhood inventions never progressed "
    "beyond the pages of my notebook, they sparked an interest in technological innovation "
    "that would eventually lead me to pursue computer science."
)

MY_PLAIN = (
    "I think AI is useful, but sometimes people exaggerate how much it's actually changing "
    "things. Like, sure, ChatGPT can write an essay in seconds, which is pretty impressive when "
    "you think about it. But that doesn't necessarily mean the essay is any good. I've noticed "
    "that AI tends to explain things in this weirdly polished way where every sentence sounds "
    "like it's trying to make some important point, even when there's not much being said. And "
    "I guess that's part of the problem. We're getting better at generating information, but "
    "I'm not sure we're getting better at understanding it. Maybe those are two completely "
    "different things."
)

# ── AI-generated texts ───────────────────────────────────────────────────────

# The sample built into detector.py.
AI_SAMPLE = (
    "The implementation of the proposed framework requires careful consideration of several "
    "key factors. First, it is important to note that the system must be able to handle a wide "
    "variety of different inputs. Additionally, the overall performance of the solution depends "
    "on a number of important variables."
)

# Written by Claude for this test set, unedited.
AI_TIME = (
    "Effective time management is an essential skill for students and professionals alike. By "
    "prioritizing tasks, setting clear goals, and minimizing distractions, individuals can "
    "significantly improve their productivity. Furthermore, regular breaks and adequate rest "
    "play a crucial role in maintaining focus over extended periods. Ultimately, developing "
    "strong time management habits not only enhances performance but also contributes to "
    "overall well-being and a healthier work-life balance."
)
AI_CLIMATE = (
    "Climate change represents one of the most pressing challenges facing humanity today. "
    "Rising global temperatures, shifting weather patterns, and increasing sea levels have "
    "far-reaching consequences for ecosystems and communities around the world. Addressing this "
    "issue requires a coordinated effort from governments, businesses, and individuals. By "
    "investing in renewable energy, promoting sustainable practices, and raising public "
    "awareness, society can work toward a more resilient and environmentally responsible future."
)
AI_READING = (
    "Reading offers numerous benefits that extend far beyond entertainment. It enhances "
    "vocabulary, improves concentration, and fosters critical thinking skills. Additionally, "
    "reading exposes individuals to diverse perspectives and cultures, which can promote empathy "
    "and understanding. Whether through novels, articles, or academic texts, engaging with "
    "written material on a regular basis can contribute to lifelong learning and personal growth."
)
AI_REMOTE = (
    "Remote work has transformed the modern workplace in significant ways. While it offers "
    "employees greater flexibility and eliminates lengthy commutes, it also presents unique "
    "challenges, such as maintaining clear communication and fostering a sense of team cohesion. "
    "Organizations that succeed in this environment typically invest in reliable digital tools "
    "and establish clear expectations. As a result, remote work can be both productive and "
    "rewarding when managed effectively."
)

# An AI paragraph I edited lightly.
EDITED_AI = (
    "Artificial intelligence has changed the way people approach everyday tasks, but I don't "
    "think everyone fully realizes the impact it has. For example, a lot of students use AI to "
    "summarize long readings, which is more efficient, but not completely the same as reading "
    "the original reading. There's also the question of how much people should rely on these "
    "tools. I use technology for all kinds of things, and sometimes it's genuinely helpful, but "
    "other times I wonder whether it's making certain tasks a little too easy. It's kind of like "
    "using a calculator before you've learned how to do basic math. You're still getting the "
    "answer, but you won't end up understanding the answers or where they came from. It can "
    "probably be argued that AI can be both good and bad. What really matters is that people "
    "know when it should be used."
)


SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        # Target: at most 1 of these 10 labelled high-confidence AI, every trial.
        "texts": [
            MY_CASUAL,
            MY_ESSAY,
            MY_PLAIN,
            "REPLACE ME with a paragraph you wrote yourself (4 of 10).",
            "REPLACE ME with a paragraph you wrote yourself (5 of 10).",
            "REPLACE ME with a paragraph you wrote yourself (6 of 10).",
            "REPLACE ME with a paragraph you wrote yourself (7 of 10).",
            "REPLACE ME with a paragraph you wrote yourself (8 of 10).",
            "REPLACE ME with a paragraph you wrote yourself (9 of 10).",
            "REPLACE ME with a paragraph you wrote yourself (10 of 10).",
        ],
    },
    {
        "name": "spread: known AI",
        "criterion": 2,
        # Compare the average combined_score here with the average from
        # "spread: known human". Target: AI average at least 0.45 higher.
        "texts": [AI_SAMPLE, AI_TIME, AI_CLIMATE, AI_READING, AI_REMOTE],
    },
    {
        "name": "spread: known human",
        "criterion": 2,
        "texts": [
            MY_CASUAL,
            MY_ESSAY,
            MY_PLAIN,
            "REPLACE ME with another paragraph you wrote yourself (4 of 5).",
            "REPLACE ME with another paragraph you wrote yourself (5 of 5).",
        ],
    },
    # Criterion 3 — the appeal path — is tested by hand with curl, because
    # run_eval.py only calls /submit: submit 5 texts, appeal each content_id,
    # check /log, and appeal one made-up id. Three times.
    {
        "name": "bad input",
        "criterion": 4,
        # Target: the five 400s and the one 413 below, never a 500, every trial.
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},             # 400
            {"text": "   \n  ", "creator_id": "eval_bad_whitespace"},  # 400
            {"creator_id": "eval_bad_missing"},                       # 400, no text field
            {"text": None, "creator_id": "eval_bad_null"},            # 400
            {"text": "Hello there", "creator_id": "eval_bad_short"},  # 400, two words
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},  # 413
        ],
    },
    {
        "name": "label coverage",
        "criterion": 5,
        # In order: 3 known-AI, 3 known-human, 3 borderline. Target: at least
        # one AI text gets "ai", one human text gets "human", and one
        # borderline text gets "unsure", every trial.
        "texts": [
            AI_SAMPLE,
            AI_TIME,
            AI_CLIMATE,
            MY_CASUAL,
            MY_ESSAY,
            "REPLACE ME with a third paragraph you wrote yourself.",
            EDITED_AI,
            MY_PLAIN,
            "REPLACE ME with another borderline text — e.g. a second AI paragraph you edit lightly.",
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
