# pages/climate_dictionary.py
# Streamlit multipage page: Climate Dictionary🔍

import re
import streamlit as st
from difflib import SequenceMatcher

st.set_page_config(page_title="Climate Dictionary🔍", page_icon="🔍", layout="wide")

# ----------------------------
# Data
# ----------------------------
TERMS = [
    {
        "term": "Keeling Curve",
        "definition": (
            "A curve that shows how the global atmospheric CO2 level is changing over time. "
            "C. David Keeling initially made the curve in March 1958. Currently, the UCSD "
            "Scripps Institute of Oceanography is responsible for updating the curve frequently. "
            "The curve can be viewed at https://keelingcurve.ucsd.edu."
        ),
        "tags": ["CO2", "atmosphere", "observations", "time series"],
    },
    {
        "term": "Greenhouse Gas (GHG)",
        "definition": (
            "Certain types of gases in the atmosphere, such as carbon dioxide, ozone, methane, "
            "water vapor, and ammonia, can induce global warming. Due to the unique molecular "
            "structure of these gases, they can absorb and emit long-wave radiation with high "
            "efficiency. They absorb long-wave radiation from the surface and emit it back to "
            "the surface. As a result, heat is trapped within the atmosphere, and the temperature goes up."
        ),
        "tags": ["radiation", "warming", "CO2", "methane"],
    },
    {
        "term": "Paris Agreement",
        "definition": (
            "An international climate agreement adopted in December 2015 at COP21 in Paris. "
            "Its main goal is to limit global temperature rise to well below 2°C above pre-industrial "
            "levels, and to pursue efforts to limit warming to 1.5°C."
        ),
        "tags": ["COP21", "policy", "UNFCCC", "targets"],
    },
    {
        "term": "Feedback",
        "definition": (
            "A process that can either amplify or reduce the effects of climate change, which can be "
            "sorted into two types: positive and negative feedback. Positive Feedback is a process "
            "that strengthens the original change. For example, when the global temperature rises, "
            "ice melts. Ice has a higher albedo, which means it reflects more sunlight. When ice "
            "disappears, darker ocean water absorbs more solar radiation, causing further warming. "
            "Negative Feedback is a process that weakens the original change. For example, increased "
            "plant growth due to higher CO₂ may absorb more carbon dioxide from the atmosphere, slightly reducing warming."
        ),
        "tags": ["positive feedback", "negative feedback", "ice-albedo"],
    },
    {
        "term": "Albedo",
        "definition": (
            "The ability of a certain type of surface to reflect radiation. For example, if 100W of "
            "solar radiation hits a surface and 35W is reflected (65W is absorbed), we say that the "
            "albedo of this surface is 35/100, or 35%, or 0.35."
        ),
        "tags": ["reflection", "radiation", "surface"],
    },
    {
        "term": "Hadley Cell",
        "definition": (
            "An atmospheric circulation cell that expands from the equator to 30 °N and 30 °S. "
            "Warm air rises from the equator and flows to 30°, where it condenses and flows back to "
            "the equator. Therefore, the Hadley Cell forms."
        ),
        "tags": ["circulation", "tropics", "subtropics"],
    },
    {
        "term": "Ferrel Cell",
        "definition": (
            "An atmospheric circulation cell that expands from 30 °N/S to 60 °N/S. As the air "
            "condenses at 30 ° (please refer to the Hadley Cell), it forms a high-pressure zone at "
            "this latitude, which is called the “subtropical high”. In the meantime, there is a "
            "“subpolar low” at 60 ° (please search for more definitions). Therefore, a circulation "
            "forms: air condenses at 30 °, moves to 60 °, then rises again, and flows back to 30 °."
        ),
        "tags": ["circulation", "mid-latitudes", "subtropical high", "subpolar low"],
    },
    {
        "term": "Polar Cell",
        "definition": (
            "The cold air at the two poles condenses and forms a high-pressure region. As there is "
            "a subpolar low at 60 °, the Polar Cell forms: air rises at 60 °, moves to the pole, "
            "condenses, and flows back to 60 °."
        ),
        "tags": ["circulation", "polar", "subpolar low"],
    },
    {
        "term": "Pressure Gradient Force",
        "definition": (
            "Force of the wind. When there is a difference in pressure at two locations, a force "
            "that points from the high-pressure to the low-pressure location forms. The larger the "
            "difference between the two pressures, and the closer the two locations, the stronger "
            "the force will be. This gradient force, together with the Coriolis Force and friction, "
            "forms the wind we see today."
        ),
        "tags": ["wind", "pressure", "coriolis", "friction"],
    },
    {
        "term": "El Niño",
        "definition": (
            "A climate phenomenon that occurs in the tropical Pacific Ocean. The trade winds weaken "
            "or even reverse direction, and sea surface temperatures in the central and eastern "
            "Pacific Ocean become warmer than normal. As a result, heavy rainfall may occur in "
            "western South America, the Western Pacific may experience drought, and marine ecosystems "
            "(particularly near Peru) can be disrupted. It usually develops every 2–7 years and can last about 9–12 months."
        ),
        "tags": ["ENSO", "Pacific", "trade winds", "SST"],
    },
    {
        "term": "La Niña",
        "definition": (
            "The reverse form of El Niño. The trade winds become stronger than usual, and sea surface "
            "temperatures in the central and eastern Pacific Ocean become cooler than normal. As a "
            "result, heavy rainfall occurs around the Western Pacific while drought occurs around the East."
        ),
        "tags": ["ENSO", "Pacific", "trade winds", "SST"],
    },
    {
        "term": "Troposhphere",
        "definition": (
            "The lowest layer of the atmosphere, extending from the sea level to about 10 km. In the "
            "troposphere, warm air is at the lower level, and cooler air is at the upper level. Thus, "
            "air convection forms and various weather exists, including rainfall, storms, and wind. "
            "Typically, the air cools at a rate of 6.5 °C/km. The troposphere at a higher latitude is thinner than at a lower latitude."
        ),
        "tags": ["atmosphere", "weather", "lapse rate"],
    },
    {
        "term": "Wavelength",
        "definition": (
            "The distance between two identical points of a wave, such as two consecutive crests or troughs. "
            "It is usually represented by the Greek letter λ (lambda) and measured in meters. "
            "Radio waves have long wavelengths, visible light has medium wavelengths, and X-rays have very short wavelengths."
    ),
        "tags": ["waves", "radiation", "physics"],
},

{
        "term": "Frequency",
        "definition": (
            "The number of wave cycles that pass a given point in one second. "
            "It is usually represented by f and measured in Hertz (Hz). "
            "Higher frequency means waves oscillate more rapidly. "
            "For example, blue light has a higher frequency than red light. "
            "For electromagnetic waves, a higher frequency means a shorter wavelength."
    ),
    "tags": ["waves", "radiation", "physics"],
},

{
        "term": "Chaos",
        "definition": (
            "A property of some dynamic systems in which very small changes in initial conditions can lead "
            "to large differences in outcomes. Although chaotic systems follow deterministic physical laws, "
            "their behavior becomes extremely difficult to predict over long periods of time. "
            "The atmosphere is considered a chaotic system, which is one reason why long-term weather "
            "forecasting is challenging."
    ),
        "tags": ["climate dynamics", "chaos theory", "weather prediction"],
},

{
        "term": "Butterfly Effect",
        "definition": (
            "A concept from chaos theory describing how a small change in a system can lead to large and "
            "unpredictable consequences. The term was introduced by meteorologist Edward Lorenz while "
            "studying atmospheric models. He suggested that a butterfly flapping its wings in Brazil "
            "could eventually cause a tornado in Texas."
    ),
        "tags": ["chaos theory", "climate dynamics", "weather prediction"],
},

{
        "term": "Stefan-Boltzmann Law",
        "definition": (
            "A physical law describing how much energy a body radiates depending on its temperature. "
            "It states that the total energy radiated per unit surface area is proportional to the fourth "
            "power of the temperature (measured in Kelvin). This law plays an important role in understanding "
            "Earth's radiation balance and the greenhouse effect."
    ),
        "tags": ["radiation", "energy balance", "climate physics"],
},

{
        "term": "Latent Heat",
        "definition": (
            "Heat related to the change of phase of a substance. For example, when ice melts into water, "
            "it absorbs latent heat. When water vapor condenses into liquid water, it releases latent heat. "
            "Latent heat is associated with phase change rather than temperature change."
    ),
        "tags": ["thermodynamics", "phase change", "energy cycle"],
},

{
        "term": "Typhoon",
        "definition": (
            "A powerful tropical cyclone that forms in the northwestern Pacific Ocean. "
            "Typhoons develop over warm ocean water and are characterized by strong rotating winds, "
            "heavy rainfall, a calm central eye, and low atmospheric pressure. "
            "Hurricanes have the same mechanism as typhoons but usually occur in the Atlantic Ocean "
            "and eastern Pacific."
    ),
        "tags": ["weather", "tropical cyclone", "storms"],
},

{
        "term": "Monsoon",
        "definition": (
            "A seasonal wind system that changes direction between summer and winter due to differences "
            "in heating between land and ocean. The most famous example is the South Asian monsoon. "
            "In summer, land heats faster than the ocean, creating low pressure over land, so moist air "
            "flows from the ocean and brings heavy rainfall. In winter, the pattern reverses and dry "
            "winds blow from land to the ocean."
    ),
        "tags": ["atmospheric circulation", "climate system", "precipitation"],
},
    {
    "term": "Stratosphere",
    "definition": (
        "The second-lowest layer of the atmosphere, extending from about 10 km to about 50 km in altitude. "
        "In this layer, air flows mostly horizontally, making it ideal for airplanes to fly. "
        "The upper part of the stratosphere contains the ozone layer, which absorbs harmful ultraviolet radiation "
        "from the Sun and protects life on Earth. Unlike the troposphere, temperature increases with altitude in "
        "the stratosphere."
    ),
    "tags": ["atmosphere", "ozone layer", "radiation"],
},

{
    "term": "Mesosphere",
    "definition": (
        "The third layer of the atmosphere, located above the stratosphere and below the thermosphere. "
        "In this layer, temperature decreases as altitude increases. "
        "The mesosphere is also where most meteors burn up when entering the Earth's atmosphere."
    ),
    "tags": ["atmosphere", "temperature structure", "meteors"],
},

{
    "term": "Thermosphere",
    "definition": (
        "The upper layer of the atmosphere above the mesosphere. "
        "In this layer, temperature increases rapidly with altitude because gases absorb high-energy solar radiation. "
        "The air is extremely thin, and many atoms become ionized, forming part of the ionosphere. "
        "Auroras and many satellites orbit in this region."
    ),
    "tags": ["atmosphere", "ionosphere", "space environment"],
},

{
    "term": "Solar Radiation",
    "definition": (
        "Electromagnetic radiation emitted by the Sun. Because of the Sun's extremely high surface temperature, "
        "solar radiation contains relatively short wavelengths and high frequencies. "
        "Solar radiation is the primary external energy source for the Earth and drives the climate system. "
        "On average, the solar energy reaching the top of Earth's atmosphere is about 1368 W/m², known as the solar constant."
    ),
    "tags": ["radiation", "energy balance", "sun"],
},

{
    "term": "Outgoing Longwave Radiation (OLR)",
    "definition": (
        "According to the Stefan–Boltzmann law, every object emits radiation depending on its temperature. "
        "The Earth's surface emits longwave (infrared) radiation toward the atmosphere and space. "
        "This emission is known as outgoing longwave radiation (OLR) and plays a key role in balancing incoming solar radiation. "
        "The warmer the Earth's surface becomes, the more OLR it emits."
    ),
    "tags": ["radiation", "energy balance", "climate system"],
},

{
    "term": "Ultraviolet Radiation (UV)",
    "definition": (
        "Electromagnetic radiation with higher frequency and shorter wavelength than visible light. "
        "Exposure to ultraviolet radiation may cause sunburn, skin damage, and eye problems. "
        "Much of the harmful UV radiation from the Sun is absorbed by the ozone layer in the stratosphere."
    ),
    "tags": ["radiation", "sun", "health"],
},

{
    "term": "Infrared Radiation (IR)",
    "definition": (
        "Electromagnetic radiation with lower frequency and longer wavelength than visible light. "
        "Infrared radiation is commonly associated with heat energy and is emitted by warm objects, "
        "including the Earth's surface. It is widely used in thermal imaging and infrared thermometers."
    ),
    "tags": ["radiation", "heat", "energy"],
},
    {
    "term": "Intertropical Convergence Zone (ITCZ)",
    "definition": (
        "A low-pressure zone near the equator where trade winds from the Northern and Southern Hemispheres converge. "
        "In this region, warm and moist air rises, leading to frequent cloud formation and heavy rainfall. "
        "The position of the ITCZ shifts north and south seasonally following the Sun, influencing tropical climates and monsoons."
    ),
    "tags": ["atmospheric circulation", "pressure system", "tropics"],
},

{
    "term": "Subtropical High",
    "definition": (
        "A high-pressure belt located around 30° latitude in both hemispheres. "
        "Air from the equator descends in this region, leading to dry and stable conditions. "
        "Subtropical highs are associated with desert regions such as the Sahara and play an important role in global circulation patterns."
    ),
    "tags": ["atmospheric circulation", "pressure system", "desert"],
},

{
    "term": "Subpolar Low",
    "definition": (
        "A low-pressure belt located around 60° latitude in both hemispheres. "
        "It forms where cold polar air meets warmer mid-latitude air, causing air to rise. "
        "This region is associated with frequent storms and strong weather systems, especially in the North Atlantic and North Pacific."
    ),
    "tags": ["atmospheric circulation", "pressure system", "storms"],
},

{
    "term": "North Atlantic Deep Water (NADW)",
    "definition": (
        "A mass of cold, dense water formed in the North Atlantic Ocean, particularly near Greenland and Iceland. "
        "It forms when surface water cools, becomes denser, and sinks to deep ocean layers. "
        "NADW is a key component of global ocean circulation and helps transport heat and carbon around the planet."
    ),
    "tags": ["ocean circulation", "thermohaline circulation", "climate system"],
},

{
    "term": "Atlantic Meridional Overturning Circulation (AMOC)",
    "definition": (
        "A large system of ocean currents in the Atlantic Ocean that transports warm surface water northward "
        "and cold deep water southward. It includes the formation of North Atlantic Deep Water. "
        "AMOC plays a crucial role in regulating climate, especially in Europe, by redistributing heat across the globe."
    ),
    "tags": ["ocean circulation", "global circulation", "climate system"],
},

{
    "term": "El Niño–Southern Oscillation (ENSO)",
    "definition": (
        "A climate pattern in the tropical Pacific Ocean involving changes in sea surface temperature, "
        "atmospheric pressure, and trade winds. ENSO has two main phases: El Niño (warming phase) and La Niña (cooling phase). "
        "It is one of the most important sources of year-to-year climate variability and affects weather patterns worldwide."
    ),
    "tags": ["climate variability", "ocean-atmosphere interaction", "ENSO"],
},

{
    "term": "Lapse Rate",
    "definition": (
        "The rate at which air temperature decreases with increasing altitude in the atmosphere. "
        "The average environmental lapse rate in the troposphere is about 6.5 °C per kilometer. "
        "Lapse rate is important for understanding atmospheric stability, cloud formation, and weather processes."
    ),
    "tags": ["atmosphere", "temperature", "weather"],
}
]

