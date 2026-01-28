import random
import streamlit as st

st.set_page_config(page_title="Climate Quiz (with Explanations)", layout="centered")
st.title("🌍 Climate Change Quiz")
st.caption("Choose 5 / 10 / 15 questions. After each answer, you'll see correctness, the correct answer, and an explanation.")

# ----------------------------
# Question bank (18 questions)
# ----------------------------
QUESTION_BANK = [
    {
        "id": 1,
        "q": "When was the Paris Agreement signed?",
        "options": {"A": "2005", "B": "2015", "C": "2025", "D": "1995"},
        "answer": "B",
        "explanation": (
            "The agreement was adopted by 195 members of the UN Climate Change Conference in Paris in "
            "December 2015, and was enforced in November 2016."
        ),
    },
    {
        "id": 2,
        "q": "Which of the following is NOT a greenhouse gas?",
        "options": {"A": "CO2", "B": "O3", "C": "H2O", "D": "N2"},
        "answer": "C",
        "explanation": (
            "Being the most abundant gas in the atmosphere, nitrogen is not a greenhouse gas (GHG). "
            "Other examples of GHG include CH4 and NOx."
        ),
    },
    {
        "id": 3,
        "q": "When does the Paris Agreement aim to reach carbon neutrality globally?",
        "options": {"A": "2045", "B": "2050", "C": "2055", "D": "2060"},
        "answer": "B",
        "explanation": (
            "The goal of the Paris Agreement is to limit the rise in temperature to 2°C by 2100 - and if possible "
            "1.5°C – in order to achieve carbon neutrality by 2050."
        ),
    },
    {
        "id": 4,
        "q": "The current CO2 level is about what level?",
        "options": {"A": "410 ppm", "B": "415 ppm", "C": "420 ppm", "D": "425 ppm"},
        "answer": "D",
        "explanation": (
            "The pre-industrial level is 280 ppm, while currently it is 428 ppm (https://keelingcurve.ucsd.edu). "
            "It is keeping rising."
        ),
    },
    {
        "id": 5,
        "q": "What impacts will global warming bring to the global rain patterns?",
        "options": {
            "A": "Dry place drier, wet place wetter",
            "B": "Dry place drier, wet place drier",
            "C": "Dry place wetter, wet place wetter",
            "D": "Dry place wetter, wet place drier",
        },
        "answer": "A",
        "explanation": (
            "Global warming will intensify air convection and accelerate the water cycle. It won't alter the "
            "convection or the precipitation pattern, but will only intensify it. Thus, the spatial distribution pattern "
            "will be more uneven, and the occurrence of extreme weather will rise."
        ),
    },
    {
        "id": 6,
        "q": "What is the curve that shows how the atmospheric CO2 level changes over time called?",
        "options": {
            "A": "The Stefan Curve",
            "B": "The Moho Curve",
            "C": "The Bjerneks Curve",
            "D": "The Keeling Curve",
        },
        "answer": "D",
        "explanation": (
            "The Keeling Curve is a daily record of global atmospheric carbon dioxide concentration maintained "
            "by Scripps Institution of Oceanography at UC San Diego. They were started by C. David Keeling in "
            "March 1958.\n"
            "You can visit this site to view the curve: https://keelingcurve.ucsd.edu"
        ),
    },
    {
        "id": 7,
        "q": "Which institution is responsible for updating the Keeling Curve?",
        "options": {"A": "UCSB", "B": "UCSD", "C": "UCLA", "D": "UCB"},
        "answer": "B",
        "explanation": (
            "The Keeling Curve is a daily record of global atmospheric carbon dioxide concentration maintained "
            "by Scripps Institution of Oceanography at UC San Diego. They were started by C. David Keeling in "
            "March 1958.\n"
            "You can visit this site to view the curve: https://keelingcurve.ucsd.edu"
        ),
    },
    {
        "id": 8,
        "q": "Which part of the world experiences the most global warming?",
        "options": {
            "A": "The equator",
            "B": "The subtropical high",
            "C": "The subpolar low",
            "D": "The two poles",
        },
        "answer": "D",
        "explanation": (
            "Because of the positive feedback brought by icesheets (albedo effect), the higher the latitude is, "
            "the larger the extent of warming a place will experience."
        ),
    },
    {
        "id": 9,
        "q": "When El Niño arrives, which part of the Pacific Ocean will become warmer?",
        "options": {"A": "The West Coast", "B": "The East Coast", "C": "Both", "D": "Neither"},
        "answer": "B",
        "explanation": (
            "During El Niño, warm water in the Pacific Ocean moves from the western Pacific toward the eastern "
            "Pacific. This makes the ocean near the west coast of the Americas (the eastern Pacific) warmer than "
            "usual, while the western Pacific becomes relatively cooler."
        ),
    },
    {
        "id": 10,
        "q": "When La Niña arrives, which part of the Pacific Ocean will become warmer?",
        "options": {"A": "The West Coast", "B": "The East Coast", "C": "Both", "D": "Neither"},
        "answer": "A",
        "explanation": (
            "During La Niña, strong trade winds push warm surface water toward the western Pacific. This makes "
            "the ocean near Asia and Australia (the western Pacific) warmer, while the eastern Pacific becomes "
            "cooler than usual."
        ),
    },
    {
        "id": 11,
        "q": "Others being equal, which night will be warmer?",
        "options": {"A": "Cloudy night", "B": "Clear-sky night", "C": "Same", "D": "No fixed answer"},
        "answer": "A",
        "explanation": (
            "Clouds act like a blanket for the Earth. They trap heat and stop it from escaping into space, so the "
            "ground cools down more slowly. On a clear night, heat escapes easily, so it gets colder."
        ),
    },
    {
        "id": 12,
        "q": "An object can emit radiation that is proportional to",
        "options": {
            "A": "its temperature",
            "B": "the square of its temperature",
            "C": "the cube of its temperature",
            "D": "the quadruple of its temperature",
        },
        "answer": "D",
        "explanation": (
            "The amount of radiation an object emits increases very fast as the temperature rises. According to the "
            "Stefan-Boltzmann law, the energy emitted is proportional to the fourth power of its temperature, so "
            "even a small temperature increase can cause a big rise in radiation."
        ),
    },
    {
        "id": 13,
        "q": "When the air temperature rises, the amount of water vapor the air can hold without condensation will",
        "options": {
            "A": "increase exponentially",
            "B": "increase linearly",
            "C": "decrease exponentially",
            "D": "decrease exponentially",
        },
        "answer": "A",
        "explanation": (
            "Warm air can hold much more water vapor than cold air. As temperature rises, the air’s capacity for "
            "water vapor increases very quickly (not just in a straight line), which is why warmer climates often "
            "have heavier rain and stronger storms."
        ),
    },
    {
        "id": 14,
        "q": "Which of the following constitutes the vast majority of freshwater?",
        "options": {"A": "River", "B": "Groundwater", "C": "Glacier", "D": "Lake"},
        "answer": "C",
        "explanation": (
            "Glaciers contribute to 69% of the total freshwater on Earth. However, it is important to note that "
            "freshwater accounts for only ~3% of all water resources."
        ),
    },
    {
        "id": 15,
        "q": "Which of the following cannot magnify the global warming effect?",
        "options": {
            "A": "The solubility of CO2 in the ocean",
            "B": "The volcanic ashes in the atmosphere",
            "C": "The albedo of ice sheets",
        },
        "answer": "B",
        "explanation": (
            "The solubility decreases as the temperature increases. Thus, the ocean cannot store the same amount "
            "of CO2 as it could before under the circumstances of global warming. Some CO2 will re-enter the "
            "atmosphere and intensify the greenhouse effect. As the temperature increases, ice will melt. As ice "
            "sheets can reflect a large amount of solar radiation into space, a lack of ice sheets means that the "
            "ground has to absorb more solar radiation, so it gets warmer more rapidly. The volcanic ashes can "
            "partially block the solar radiation and prevent it from warming the ground."
        ),
    },
    {
        "id": 16,
        "q": "In the troposphere, as the altitude increases by 1km, the air temperature will decrease by",
        "options": {"A": "5.5 °C", "B": "6.0 °C", "C": "6.5 °C", "D": "7.0 °C"},
        "answer": "C",
        "explanation": "This is the lapse rate: -6.5 °C/km.",
    },
    {
        "id": 17,
        "q": "What is the most significant feature of the Mediterranean Climate?",
        "options": {
            "A": "Warmth and rain throughout the year",
            "B": "Warm in summer, but rainy in winter",
            "C": "Never rains",
            "D": "Cooler than other places of the same latitude",
        },
        "answer": "B",
        "explanation": (
            "In the summer, such places are controlled by subpolar high pressure, which is hot and dry; in winter, "
            "it is dominated by the Westerlies from the ocean, bringing an abundance of moisture. The Mediterranean "
            "Climate exists around the western coast of the subtropical region, such as Spain and Italy."
        ),
    },
    {
        "id": 18,
        "q": "Where is the Hadley Cell?",
        "options": {"A": "In the low latitude", "B": "In the mid-latitude", "C": "In the high latitude"},
        "answer": "A",
        "explanation": (
            "Warm air rises from the equator and flows to 30°, where it condenses and flows back to the equator. "
            "It forms the Hadley Cell, which exists in both hemispheres. The Ferrel Cell is in the mid-latitude "
            "while the Polar Cell is in the high-latitude."
        ),
    },
]

