import random
import streamlit as st

st.set_page_config(page_title="Climate Quiz (Smart Feedback)", layout="centered")
st.title("🌍 Climate Change Quiz")
st.caption(
    "Choose 5 / 10 / 15 questions. If you answer correctly, you'll move on automatically. "
    "If you answer incorrectly, you'll see the correct answer + explanation, then click Next."
)

# ----------------------------
# Question bank (24 questions)
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
            "It forms the Hadley Cell, which exists in both hemispheres. The Ferrel Cell is in the mid-latitude."
            "while the Polar Cell is in the high-latitude."
        ),
    },
{
        "id": 19,
        "q": "What weather system is the typhoon from?",
        "options": {"A": "Cyclone", "B": "Anti-cyclone", "C": "Cold Front", "D": "Warm Front"},
        "answer": "A",
        "explanation": (
            """ The typhoon is generated from a low-pressure center in the atmosphere above the warm ocean surface.
		As the surrounding atmosphere is relatively high-pressure, the air spirals inward and convects upward, 
		forming a lot of rain. Such a convection is called a cyclone."""
        ),
    },
{
        "id": 20,
        "q": "How can we best define the latitude of 60 °?",
        "options": {"A": "Cold and dry", "B": "Cold and wet", "C": "Hot and dry", "D": "Hot and wet"},
        "answer": "B",
        "explanation": (
            """This is a relatively high latitude, so certainly it is cold. It is also under the upward limb of the 
		Ferrel Cell, where the air convects upward and forms a low-pressure zone. The moisture condenses and 
		forms precipitation. This latitude is called the Subpolar Low."""
        ),
    },
{
        "id": 21,
        "q": "What is an advantage of a monsoonal climate for agriculture?",
        "options": {"A": "It rains a lot", "B": "It is warm enough", "C": "It brings warmth and rain at the same time"},
        "answer": "C",
        "explanation": (
            """In a monsoon climate, the rainy season and the warm season happen at the same time.
		This is good for crops because plants need both heat and water to grow.
		Warm temperatures help crops grow faster, and frequent rain provides enough water for roots and leaves.
		When rain and heat come together, crops can grow strong without needing much artificial irrigation. """
        ),
    },
{
        "id": 22,
        "q": "Which of the following approaches cannot result in a low-carbon world?",
        "options": {"A": "Promote the use of electric vehicles", "B": "Expand green areas", "C": "Eat genetically produced meat","D":"Use Big Data substantially"},
        "answer": "D",
        "explanation": (
            """Big Data needs many computers and data centers, which use a lot of electricity.
		If this electricity comes from fossil fuels, carbon emissions will increase.
		So Big Data alone cannot create a low-carbon world."""
        ),
    },
{
        "id": 23,
        "q": "Why is deep seawater colder than shallow seawater?",
        "options": {"A": "Surface water can receive sunlight, while deep water cannot", "B": "Cold water is heavier (higher density), so it will sink", "C": "Human activities warm up the sea surface","D":"Both A and B"},
        "answer": "D",
        "explanation": (
            """Deep seawater is colder for two main reasons.
		First, sunlight mainly heats the surface of the ocean, and very little sunlight can reach deep water.
		Second, cold water is denser (heavier) than warm water, so it sinks to the bottom of the ocean.
		As a result, deep seawater stays cold while surface water is warmer."""
        ),
    },
{
        "id": 24,
        "q": "What is the difference between randomness and chaos?",
        "options": {"A": "Randomness is completely unpredictable, while chaos is unpredictable because it has no rules.",
 			"B": "Randomness follows clear physical laws, while chaos does not.", 
			"C": "Randomness has no underlying order, while chaos follows deterministic rules but is very sensitive to initial conditions.",
			"D":"There is no difference between randomness and chaos."},
        "answer": "C",
        "explanation": (
            """Randomness means there is no clear pattern or rule behind the behavior, 
		so the outcome cannot be predicted even in theory.
		Chaos, however, follows deterministic physical laws, 
		but very small differences in initial conditions can lead to very different results.
		Because we can never measure initial conditions perfectly, 
		chaotic systems appear unpredictable, even though they are not truly random."""
        ),
    }，
{
        "id": 25,
        "q": "Which of the following if the major energy source in the troposphere?",
        "options": {"A": "Solar Radiation",
 			"B": "Longwave radiation from Earth's surface", 
			"C": "Atmospheric back radiation"},
        "answer": "B",
        "explanation": (
            """That is why in troposphere, cold air is at the top while warm air at the bottom."""
        ),
    },
{
        "id": 26,
        "q": "What is a feature of the stratosphere?",
        "options": {"A": "Ozone layer",
 			"B": "Nitrogen layer", 
			"C": "Oxygen layer",
			"D":"Carbon dioxide layer"},
        "answer": "A",
        "explanation": (
            """The ozone layer can prevent ultraviolet radiation from harming people’s health."""
        ),
    },
{
        "id": 27,
        "q": "What is a characteristic of infrared radiation?",
        "options": {"A": "High frequency",
 			"B": "High intensity", 
			"C": "Long wavelength",
			"D":"High speed"},
        "answer": "C",
        "explanation": (
            """IR has a lower frequency than visible lights. Thus, it has longer wavelength and lower intensity. """
        ),
    },
{
        "id": 28,
        "q": "What is a characteristic of ultraviolet radiation?",
        "options": {"A": "Low frequency",
 			"B": "High intensity", 
			"C": "Long wavelength",
			"D":"Low speed"},
        "answer": "B",
        "explanation": (
            """UV has a higher frequency than visible lights. Thus, it has shorter wavelength and higher intensity. """
        ),
    },
{
        "id": 29,
        "q": "Which of the following has the highest frequency?",
        "options": {"A": "Radiowave",
 			"B": "Visible light", 
			"C": "Gamma ray",
			"D":"X ray"},
        "answer": "C",
        "explanation": (
            """From high frequency to low frequency: Gamma Ray, X Ray, Visible Light, Radiowave."""
        ),
    },
{
        "id": 30,
        "q": "When water decreases from 10oC to -10oC, what happens?",
        "options": {"A":"It releases both latent heat and sensible heat",
 			"B": "It releases only sensible heat", 
			"C": "It releases onlt latent heat",
			"D":"It releases latent heat but absorbs sensible heat"},
        "answer": "A",
        "explanation": (
            """
                Because temperature decreases, it releases sensible heat; 
                because phase also changes (liquid-solid), latent heat is also released. 
"""
        ),
    }
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

