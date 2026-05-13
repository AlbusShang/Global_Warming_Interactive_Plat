import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Climate Lab",
    page_icon="🔬",
    layout="wide"
)

# -----------------------------
# Shared Constants
# -----------------------------
SIGMA = 5.67e-8  # Stefan-Boltzmann constant
BASELINE_TEMP_C = 15.0


# -----------------------------
# Shared Utility Functions
# -----------------------------
def clip(value, lower, upper):
    return max(lower, min(value, upper))


# -----------------------------
# Ice-Albedo Model Functions
# -----------------------------
def calculate_albedo(ice_fraction, ice_albedo, non_ice_albedo):
    return ice_fraction * ice_albedo + (1 - ice_fraction) * non_ice_albedo


def calculate_absorbed_solar_radiation(S, albedo):
    return (S / 4) * (1 - albedo)


def calculate_equilibrium_temperature(absorbed_radiation, emissivity):
    temperature_k = (absorbed_radiation / (emissivity * SIGMA)) ** 0.25
    return temperature_k - 273.15


def run_ice_albedo_simulation(
    years,
    initial_f,
    ice_albedo,
    non_ice_albedo,
    response_speed,
    melt_sensitivity,
    warming_rate,
    S,
    emissivity
):
    records = []

    f = initial_f
    albedo = calculate_albedo(f, ice_albedo, non_ice_albedo)
    absorbed = calculate_absorbed_solar_radiation(S, albedo)
    temp_c = BASELINE_TEMP_C
    initial_albedo = albedo
    initial_absorbed = absorbed

    for year in range(years + 1):
        albedo = calculate_albedo(f, ice_albedo, non_ice_albedo)
        absorbed = calculate_absorbed_solar_radiation(S, albedo)
        equilibrium_temp = calculate_equilibrium_temperature(absorbed, emissivity)
        reflected = (S / 4) * albedo
        temp_anomaly = temp_c - BASELINE_TEMP_C

        records.append({
            "Year": year,
            "Ice/Snow Cover Fraction": f,
            "Planetary Albedo": albedo,
            "Absorbed Solar Radiation (W/m²)": absorbed,
            "Reflected Solar Radiation (W/m²)": reflected,
            "Estimated Global Temperature (°C)": temp_c,
            "Temperature Anomaly (°C)": temp_anomaly,
            "Equilibrium Temperature (°C)": equilibrium_temp,
            "Extra Absorbed Energy (W/m²)": absorbed - initial_absorbed,
            "Albedo Change": albedo - initial_albedo,
        })

        temp_c = temp_c + response_speed * (equilibrium_temp - temp_c) + warming_rate
        warming_above_baseline = max(0, temp_c - BASELINE_TEMP_C)
        f = f - melt_sensitivity * warming_above_baseline
        f = clip(f, 0.0, 1.0)

    return pd.DataFrame(records)


# -----------------------------
# Sea Level Rise Model Functions
# -----------------------------
def run_sea_level_rise_simulation(
    years,
    initial_sea_level,
    warming_rate,
    thermal_expansion_rate,
    glacier_melt_rate,
    ice_sheet_melt_rate,
    local_subsidence_rate,
    storm_surge_height
):
    records = []

    sea_level = initial_sea_level
    temperature_anomaly = 0.0

    for year in range(years + 1):
        # Temperature anomaly increases gradually according to the chosen warming rate.
        temperature_anomaly = warming_rate * year

        # Sea level components, in meters.
        thermal_expansion = thermal_expansion_rate * temperature_anomaly * year / 1000
        glacier_melt = glacier_melt_rate * temperature_anomaly * year / 1000
        ice_sheet_melt = ice_sheet_melt_rate * (temperature_anomaly ** 1.3) * year / 1000
        local_subsidence = local_subsidence_rate * year / 1000

        sea_level = initial_sea_level + thermal_expansion + glacier_melt + ice_sheet_melt + local_subsidence
        extreme_water_level = sea_level + storm_surge_height

        records.append({
            "Year": year,
            "Temperature Anomaly (°C)": temperature_anomaly,
            "Thermal Expansion (m)": thermal_expansion,
            "Glacier Melt Contribution (m)": glacier_melt,
            "Ice Sheet Contribution (m)": ice_sheet_melt,
            "Local Subsidence Contribution (m)": local_subsidence,
            "Relative Sea Level Rise (m)": sea_level,
            "Extreme Water Level with Storm Surge (m)": extreme_water_level,
        })

    return pd.DataFrame(records)