# ----------------------------
# Helpers
# ----------------------------
def normalize(s: str) -> str:
    return (s or "").strip().lower()

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()

def term_matches(query: str, item: dict) -> bool:
    if not query:
        return True
    q = normalize(query)

    hay = " ".join([
        item["term"],
        item.get("definition", ""),
        " ".join(item.get("tags", [])),
    ])
    hay_n = normalize(hay)

    # 1) substring partial match (fast fuzzy)
    if q in hay_n:
        return True

    # 2) approximate match against term
    if similarity(q, item["term"]) >= 0.55:
        return True

    # 3) approximate match against tags
    for t in item.get("tags", []):
        if similarity(q, t) >= 0.65:
            return True

    return False

def highlight(text: str, query: str) -> str:
    """Return HTML with query highlighted (case-insensitive)."""
    if not query:
        return text
    q = query.strip()
    if not q:
        return text
    pattern = re.compile(re.escape(q), re.IGNORECASE)
    return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)

# ----------------------------
# UI
# ----------------------------
st.title("Climate Dictionary🔍")
st.caption("Click a term to expand its definition. Use the search bar for fuzzy search.")

# NOTE: removed vertical_alignment for compatibility with older Streamlit
col1, col2 = st.columns([2, 1])

with col1:
    query = st.text_input(
        "Search terms (supports partial & fuzzy match)",
        placeholder="e.g., 'keeling', 'greenhouse', 'ENSO', 'albe'...",
    )