# ----------------------------
# Session state init
# ----------------------------
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "last_feedback" not in st.session_state:
    # ("correct"/"wrong", correct_letter)
    st.session_state.last_feedback = None
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None


def start_quiz(n: int):
    if n > len(QUESTION_BANK):
        n = len(QUESTION_BANK)
    st.session_state.quiz_questions = random.sample(QUESTION_BANK, k=n)
    st.session_state.quiz_started = True
    st.session_state.idx = 0
    st.session_state.correct = 0
    st.session_state.answered = False
    st.session_state.last_feedback = None
    st.session_state.selected_option = None


def reset_quiz():
    st.session_state.quiz_started = False
    st.session_state.quiz_questions = []
    st.session_state.idx = 0
    st.session_state.correct = 0
    st.session_state.answered = False
    st.session_state.last_feedback = None
    st.session_state.selected_option = None


# ----------------------------
# Sidebar: Setup
# ----------------------------
with st.sidebar:
    st.header("⚙️ Quiz Settings")
    n_questions = st.radio("Choose number of questions", [5, 10, 15], index=1)

    if not st.session_state.quiz_started:
        if st.button("Start Quiz", use_container_width=True):
            start_quiz(n_questions)
    else:
        if st.button("Restart", use_container_width=True):
            reset_quiz()
            st.rerun()