# -----------------------------
# Urban Heat Island Model Functions
# -----------------------------
def run_urban_heat_island_simulation(
    hours,
    base_air_temp,
    building_density,
    vegetation_fraction,
    surface_albedo,
    anthropogenic_heat,
    wind_speed,
    cooling_efficiency
):
    records = []

    for hour in range(hours + 1):
        time_of_day = hour % 24

        # Simple daily temperature cycle: warmest around 15:00, coolest around 05:00.
        daily_cycle = 5 * np.sin((2 * np.pi / 24) * (time_of_day - 9))
        rural_temp = base_air_temp + daily_cycle

        # UHI intensity is increased by dense buildings, dark surfaces, and human heat emissions.
        # It is reduced by vegetation, wind, and cooling design.
        density_effect = 5.0 * building_density
        vegetation_effect = -4.0 * vegetation_fraction
        albedo_effect = 4.0 * (0.35 - surface_albedo)
        heat_effect = 0.08 * anthropogenic_heat
        wind_effect = -0.7 * wind_speed
        cooling_effect = -3.0 * cooling_efficiency

        raw_uhi = density_effect + vegetation_effect + albedo_effect + heat_effect + wind_effect + cooling_effect

        # Urban heat island is usually strongest at night.
        night_factor = 1.0 + 0.35 * np.cos((2 * np.pi / 24) * (time_of_day - 3))
        uhi_intensity = max(0, raw_uhi * night_factor)

        urban_temp = rural_temp + uhi_intensity

        records.append({
            "Hour": hour,
            "Time of Day": time_of_day,
            "Rural Temperature (°C)": rural_temp,
            "Urban Temperature (°C)": urban_temp,
            "UHI Intensity (°C)": uhi_intensity,
            "Building Density Effect (°C)": density_effect,
            "Vegetation Effect (°C)": vegetation_effect,
            "Albedo Effect (°C)": albedo_effect,
            "Anthropogenic Heat Effect (°C)": heat_effect,
            "Wind Effect (°C)": wind_effect,
            "Cooling Design Effect (°C)": cooling_effect,
        })

    return pd.DataFrame(records)


# -----------------------------
# Climate Lab Page
# -----------------------------
def show_climate_lab():
    st.title("🔬 Climate Lab")
    st.caption("Choose an experiment, adjust the parameters, and observe how the climate system responds.")

    st.markdown(
        """
        Welcome to the **Climate Lab**. This page is designed for interactive climate experiments.
        Instead of only reading explanations, students can change variables, run simulations, compare outcomes,
        and explain the mechanisms behind climate change.
        """
    )

    experiment = st.selectbox(
        "Choose an experiment",
        [
            "Ice-Albedo Feedback",
            "Sea Level Rise",
            "Urban Heat Island",
        ],
        index=0
    )

    st.divider()

    if experiment == "Ice-Albedo Feedback":
        show_ice_albedo_lab()
    elif experiment == "Sea Level Rise":
        show_sea_level_rise_lab()
    elif experiment == "Urban Heat Island":
        show_urban_heat_island_lab()


# -----------------------------
# Coming Soon Placeholder
# -----------------------------
def show_coming_soon_lab(title, description):
    st.title(title)
    st.info(description)
    st.markdown("This experiment is coming soon. The Climate Lab structure is ready for adding more experiments.")


