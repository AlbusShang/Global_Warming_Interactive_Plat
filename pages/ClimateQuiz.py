import random
import streamlit as st

st.set_page_config(page_title="Climate Quiz", layout="centered")
st.title("🌍 Climate Change Quiz")

# ----------------------------
# Question bank (18 questions)
# ----------------------------
QUESTION_BANK = [
    {
        "id": 1,
        "q": "When was the Paris Agreement signed?",
        "options": {"A": "2005", "B": "2015", "C": "2025", "D": "1995"},
        "answer": "B",
    },
    {
        "id": 2,
        "q": "Which of the following is NOT a greenhouse gas?",
        "options": {"A": "CO2", "B": "O3", "C": "H2O", "D": "N2"},
        "answer": "C",
    },
    {
        "id": 3,
        "q": "When does the Paris Agreement aim to reach carbon neutrality globally?",
        "options": {"A": "2045", "B": "2050", "C": "2055", "D": "2060"},
        "answer": "B",
    },
    {
        "id": 4,
        "q": "The current CO2 level is about what level?",
        "options": {"A": "410 ppm", "B": "415 ppm", "C": "420 ppm", "D": "425 ppm"},
        "answer": "D",
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
    },
    {
        "id": 7,
        "q": "Which institution is responsible for updating the Keeling Curve?",
        "options": {"A": "UCSB", "B": "UCSD", "C": "UCLA", "D": "UCB"},
        "answer": "B",
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
    },
    {
        "id": 9,
        "q": "When El Niño arrives, which part of the Pacific Ocean will become warmer?",
        "options": {"A": "The West Coast", "B": "The East Coast", "C": "Both", "D": "Neither"},
        "answer": "B",
    },
    {
        "id": 10,
        "q": "When La Niña arrives, which part of the Pacific Ocean will become warmer?",
        "options": {"A": "The West Coast", "B": "The East Coast", "C": "Both", "D": "Neither"},
        "answer": "A",
    },
    {
        "id": 11,
        "q": "Others being equal, which night will be warmer?",
        "options": {"A": "Cloudy night", "B": "Clear-sky night", "C": "Same", "D": "No fixed answer"},
        "answer": "A",
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
    },
    {
        "id": 14,
        "q": "Which of the following attributes to the majority of freshwater in the world?",
        "options": {"A": "River", "B": "Groundwater", "C": "Glacier", "D": "Lake"},
        "answer": "C",
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
    },
    {
        "id": 16,
        "q": "In the troposphere, as the altitude increases by 1km, the air temperature will decrease by",
        "options": {"A": "5.5 °C", "B": "6.0 °C", "C": "6.5 °C", "D": "7.0 °C"},
        "answer": "C",
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
    },
    {
        "id": 18,
        "q": "Where is the Hadley Cell?",
        "options": {"A": "In the low latitude", "B": "In the mid-latitude", "C": "In the high latitude"},
        "answer": "A",
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
    st.session_state.last_feedback = None
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None


def start_quiz(n: int):
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
# UI: Quiz setup
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

    if status == "correct":
        st.success(f"✅ Correct! The answer is **{correct_text}**.")
    else:
        st.error(f"❌ Incorrect. The correct answer is **{correct_text}**.")

    st.caption("Click **Next** to continue.")

if next_q:
    st.session_state.idx += 1
    st.session_state.answered = False
    st.session_state.last_feedback = None
    st.session_state.selected_option = None
    st.rerun()
