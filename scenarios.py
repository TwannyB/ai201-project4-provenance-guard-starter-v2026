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

HUMAN_ONE = "On late Friday nights, I remember the magic that accompanied the enthralling news that my brothers and I would be permitted to spend the night at our Mom mom’s house. Usually, my brothers and I would privately convene beforehand to decide which one of us would be tasked with asking our parents, and more often than not, my younger brother would be assigned the duty. My older brother and I would then eavesdrop from behind the stair banister to hear the answer: we would be permitted to spend the night if we finished all of our household chores before midnight, which was when our grandmother’s bedtime was. On some nights, we’d already finished said chores and were able to leave as soon as we’d packed our bags. On other nights, we cleaned, vacuumed, and washed dishes with maximum efficiency, determined to make it to the oasis that was our Mom mom’s house."
HUMAN_TWO = "Following an anticipation filled car ride under the stars, we’d arrive at our destination: a quaint, two story house right at the tree-lined bend of a quiet neighborhood. From the top of the uphill driveway, the golden porch-lights would shine as a beacon, signaling a welcome. Inside the house on the first floor first awaited the foyer. The same foyer had enclosed countless hello and goodbye hugs between family members, exciting departures for vacations, sleepy afternoon returns from the neighborhood playground and park, the commencement of hide and seek games with cousins, and victorious homecomings from track meets."
HUMAN_THREE = "Also on the first floor was the kitchen, which had a refrigerator covered with baby and childhood family pictures, an oven that had baked dozens of Ellio’s pizzas, a counter with potholders that had supported pans of macaroni and cheese and peach cobbler, a microwave that had heated leftovers and popcorn for movie nights, and a snack table filled with our favorite snacks and beverages. On Saturday mornings, the kitchen emanated the smell of cooked bacon and french toast, which snuck its way up stairs and under doors to reach every room in the house."
HUMAN_FOUR = "Bordering both the kitchen and foyer was the conjoined dining room and living room. The living room was where we’d unwrapped gifts on various Christmases, played chess, and hid under the table during hide and seek games. Also in the living room was the piano that my songwriting uncle had learned to play on, the antique grandfather clock, the shelf full of photos of my mother and her siblings as teenagers, and the long sofa that had been present in numerous family photos. It was in the dining room that we’d eaten holiday meals, cut birthday cakes, and stored desserts. "
HUMAN_FIVE = "	On the second floor of the house are two bathrooms, the computer room, and the bedrooms of my mother, her siblings, and my grandparents. When spending the night at our grandparents’ house, we’d most often sleep in our mother’s bedroom, which had stacks of books by the wall that our grandmother would read to us, suitcases awaiting the next family vacation inside the sliding door closet, a wooden vanity, and my mother’s violin from high school, which was tucked under a pink and white sheeted bed with flower engravings on the wooden headboard."
HUMAN_SIX = "Perpendicular to my mother’s room is the computer room, which was doubled as my grandfather’s office and game room, where he won online chess and stored his bowling gear. The desk and table in the room held a few trinkets from his time as an Army Lieutenant Colonel in Vietnam, while a painting from Vietnam hung on the wall, serving as a reminder of his service. For my brothers and cousins and I, the room was where we watched anime and played computer games."
HUMAN_SEVEN = "	In the poem, McGrath reiterates that indoctrination is deeply embedded in the practice of war. Consistently, McGrath addresses the deceased soldier the ode is addressed to with a seemingly omniscient insight into their experiences and thoughts. In the poem’s beginning, he hyperbolizes the devotion of the soldier to his country by describing the soldier as “perfectly ready to kill / the world and [their] brother,” (McGrath 8-9). Through the exaggeration, McGrath communicates that the soldier’s devotion is not only unwavering and extreme, but illogical to the extent that they would kill their own kin for the sake of their country. In the second stanza, McGrath continues to magnify the devotion of the soldier with natural imagery:"


MY_PLAIN = "Furthermore, McGrath asserts that ignorance is the effect of indoctrination, but is regarded in American society as bravery. In the second stanza’s line: “No scholar put your thinking cap on,” childish, colloquial diction paints an image of the soldier in a classroom as a student (McGrath 23). Through the image of the soldier being without a “thinking cap”, McGrath establishes that the soldiers are not only loyal to their orders, but altogether incapable of “thinking”, and therefore grounded in their ignorance. The permeating motif of ignorance in the poem is often linked to bravery as a concept and its existence as merely an illusion. In the poem’s opening, the speaker tells the soldier that “All [of their] false flags were / Of bravery and ignorance” (McGrath 4-5). In the two lines, the contradictory symbol of a false flag is utilized to portray courage and pride, as are usually associated with a flag, intermixed with the notion of the flag being a pretense. Together, the ideas present that the soldier’s bravery and pride aren’t genuine or reasonable, but purely a result of ignorance and conformity to their society’s beliefs. The same idea of bravery’s illusory presence is reiterated through the metaphorical contradiction of the soldier possessing “scarecrow valor” (McGrath 34). Similar to a scarecrow’s falsity, the bravery of a soldier is fake with the sole purpose of convincing others. Via McGrath's recurring notion of ignorance leading to a false portrayal of bravery, he communicates that the gallantry exhibited by the soldier is nothing more than a form of disguised ignorance."

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

EDITED_AI_2 = "I agree with Jones and found the article insightful because I’ve never seen or heard of Latimore’s painting or the reaction to it. I’m familiar with the stereotypical image of Jesus with brown hair, blue eyes, and white skin and see how repeatedly seeing the image can shape what people subconsciously believe Jesus looked like. Some people might think the author is overreacting or thinking too deeply about it, but I think familiar images can carry racial meanings that we do not always notice. If Jesus is repeatedly depicted as white, people may eventually draw a connection between whiteness, divinity, and purity, even without consciously intending to. That connection often inadvertently comes with the connection of darker skin and impurity of ungodliness. This connects to the article about Russell Moore because both readings show how people’s existing cultural and political loyalties can influence their faith. "

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
            HUMAN_ONE,
            HUMAN_TWO,
            HUMAN_THREE,
            HUMAN_FOUR,
            HUMAN_FIVE,
            HUMAN_SIX,
            HUMAN_SEVEN,
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
            HUMAN_ONE,
            HUMAN_TWO,
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
            HUMAN_THREE,
            EDITED_AI,
            MY_PLAIN,
            EDITED_AI_2,
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