with col2:
    sort_mode = st.selectbox("Sort", ["Most relevant", "A → Z"], index=0)

filtered = [t for t in TERMS if term_matches(query, t)]

if sort_mode == "A → Z":
    filtered = sorted(filtered, key=lambda x: x["term"].lower())
else:
    if query:
        filtered = sorted(
            filtered,
            key=lambda x: max(
                similarity(query, x["term"]),
                similarity(query, " ".join(x.get("tags", []))),
            ),
            reverse=True,
        )
    else:
        filtered = sorted(filtered, key=lambda x: x["term"].lower())

st.divider()
st.write(f"Showing **{len(filtered)}** / {len(TERMS)} terms")

# "Click to locate" index (not true anchor jump, but easy to find)
if filtered:
    with st.expander("Quick Locate", expanded=False):
        picked = st.selectbox(
            "Choose a term to locate below",
            [x["term"] for x in filtered],
            index=0,
        )
        st.caption("Scroll down; the chosen term will be expanded automatically.")

st.divider()

# auto-open picked term if any
picked_term = None
try:
    picked_term = picked  # exists only if expander ran
except NameError:
    picked_term = None

for item in filtered:
    open_by_default = (picked_term is not None and item["term"] == picked_term)

    title_html = highlight(item["term"], query)
    tags = item.get("tags", [])
    tag_str = " · ".join(tags) if tags else ""

    with st.expander(label=item["term"], expanded=open_by_default):
        if tag_str:
            st.caption(tag_str)

        # highlight matches in definition as well
        def_html = highlight(item.get("definition", "").strip(), query)
        st.markdown(def_html, unsafe_allow_html=True)

if not filtered:
    st.warning("No matches found. Try a shorter keyword or a different spelling.")