# -----------------------------
# Ice-Albedo Lab Page
# -----------------------------
def show_ice_albedo_lab():
    st.header("❄️ Ice-Albedo Feedback Lab")
    st.caption("Explore how shrinking ice and snow cover can reduce Earth's reflectivity and amplify warming.")

    st.markdown(
        """
        The **ice-albedo feedback** is one of the most important positive feedback mechanisms in the climate system.
        Ice and snow reflect a large fraction of incoming sunlight. When they melt, darker ocean or land surfaces are exposed,
        absorbing more solar energy and causing additional warming.
        """
    )

    st.subheader("Experiment Parameters")

    with st.expander("Adjust model parameters", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            simulation_years = st.slider(
                "Simulation Length (years)",
                min_value=20,
                max_value=200,
                value=100,
                step=10
            )

            initial_ice_fraction = st.slider(
                "Initial Ice/Snow Cover Fraction",
                min_value=0.05,
                max_value=1.00,
                value=0.70,
                step=0.05,
                help="A simplified fraction from 0 to 1. Higher values mean more ice and snow cover."
            )

            alpha_ice = st.slider(
                "Ice/Snow Albedo",
                min_value=0.50,
                max_value=0.90,
                value=0.75,
                step=0.01,
                help="Fresh snow can have very high albedo. Older ice or dirty snow reflects less sunlight."
            )

        with col2:
            alpha_non_ice = st.slider(
                "Non-Ice Surface Albedo",
                min_value=0.05,
                max_value=0.40,
                value=0.25,
                step=0.01,
                help="Ocean, forests, bare soil, and urban surfaces usually reflect less sunlight than ice and snow."
            )

            climate_response = st.slider(
                "Climate Response Speed",
                min_value=0.01,
                max_value=0.20,
                value=0.05,
                step=0.01,
                help="Controls how quickly temperature moves toward the new equilibrium each year."
            )

            ice_sensitivity = st.slider(
                "Ice Melt Sensitivity",
                min_value=0.000,
                max_value=0.020,
                value=0.005,
                step=0.001,
                help="Controls how strongly warming reduces ice/snow cover."
            )

        with col3:
            external_warming_rate = st.slider(
                "External Warming Rate (°C/year)",
                min_value=0.000,
                max_value=0.050,
                value=0.010,
                step=0.001,
                help="Represents additional warming from greenhouse gases and other external forcing."
            )

            solar_constant = st.number_input(
                "Solar Constant S (W/m²)",
                min_value=1300.0,
                max_value=1420.0,
                value=1361.0,
                step=1.0
            )

            effective_emissivity = st.slider(
                "Effective Emissivity",
                min_value=0.45,
                max_value=0.85,
                value=0.61,
                step=0.01,
                help="A simplified parameter used to approximate the greenhouse effect in the energy balance model."
            )

    df = run_ice_albedo_simulation(
        years=simulation_years,
        initial_f=initial_ice_fraction,
        ice_albedo=alpha_ice,
        non_ice_albedo=alpha_non_ice,
        response_speed=climate_response,
        melt_sensitivity=ice_sensitivity,
        warming_rate=external_warming_rate,
        S=solar_constant,
        emissivity=effective_emissivity
    )

    initial = df.iloc[0]
    final = df.iloc[-1]

    st.subheader("Final Simulation Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Temperature Change",
            f"{final['Temperature Anomaly (°C)']:+.2f} °C",
            delta=f"over {simulation_years} years"
        )

    with col2:
        ice_change_pct = (final["Ice/Snow Cover Fraction"] - initial["Ice/Snow Cover Fraction"]) * 100
        st.metric(
            "Ice/Snow Cover Change",
            f"{ice_change_pct:+.1f}%",
            delta=f"final fraction: {final['Ice/Snow Cover Fraction']:.2f}"
        )

    with col3:
        st.metric(
            "Albedo Change",
            f"{final['Albedo Change']:+.3f}",
            delta=f"final albedo: {final['Planetary Albedo']:.3f}"
        )

    with col4:
        st.metric(
            "Extra Absorbed Energy",
            f"{final['Extra Absorbed Energy (W/m²)']:+.2f} W/m²",
            delta="relative to year 0"
        )

    if final["Temperature Anomaly (°C)"] < 1.5:
        risk_label = "Stable"
        risk_text = "The feedback remains relatively limited in this simplified simulation."
    elif final["Temperature Anomaly (°C)"] < 3.0:
        risk_label = "Accelerating"
        risk_text = "The feedback is becoming stronger as ice and snow cover continue to decline."
    else:
        risk_label = "Critical"
        risk_text = "The simulation shows strong warming amplification and rapid ice/snow loss."

    st.info(f"**Feedback Status: {risk_label}** — {risk_text}")

    st.subheader("Time Series")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Temperature",
        "Ice/Snow Cover",
        "Albedo",
        "Energy Balance"
    ])

    with tab1:
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.plot(df["Year"], df["Estimated Global Temperature (°C)"], linewidth=2)
        ax.set_xlabel("Year")
        ax.set_ylabel("Estimated Global Temperature (°C)")
        ax.set_title("Estimated Global Temperature Over Time")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with tab2:
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.plot(df["Year"], df["Ice/Snow Cover Fraction"], linewidth=2)
        ax.set_xlabel("Year")
        ax.set_ylabel("Ice/Snow Cover Fraction")
        ax.set_title("Ice/Snow Cover Over Time")
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with tab3:
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.plot(df["Year"], df["Planetary Albedo"], linewidth=2)
        ax.set_xlabel("Year")
        ax.set_ylabel("Planetary Albedo")
        ax.set_title("Planetary Albedo Over Time")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with tab4:
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.plot(df["Year"], df["Absorbed Solar Radiation (W/m²)"], linewidth=2, label="Absorbed")
        ax.plot(df["Year"], df["Reflected Solar Radiation (W/m²)"], linewidth=2, label="Reflected")
        ax.set_xlabel("Year")
        ax.set_ylabel("Solar Radiation (W/m²)")
        ax.set_title("Absorbed and Reflected Solar Radiation")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    st.subheader("Simplified Polar Ice Visualization")

    selected_year = st.slider(
        "Choose a year to visualize",
        min_value=0,
        max_value=simulation_years,
        value=simulation_years,
        step=1
    )

    selected = df[df["Year"] == selected_year].iloc[0]
    selected_f = selected["Ice/Snow Cover Fraction"]

    left, right = st.columns([1.1, 1])

    with left:
        theta = np.linspace(0, 2 * np.pi, 500)
        outer_r = 1.0
        ice_r = np.sqrt(selected_f)

        fig, ax = plt.subplots(figsize=(5.8, 5.8))
        ax.fill(outer_r * np.cos(theta), outer_r * np.sin(theta), alpha=0.35)
        ax.fill(ice_r * np.cos(theta), ice_r * np.sin(theta), alpha=0.85)
        ax.set_aspect("equal")
        ax.set_xlim(-1.05, 1.05)
        ax.set_ylim(-1.05, 1.05)
        ax.axis("off")
        ax.set_title(f"Simplified Ice/Snow Extent — Year {selected_year}")
        st.pyplot(fig)

    with right:
        st.markdown(
            f"""
            **Year {selected_year} Snapshot**

            - Ice/Snow Cover Fraction: **{selected_f:.2f}**
            - Planetary Albedo: **{selected['Planetary Albedo']:.3f}**
            - Estimated Global Temperature: **{selected['Estimated Global Temperature (°C)']:.2f} °C**
            - Temperature Anomaly: **{selected['Temperature Anomaly (°C)']:+.2f} °C**
            - Absorbed Solar Radiation: **{selected['Absorbed Solar Radiation (W/m²)']:.2f} W/m²**
            - Reflected Solar Radiation: **{selected['Reflected Solar Radiation (W/m²)']:.2f} W/m²**
            """
        )

    with st.expander("View Simulation Data"):
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Simulation Data as CSV",
            data=csv,
            file_name="ice_albedo_feedback_simulation.csv",
            mime="text/csv"
        )

    st.subheader("How the Model Works")

    st.markdown(
        """
        This is a **simplified educational model**, not a full climate model. It is designed to help students understand
        the mechanism of ice-albedo feedback.

        **1. Planetary albedo** is calculated from the fraction of ice/snow cover:

        `albedo = ice_fraction × ice_albedo + (1 - ice_fraction) × non_ice_albedo`

        **2. Absorbed solar radiation** increases when albedo decreases:

        `absorbed_solar_radiation = solar_constant / 4 × (1 - albedo)`

        **3. Equilibrium temperature** is estimated using a simplified Stefan-Boltzmann energy balance:

        `temperature = [absorbed_solar_radiation / (emissivity × sigma)] ^ 0.25`

        **4. Temperature changes gradually** rather than instantly reaching equilibrium:

        `temperature_next = temperature_now + response_speed × (equilibrium_temperature - temperature_now) + external_warming_rate`

        **5. Ice/snow cover decreases when temperature rises above the baseline:**

        `ice_fraction_next = ice_fraction_now - ice_melt_sensitivity × max(0, temperature_now - baseline_temperature)`

        The key idea is simple: **less ice means lower albedo, lower albedo means more absorbed energy, and more absorbed energy means more warming.**
        """
    )

    st.warning(
        "Model limitation: This lab intentionally simplifies the climate system. It does not include clouds, ocean circulation, regional climate differences, seasonal cycles, aerosols, or detailed greenhouse gas chemistry."
    )