# When a user answers wrong, we "lock" the question and show explanation until they click Next.
if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False

# Store last wrong feedback to render explanation on rerun
if "last_wrong_info" not in st.session_state:
    # {"correct_letter": "B", "correct_text": "...", "explanation": "..."}
    st.session_state.last_wrong_info = None

# For stable radio selection
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None


def start_quiz(n: int):
    n = min(n, len(QUESTION_BANK))
    st.session_state.quiz_questions = random.sample(QUESTION_BANK, k=n)
    st.session_state.quiz_started = True
    st.session_state.idx = 0
    st.session_state.correct = 0
    st.session_state.show_explanation = False
    st.session_state.last_wrong_info = None
    st.session_state.selected_option = None


def reset_quiz():
    st.session_state.quiz_started = False
    st.session_state.quiz_questions = []
    st.session_state.idx = 0
    st.session_state.correct = 0
    st.session_state.show_explanation = False
    st.session_state.last_wrong_info = None
    st.session_state.selected_option = None


def go_next_question():
    st.session_state.idx += 1
    st.session_state.show_explanation = False
    st.session_state.last_wrong_info = None
    st.session_state.selected_option = None


# ----------------------------
# Sidebar: Setup
# ----------------------------
with st.sidebar:
    st.header("⚙️ Quiz Settings")
    n_questions = st.radio("Choose number of questions", [5, 10, 15,20,24], index=1)

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
    st.info("Choose 5 / 10 / 15 / 20 / 24 questions in the sidebar, then click **Start Quiz**.")
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

opt_keys = list(qobj["options"].keys())
opt_labels = [f"{k}. {qobj['options'][k]}" for k in opt_keys]

# Keep selection stable across reruns
default_index = 0
if st.session_state.selected_option in opt_keys:
    default_index = opt_keys.index(st.session_state.selected_option)

# If showing explanation (wrong answer), lock selection
choice_label = st.radio(
    "Select one:",
    opt_labels,
    index=default_index,
    key=f"radio_{qobj['id']}_{idx}",
    disabled=st.session_state.show_explanation,
)

selected_letter = choice_label.split(".")[0].strip()
st.session_state.selected_option = selected_letter

colA, colB = st.columns(2)

# Confirm button is disabled only when we are currently showing explanation
with colA:
    confirm = st.button("✅ Confirm", use_container_width=True, disabled=st.session_state.show_explanation)

# Next button only appears when explanation is being shown
with colB:
    next_btn = st.button("➡️ Next", use_container_width=True, disabled=not st.session_state.show_explanation)

# ----------------------------
# Confirm logic:
# - Correct: increment score, auto-advance to next question
# - Wrong: show correct answer + explanation, require clicking Next
# ----------------------------
if confirm:
    correct_letter = qobj["answer"]
    if selected_letter == correct_letter:
        st.session_state.correct += 1
        go_next_question()
        st.rerun()
    else:
        correct_text = f"{correct_letter}. {qobj['options'][correct_letter]}"
        explanation_text = qobj.get("explanation", "").strip()
        st.session_state.last_wrong_info = {
            "correct_letter": correct_letter,
            "correct_text": correct_text,
            "explanation": explanation_text,
        }
        st.session_state.show_explanation = True
        st.rerun()

# Show explanation only when wrong
if st.session_state.show_explanation and st.session_state.last_wrong_info:
    info = st.session_state.last_wrong_info
    st.error(f"❌ Incorrect. The correct answer is **{info['correct_text']}**.")
    if info["explanation"]:
        st.markdown("**Explanation:**")
        st.write(info["explanation"])
    st.caption("Click **Next** to continue.")

if next_btn:
    go_next_question()
    st.rerun()