# ----------------------------
# Main flow
# ----------------------------
if not st.session_state.quiz_started:
    st.info("Choose 5 / 10 / 15 questions in the sidebar, then click **Start Quiz**.")
    st.stop()

total = len(st.session_state.quiz_questions)
idx = st.session_state.idx

# Finish screen
if idx >= total:
    accuracy = st.session_state.correct / total if total else 0.0
    st.success("✅ Quiz Finished!")
    st.metric("Correct", f"{st.session_state.correct} / {total}")
    st.metric("Accuracy", f"{accuracy*100:.1f}%")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Restart (new random set)", use_container_width=True):
            reset_quiz()
            start_quiz(n_questions)
            st.rerun()
    with col2:
        if st.button("Back to setup", use_container_width=True):
            reset_quiz()
            st.rerun()

    st.stop()

# Current question
qobj = st.session_state.quiz_questions[idx]

st.subheader(f"Question {idx+1} / {total}")
st.write(f"**{qobj['q']}**")

# Display options
opt_keys = list(qobj["options"].keys())
opt_labels = [f"{k}. {qobj['options'][k]}" for k in opt_keys]

# Keep selection stable across reruns
default_index = 0
if st.session_state.selected_option in opt_keys:
    default_index = opt_keys.index(st.session_state.selected_option)

choice_label = st.radio(
    "Select one:",
    opt_labels,
    index=default_index,
    key=f"radio_{qobj['id']}_{idx}",
    disabled=st.session_state.answered,
)

# Parse selected option letter from label "A. xxx"
selected_letter = choice_label.split(".")[0].strip()
st.session_state.selected_option = selected_letter

# Submit / Next buttons
colA, colB = st.columns(2)

with colA:
    submit = st.button("✅ Confirm", use_container_width=True, disabled=st.session_state.answered)

with colB:
    next_q = st.button("➡️ Next", use_container_width=True, disabled=not st.session_state.answered)

if submit:
    correct_letter = qobj["answer"]
    if selected_letter == correct_letter:
        st.session_state.correct += 1
        st.session_state.last_feedback = ("correct", correct_letter)
    else:
        st.session_state.last_feedback = ("wrong", correct_letter)

    st.session_state.answered = True
    st.rerun()

# Feedback block (after submit)
if st.session_state.answered and st.session_state.last_feedback is not None:
    status, correct_letter = st.session_state.last_feedback
    correct_text = f"{correct_letter}. {qobj['options'][correct_letter]}"
    explanation_text = qobj.get("explanation", "").strip()

    if status == "correct":
        st.success(f"✅ Correct! The answer is **{correct_text}**.")
    else:
        st.error(f"❌ Incorrect. The correct answer is **{correct_text}**.")

    if explanation_text:
        st.markdown("**Explanation:**")
        st.write(explanation_text)

    st.caption("Click **Next** to continue.")

if next_q:
    st.session_state.idx += 1
    st.session_state.answered = False
    st.session_state.last_feedback = None
    st.session_state.selected_option = None
    st.rerun()