# -----------------------------
# Sea Level Rise Lab Page
# -----------------------------
def show_sea_level_rise_lab():
    st.header("🌊 Sea Level Rise Lab")
    st.caption("Explore how warming, land subsidence, and storm surge can increase coastal flood risk.")

    st.markdown(
        """
        **Sea level rise** is caused by several processes, including thermal expansion of seawater,
        melting mountain glaciers, melting ice sheets, and local land subsidence.
        In this lab, students can adjust these factors and observe how coastal flood risk changes over time.
        """
    )

    st.subheader("Experiment Parameters")

    with st.expander("Adjust model parameters", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            simulation_years = st.slider(
                "Simulation Length (years)",
                min_value=20,
                max_value=150,
                value=100,
                step=10,
                key="slr_years"
            )

            warming_rate = st.slider(
                "Warming Rate (°C/year)",
                min_value=0.000,
                max_value=0.050,
                value=0.020,
                step=0.001,
                key="slr_warming_rate",
                help="A simplified rate of global temperature increase. 0.020 °C/year means about +2.0 °C in 100 years."
            )

            initial_sea_level = st.slider(
                "Initial Relative Sea Level Rise (m)",
                min_value=0.0,
                max_value=0.5,
                value=0.0,
                step=0.01,
                key="slr_initial"
            )

        with col2:
            thermal_expansion_rate = st.slider(
                "Thermal Expansion Sensitivity (mm/year/°C)",
                min_value=0.0,
                max_value=4.0,
                value=1.4,
                step=0.1,
                key="slr_thermal",
                help="Warmer ocean water expands, raising sea level."
            )

            glacier_melt_rate = st.slider(
                "Glacier Melt Sensitivity (mm/year/°C)",
                min_value=0.0,
                max_value=5.0,
                value=1.8,
                step=0.1,
                key="slr_glacier",
                help="Mountain glaciers lose mass as temperature rises."
            )

            ice_sheet_melt_rate = st.slider(
                "Ice Sheet Melt Sensitivity (mm/year/°C^1.3)",
                min_value=0.0,
                max_value=4.0,
                value=1.0,
                step=0.1,
                key="slr_ice_sheet",
                help="A simplified nonlinear term for Greenland and Antarctic ice sheet contribution."
            )

        with col3:
            local_subsidence_rate = st.slider(
                "Local Land Subsidence (mm/year)",
                min_value=0.0,
                max_value=20.0,
                value=3.0,
                step=0.5,
                key="slr_subsidence",
                help="Some coastal cities sink because of groundwater extraction, sediment compaction, or tectonic factors."
            )

            storm_surge_height = st.slider(
                "Storm Surge Height (m)",
                min_value=0.0,
                max_value=5.0,
                value=1.5,
                step=0.1,
                key="slr_surge",
                help="Temporary sea level rise during storms, typhoons, hurricanes, or cyclones."
            )

            protection_height = st.slider(
                "Coastal Protection Height (m)",
                min_value=0.0,
                max_value=6.0,
                value=2.5,
                step=0.1,
                key="slr_protection",
                help="A simplified height of seawalls, dunes, levees, or other flood defenses."
            )

    df = run_sea_level_rise_simulation(
        years=simulation_years,
        initial_sea_level=initial_sea_level,
        warming_rate=warming_rate,
        thermal_expansion_rate=thermal_expansion_rate,
        glacier_melt_rate=glacier_melt_rate,
        ice_sheet_melt_rate=ice_sheet_melt_rate,
        local_subsidence_rate=local_subsidence_rate,
        storm_surge_height=storm_surge_height
    )

    final = df.iloc[-1]
    max_extreme_water = df["Extreme Water Level with Storm Surge (m)"].max()
    protection_gap = protection_height - max_extreme_water

    st.subheader("Final Simulation Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Final Sea Level Rise",
            f"{final['Relative Sea Level Rise (m)']:.2f} m",
            delta=f"after {simulation_years} years"
        )

    with col2:
        st.metric(
            "Extreme Water Level",
            f"{final['Extreme Water Level with Storm Surge (m)']:.2f} m",
            delta="sea level + storm surge"
        )

    with col3:
        st.metric(
            "Final Warming",
            f"+{final['Temperature Anomaly (°C)']:.2f} °C"
        )

    with col4:
        st.metric(
            "Protection Gap",
            f"{protection_gap:+.2f} m",
            delta="positive means safer margin"
        )

    if protection_gap > 1.0:
        risk_status = "Low"
        risk_text = "Coastal protection remains well above the simulated extreme water level."
    elif protection_gap > 0:
        risk_status = "Moderate"
        risk_text = "The safety margin is small. Stronger storms or faster sea level rise could create flood risk."
    else:
        risk_status = "High"
        risk_text = "The simulated extreme water level exceeds the protection height. Flooding becomes likely in this simplified model."

    st.info(f"**Coastal Flood Risk: {risk_status}** — {risk_text}")

    st.subheader("Time Series")

    tab1, tab2, tab3 = st.tabs([
        "Sea Level Rise",
        "Extreme Water Level",
        "Component Contributions"
    ])

    with tab1:
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.plot(df["Year"], df["Relative Sea Level Rise (m)"], linewidth=2)
        ax.set_xlabel("Year")
        ax.set_ylabel("Relative Sea Level Rise (m)")
        ax.set_title("Relative Sea Level Rise Over Time")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with tab2:
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.plot(df["Year"], df["Extreme Water Level with Storm Surge (m)"], linewidth=2, label="Extreme Water Level")
        ax.axhline(protection_height, linestyle="--", linewidth=2, label="Coastal Protection Height")
        ax.set_xlabel("Year")
        ax.set_ylabel("Water Level (m)")
        ax.set_title("Extreme Water Level vs Coastal Protection")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with tab3:
        final_contributions = pd.DataFrame({
            "Component": [
                "Thermal Expansion",
                "Glacier Melt",
                "Ice Sheet Melt",
                "Local Subsidence"
            ],
            "Contribution (m)": [
                final["Thermal Expansion (m)"],
                final["Glacier Melt Contribution (m)"],
                final["Ice Sheet Contribution (m)"],
                final["Local Subsidence Contribution (m)"],
            ]
        })

        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.bar(final_contributions["Component"], final_contributions["Contribution (m)"])
        ax.set_ylabel("Contribution to Relative Sea Level Rise (m)")
        ax.set_title("Final Sea Level Rise Contributions")
        ax.tick_params(axis="x", rotation=20)
        ax.grid(True, axis="y", alpha=0.3)
        st.pyplot(fig)

    st.subheader("Simplified Coastal Cross-Section")

    selected_year = st.slider(
        "Choose a year to visualize",
        min_value=0,
        max_value=simulation_years,
        value=simulation_years,
        step=1,
        key="slr_selected_year"
    )

    selected = df[df["Year"] == selected_year].iloc[0]
    water_level = selected["Relative Sea Level Rise (m)"]
    extreme_level = selected["Extreme Water Level with Storm Surge (m)"]

    left, right = st.columns([1.15, 1])

    with left:
        x = np.linspace(0, 10, 300)
        land = 0.25 * (x - 2.5)
        land = np.clip(land, -0.5, 3.5)

        fig, ax = plt.subplots(figsize=(7, 4.8))
        ax.fill_between(x, -1, land, alpha=0.45, label="Land")
        ax.fill_between(
            x,
            -1,
            water_level,
            where=np.full_like(x, water_level > -1, dtype=bool),
            alpha=0.35,
            label="Mean Sea Level"
        )
        ax.axhline(extreme_level, linewidth=2, label="Extreme Water Level")
        ax.axhline(protection_height, linestyle="--", linewidth=2, label="Protection Height")
        ax.set_ylim(-0.5, max(4.0, protection_height + 0.8, extreme_level + 0.8))
        ax.set_xlim(0, 10)
        ax.set_xlabel("Coast-to-Inland Transect")
        ax.set_ylabel("Elevation / Water Level (m)")
        ax.set_title(f"Simplified Coastal Flood Profile — Year {selected_year}")
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with right:
        flooded_fraction = np.mean(land < extreme_level)
        st.markdown(
            f"""
            **Year {selected_year} Snapshot**

            - Temperature Anomaly: **+{selected['Temperature Anomaly (°C)']:.2f} °C**
            - Relative Sea Level Rise: **{water_level:.2f} m**
            - Storm Surge Height: **{storm_surge_height:.2f} m**
            - Extreme Water Level: **{extreme_level:.2f} m**
            - Coastal Protection Height: **{protection_height:.2f} m**
            - Simplified Flooded Transect Fraction: **{flooded_fraction * 100:.1f}%**
            """
        )

    with st.expander("View Simulation Data"):
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Simulation Data as CSV",
            data=csv,
            file_name="sea_level_rise_simulation.csv",
            mime="text/csv"
        )

    st.subheader("How the Model Works")

    st.markdown(
        """
        This is a **simplified educational model**, not a full sea level projection model.
        It is designed to help students understand why coastal flood risk depends on both global and local factors.

        **1. Temperature anomaly** increases according to a simple warming rate:

        `temperature_anomaly = warming_rate × year`

        **2. Relative sea level rise** is estimated from four components:

        `sea_level_rise = thermal_expansion + glacier_melt + ice_sheet_melt + local_subsidence`

        **3. Extreme water level** adds storm surge on top of mean sea level rise:

        `extreme_water_level = sea_level_rise + storm_surge_height`

        **4. Flood risk** is estimated by comparing extreme water level with coastal protection height:

        `protection_gap = protection_height - extreme_water_level`

        The key idea is simple: **sea level rise is gradual, but flood disasters often happen when long-term sea level rise combines with short-term storm surge.**
        """
    )

    st.warning(
        "Model limitation: This lab intentionally simplifies sea level rise. It does not include tides, waves, local bathymetry, real elevation data, coastal erosion, groundwater flooding, or official IPCC projection pathways."
    )


# -----------------------------
# Urban Heat Island Lab Page
# -----------------------------
def show_urban_heat_island_lab():
    st.header("🏙️ Urban Heat Island Lab")
    st.caption("Explore how urban surfaces, vegetation, buildings, wind, and human heat emissions affect city temperature.")

    st.markdown(
        """
        The **urban heat island effect** occurs when cities become warmer than nearby rural areas.
        Dense buildings, dark surfaces, limited vegetation, traffic, air conditioning, and weak wind can all increase urban temperatures.
        In this lab, students can adjust city design variables and observe how the urban-rural temperature difference changes.
        """
    )

    st.subheader("Experiment Parameters")

    with st.expander("Adjust model parameters", expanded=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            simulation_hours = st.slider(
                "Simulation Length (hours)",
                min_value=24,
                max_value=168,
                value=72,
                step=24
            )

            base_air_temp = st.slider(
                "Baseline Rural Temperature (°C)",
                min_value=10.0,
                max_value=40.0,
                value=28.0,
                step=0.5,
                help="The average rural air temperature before the daily cycle is added."
            )

            building_density = st.slider(
                "Building Density",
                min_value=0.0,
                max_value=1.0,
                value=0.70,
                step=0.05,
                help="Higher values represent denser urban areas with more heat-trapping surfaces."
            )

        with col2:
            vegetation_fraction = st.slider(
                "Vegetation Fraction",
                min_value=0.0,
                max_value=1.0,
                value=0.20,
                step=0.05,
                help="Higher values represent more trees, parks, and green space."
            )

            surface_albedo = st.slider(
                "Average Surface Albedo",
                min_value=0.05,
                max_value=0.60,
                value=0.18,
                step=0.01,
                help="Higher albedo surfaces reflect more sunlight and usually reduce heating."
            )

            anthropogenic_heat = st.slider(
                "Anthropogenic Heat Release (W/m²)",
                min_value=0,
                max_value=80,
                value=30,
                step=5,
                help="Heat released by vehicles, buildings, air conditioning, and industry."
            )

        with col3:
            wind_speed = st.slider(
                "Wind Speed (m/s)",
                min_value=0.0,
                max_value=8.0,
                value=2.0,
                step=0.5,
                help="Wind helps mix air and reduce heat accumulation."
            )

            cooling_efficiency = st.slider(
                "Cooling Design Efficiency",
                min_value=0.0,
                max_value=1.0,
                value=0.15,
                step=0.05,
                help="Represents cool roofs, shade, water features, ventilation corridors, and climate-sensitive design."
            )

    df = run_urban_heat_island_simulation(
        hours=simulation_hours,
        base_air_temp=base_air_temp,
        building_density=building_density,
        vegetation_fraction=vegetation_fraction,
        surface_albedo=surface_albedo,
        anthropogenic_heat=anthropogenic_heat,
        wind_speed=wind_speed,
        cooling_efficiency=cooling_efficiency
    )

    final = df.iloc[-1]
    max_uhi = df["UHI Intensity (°C)"].max()
    avg_uhi = df["UHI Intensity (°C)"].mean()
    max_urban_temp = df["Urban Temperature (°C)"].max()
    max_rural_temp = df["Rural Temperature (°C)"].max()

    st.subheader("Final Simulation Results")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Average UHI Intensity", f"{avg_uhi:.2f} °C")

    with col2:
        st.metric("Maximum UHI Intensity", f"{max_uhi:.2f} °C")

    with col3:
        st.metric("Maximum Urban Temperature", f"{max_urban_temp:.2f} °C")

    with col4:
        st.metric("Urban-Rural Difference at Final Hour", f"{final['UHI Intensity (°C)']:.2f} °C")

    if max_uhi < 2:
        status = "Low"
        status_text = "The city remains relatively close to rural temperatures in this simplified simulation."
    elif max_uhi < 5:
        status = "Moderate"
        status_text = "Urban warming is noticeable. More vegetation, higher albedo, or better ventilation could reduce the effect."
    else:
        status = "Severe"
        status_text = "The simulation shows strong urban heat stress. Cooling strategies are urgently needed."

    st.info(f"**Heat Island Status: {status}** — {status_text}")

    st.subheader("Time Series")

    tab1, tab2, tab3 = st.tabs([
        "Urban vs Rural Temperature",
        "UHI Intensity",
        "Factor Contributions"
    ])

    with tab1:
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.plot(df["Hour"], df["Urban Temperature (°C)"], linewidth=2, label="Urban")
        ax.plot(df["Hour"], df["Rural Temperature (°C)"], linewidth=2, label="Rural")
        ax.set_xlabel("Hour")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title("Urban and Rural Temperature Over Time")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with tab2:
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.plot(df["Hour"], df["UHI Intensity (°C)"], linewidth=2)
        ax.set_xlabel("Hour")
        ax.set_ylabel("Urban Heat Island Intensity (°C)")
        ax.set_title("Urban Heat Island Intensity Over Time")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    with tab3:
        contributions = pd.DataFrame({
            "Factor": [
                "Building Density",
                "Vegetation",
                "Surface Albedo",
                "Anthropogenic Heat",
                "Wind",
                "Cooling Design"
            ],
            "Contribution (°C)": [
                df["Building Density Effect (°C)"].iloc[0],
                df["Vegetation Effect (°C)"].iloc[0],
                df["Albedo Effect (°C)"].iloc[0],
                df["Anthropogenic Heat Effect (°C)"].iloc[0],
                df["Wind Effect (°C)"].iloc[0],
                df["Cooling Design Effect (°C)"].iloc[0],
            ]
        })

        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.bar(contributions["Factor"], contributions["Contribution (°C)"])
        ax.axhline(0, linewidth=1)
        ax.set_ylabel("Contribution to UHI Intensity (°C)")
        ax.set_title("Simplified Contribution of Each Factor")
        ax.tick_params(axis="x", rotation=30)
        ax.grid(True, axis="y", alpha=0.3)
        st.pyplot(fig)

    st.subheader("Simplified City Heat Map")

    selected_hour = st.slider(
        "Choose an hour to visualize",
        min_value=0,
        max_value=simulation_hours,
        value=simulation_hours,
        step=1,
        key="uhi_selected_hour"
    )

    selected = df[df["Hour"] == selected_hour].iloc[0]
    selected_uhi = selected["UHI Intensity (°C)"]

    left, right = st.columns([1.1, 1])

    with left:
        grid_size = 80
        x = np.linspace(-1, 1, grid_size)
        y = np.linspace(-1, 1, grid_size)
        X, Y = np.meshgrid(x, y)
        distance = np.sqrt(X**2 + Y**2)

        # Hotter city center, cooler outskirts.
        heat_field = selected["Rural Temperature (°C)"] + selected_uhi * np.exp(-3 * distance**2)

        fig, ax = plt.subplots(figsize=(5.8, 5.2))
        im = ax.imshow(heat_field, origin="lower", extent=[-1, 1, -1, 1])
        ax.set_title(f"Simplified Urban Temperature Field — Hour {selected_hour}")
        ax.set_xlabel("West-East Urban Transect")
        ax.set_ylabel("South-North Urban Transect")
        fig.colorbar(im, ax=ax, label="Temperature (°C)")
        st.pyplot(fig)

    with right:
        st.markdown(
            f"""
            **Hour {selected_hour} Snapshot**

            - Time of Day: **{int(selected['Time of Day']):02d}:00**
            - Rural Temperature: **{selected['Rural Temperature (°C)']:.2f} °C**
            - Urban Temperature: **{selected['Urban Temperature (°C)']:.2f} °C**
            - UHI Intensity: **{selected['UHI Intensity (°C)']:.2f} °C**
            - Maximum Urban Temperature in Heat Map: **{heat_field.max():.2f} °C**
            """
        )

    with st.expander("View Simulation Data"):
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Simulation Data as CSV",
            data=csv,
            file_name="urban_heat_island_simulation.csv",
            mime="text/csv"
        )

    st.subheader("How the Model Works")

    st.markdown(
        """
        This is a **simplified educational model**, not a full urban climate model.
        It is designed to help students understand how different urban design factors can increase or reduce heat.

        **1. Rural temperature** follows a simple daily cycle:

        `rural_temperature = baseline_temperature + daily_temperature_cycle`

        **2. Urban heat island intensity** is estimated from several factors:

        `UHI = building_density_effect + vegetation_effect + albedo_effect + anthropogenic_heat_effect + wind_effect + cooling_design_effect`

        **3. Nighttime amplification** is added because urban heat islands are often strongest at night:

        `UHI_adjusted = UHI × night_factor`

        **4. Urban temperature** is calculated as:

        `urban_temperature = rural_temperature + UHI_adjusted`

        The key idea is simple: **dense, dark, low-vegetation cities store and release more heat, while vegetation, reflective surfaces, wind, and cooling design can reduce heat stress.**
        """
    )

    st.warning(
        "Model limitation: This lab intentionally simplifies urban climate. It does not include real land cover data, building geometry, humidity, cloud cover, radiation timing, or detailed weather conditions."
    )


# -----------------------------
# Run Page
# -----------------------------
show_climate_lab()
