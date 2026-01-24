import streamlit as st
import xarray as xr
import numpy as np
import pandas as pd
import pydeck as pdk
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path

# ✅ 用于 deck.gl click 事件回传
from streamlit_deckgl import st_deckgl

st.set_page_config(page_title="🌍 Interactive Map for Global Warming", layout="wide")

# Map_Interactive.py 所在目录
APP_DIR = Path(__file__).resolve().parent

# ERA5 数据目录（与 Map_Interactive.py 同级）
DATA_DIR = APP_DIR / "ERA5_monthly"

# 检查数据目录是否存在
if not DATA_DIR.exists():
    st.error(f"找不到 ERA5 数据文件夹：{DATA_DIR}")
    st.stop()

MONTH_FILE_TMPL = "t2m_2deg_month_{:02d}.nc"
ANNUAL_FILE = "t2m_2deg_annual_mean.nc"

# 带国界/海岸线的底图（无需 token）
BASEMAP = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"


def k_to_c(k):
    return k - 273.15


def draw_colorbar(vmin, vmax, cmap_name="turbo"):
    fig, ax = plt.subplots(figsize=(7.2, 0.55), dpi=160)
    fig.subplots_adjust(bottom=0.45)
    cmap = mpl.colormaps.get_cmap(cmap_name)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, orientation="horizontal")
    cb.set_label("Temperature (°C)")
    return fig


def file_for_mode(mode):
    # mode: "Annual" 或 1..12
    if mode == "Annual":
        return DATA_DIR / ANNUAL_FILE
    else:
        return DATA_DIR / MONTH_FILE_TMPL.format(int(mode))


@st.cache_data(show_spinner=False)
def get_years_for_file(path):
    ds = xr.open_dataset(path)
    years = np.unique(pd.to_datetime(ds["valid_time"].values).year)
    ds.close()
    return years


@st.cache_data(show_spinner=True)
def load_year_field(mode, year):
    """
    读取某个月(1-12)或 Annual 的某一年气温场
    输出：lat(1d), lon(1d, -180..180 已排序), temp_c(2d: lat x lon)
    """
    path = file_for_mode(mode)
    ds = xr.open_dataset(path)

    time_index = pd.to_datetime(ds["valid_time"].values)
    mask = (time_index.year == int(year))

    if mask.sum() == 0:
        ds.close()
        raise ValueError(f"No data for year={year} in {path.name}")

    # 取该年的时间点（保险起见：若不止一个就平均）
    t2m = ds["t2m"].sel(valid_time=ds["valid_time"].values[mask]).mean("valid_time")

    # 经度 0..360 -> -180..180，并排序（防止日界线断裂）
    lon = t2m["longitude"]
    lon_fixed = (((lon + 180) % 360) - 180)
    t2m = t2m.assign_coords(longitude=lon_fixed).sortby("longitude")

    lat = t2m["latitude"].values
    lon_sorted = t2m["longitude"].values
    temp_c = k_to_c(t2m.values).astype(np.float32)

    ds.close()
    return lat, lon_sorted, temp_c


def edges_from_centers(arr):
    """
    给定中心点坐标（等间距），返回边界坐标。
    例：centers=[...], edges 长度 = len(centers)+1
    """
    arr = np.asarray(arr, dtype=np.float64)
    d = np.diff(arr)
    step = np.median(np.abs(d)) if len(d) else 1.0
    edges = np.empty(len(arr) + 1, dtype=np.float64)
    edges[1:-1] = (arr[:-1] + arr[1:]) / 2.0
    edges[0] = arr[0] - step / 2.0
    edges[-1] = arr[-1] + step / 2.0
    return edges


@st.cache_data(show_spinner=True)
def grid_to_polygons(lat, lon, temp_c, cmap_name="turbo"):
    """
    把 2D 栅格转成 PolygonLayer 需要的 DataFrame
    每格一个矩形 polygon，带 fill_color
    """
    lat_edges = edges_from_centers(lat)
    lon_edges = edges_from_centers(lon)

    vals = temp_c.ravel()
    vals = vals[np.isfinite(vals)]
    vmin = float(np.nanpercentile(vals, 2))
    vmax = float(np.nanpercentile(vals, 98))
    if vmax <= vmin:
        vmax = vmin + 1.0

    cmap = mpl.colormaps.get_cmap(cmap_name)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

    records = []
    nlat = len(lat)
    nlon = len(lon)

    for i in range(nlat):
        lat0, lat1 = float(lat_edges[i]), float(lat_edges[i + 1])
        for j in range(nlon):
            val = float(temp_c[i, j])
            if not np.isfinite(val):
                continue

            lon0, lon1 = float(lon_edges[j]), float(lon_edges[j + 1])

            rgba = cmap(norm(val))
            r, g, b = (np.array(rgba[:3]) * 255).astype(int).tolist()

            poly = [
                [lon0, lat0],
                [lon1, lat0],
                [lon1, lat1],
                [lon0, lat1],
            ]

            records.append(
                {"polygon": poly, "temp_c": val, "fill_color": [r, g, b, 190]}
            )

    df_poly = pd.DataFrame.from_records(records)
    return df_poly, vmin, vmax


@st.cache_data(show_spinner=True)
def load_point_timeseries(mode, lat0, lon0):
    """
    mode: "Annual" 或 1..12
    返回：years(1d), temps_c(1d), nearest_lat, nearest_lon
    """
    path = file_for_mode(mode)
    ds = xr.open_dataset(path)

    time_index = pd.to_datetime(ds["valid_time"].values)
    years_all = time_index.year

    t2m = ds["t2m"]

    # 经度修正到 [-180, 180)
    lon = t2m["longitude"]
    lon_fixed = (((lon + 180) % 360) - 180)
    t2m = t2m.assign_coords(longitude=lon_fixed).sortby("longitude")

    # 点击经度也规范化到 [-180, 180)
    lon0_fixed = ((float(lon0) + 180) % 360) - 180

    # 选最近邻格点
    point = t2m.sel(latitude=float(lat0), longitude=float(lon0_fixed), method="nearest")

    # 保险起见按年聚合（即使一年有多时刻也能处理）
    df = pd.DataFrame({"year": years_all, "t2m": point.values})
    series = df.groupby("year")["t2m"].mean()

    years = series.index.values.astype(int)
    temps_c = (series.values - 273.15).astype(np.float32)

    nearest_lat = float(point["latitude"].values)
    nearest_lon = float(point["longitude"].values)

    ds.close()
    return years, temps_c, nearest_lat, nearest_lon


def plot_timeseries(years, temps_c, mode, nearest_lat, nearest_lon):
    fig, ax = plt.subplots(figsize=(8.2, 3.6), dpi=160)
    ax.plot(years, temps_c)

    if mode == "Annual":
        title = f"Annual Mean Temperature Trend @ nearest grid ({nearest_lat:.2f}, {nearest_lon:.2f})"
    else:
        title = f"Month {int(mode):02d} Temperature Trend @ nearest grid ({nearest_lat:.2f}, {nearest_lon:.2f})"

    ax.set_title(title)
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature (°C)")
    ax.grid(True, alpha=0.25)
    return fig


def parse_click_latlon(event_dict):
    """
    尽量兼容不同 deck.gl 事件 payload 格式。
    目标：返回 (lat, lon) 或 None
    """
    if not isinstance(event_dict, dict):
        return None

    # 常见：{'coordinate': [lon, lat, ...]}
    coord = event_dict.get("coordinate")
    if isinstance(coord, (list, tuple)) and len(coord) >= 2:
        lon, lat = coord[0], coord[1]
        return float(lat), float(lon)

    # 有些会叫 lngLat: [lng, lat]
    lnglat = event_dict.get("lngLat") or event_dict.get("lnglat")
    if isinstance(lnglat, (list, tuple)) and len(lnglat) >= 2:
        lon, lat = lnglat[0], lnglat[1]
        return float(lat), float(lon)

    # 兜底：直接提供 lat/lon
    if "lat" in event_dict and "lon" in event_dict:
        return float(event_dict["lat"]), float(event_dict["lon"])
    if "latitude" in event_dict and "longitude" in event_dict:
        return float(event_dict["latitude"]), float(event_dict["longitude"])

    return None


# ----------------------------
# UI
# ----------------------------
st.title("🌍 Interactive Map for Global Warming")

# 文件存在性检查
missing = []
for m in range(1, 13):
    if not (DATA_DIR / MONTH_FILE_TMPL.format(m)).exists():
        missing.append(MONTH_FILE_TMPL.format(m))
if not (DATA_DIR / ANNUAL_FILE).exists():
    missing.append(ANNUAL_FILE)

if missing:
    st.warning("以下文件不存在（请确认文件名与目录）：")
    st.code("\n".join(missing))
    st.stop()

col_left, col_right = st.columns([1, 3])

with col_left:
    st.subheader("控制面板")

    mode_label = st.selectbox(
        "Select a month (or annual mean)",
        options=["Annual"] + [f"{m:02d}" for m in range(1, 13)],
        index=0,
        format_func=lambda x: "Annual (全年平均)" if x == "Annual" else f"Month {x}",
    )
    mode = "Annual" if mode_label == "Annual" else int(mode_label)

    years = get_years_for_file(file_for_mode(mode))
    year_min, year_max = int(years.min()), int(years.max())
    year = st.slider(
        "Select a year",
        min_value=year_min,
        max_value=year_max,
        value=year_min,
        step=1,
    )

    st.markdown("---")
    cmap_name = st.selectbox("Color", ["turbo", "viridis", "plasma", "inferno"], index=0)
    opacity = st.slider("Opacity", 0.2, 1.0, 0.85, 0.05)
    show_edges = st.toggle("Show Grid", value=False)

    st.caption(f"数据目录：{DATA_DIR}")

    st.markdown("---")
    st.subheader("📍 Click-to-plot")
    st.caption("直接在右侧主地图上点击一个格子：\n- Month 模式：画该月逐年曲线\n- Annual 模式：画年平均逐年曲线")

with col_right:
    lat, lon, temp_c = load_year_field(mode, year)
    df_poly, vmin, vmax = grid_to_polygons(lat, lon, temp_c, cmap_name=cmap_name)

    if mode == "Annual":
        title = f"{year} — Annual Mean Temperature"
    else:
        title = f"{year} — Month {mode:02d} Mean Temperature"

    st.subheader(title)

    poly_layer = pdk.Layer(
        "PolygonLayer",
        data=df_poly,
        get_polygon="polygon",
        pickable=True,
        filled=True,
        stroked=bool(show_edges),
        get_fill_color="fill_color",
        get_line_color=[0, 0, 0, 60],
        line_width_min_pixels=0.5,
        opacity=float(opacity),
    )

    view_state = pdk.ViewState(latitude=20, longitude=0, zoom=1.0, pitch=0)

    tooltip = {
        "html": "<b>Temp</b>: {temp_c} °C",
        "style": {"backgroundColor": "rgba(0,0,0,0.75)", "color": "white"},
    }

    deck = pdk.Deck(
        layers=[poly_layer],
        initial_view_state=view_state,
        map_style=BASEMAP,
        tooltip=tooltip,
    )

    # ✅ 监听 click 事件（返回事件 payload）
    event = st_deckgl(deck, height=560, key="main_deck", events=["click"])

    # ---- Colorbar & slice info ----
    st.markdown("**Colorbar**")
    st.pyplot(draw_colorbar(vmin, vmax, cmap_name), use_container_width=False)

    with st.expander("Current slice info"):
        st.write(pd.Series(df_poly["temp_c"]).describe(percentiles=[0.05, 0.5, 0.95]))

    # ----------------------------
    # 点击 -> 时间序列
    # ----------------------------
    st.markdown("---")
    st.subheader("📈 Temperature trend at clicked location (1940–2024)")

    clicked = parse_click_latlon(event)
    if clicked is not None:
        st.session_state["clicked_lat"], st.session_state["clicked_lon"] = clicked

    if "clicked_lat" not in st.session_state:
        st.info("Please select a point on the map above.")
    else:
        lat0 = float(st.session_state["clicked_lat"])
        lon0 = float(st.session_state["clicked_lon"])
        st.write(f"Selected click: **lat={lat0:.4f}**, **lon={lon0:.4f}**")

        years_ts, temps_ts, near_lat, near_lon = load_point_timeseries(mode, lat0, lon0)

        # 目标范围：1940–2024（若文件不全，会自动按可用年份截取）
        mask = (years_ts >= 1940) & (years_ts <= 2024)
        years_ts = years_ts[mask]
        temps_ts = temps_ts[mask]

        if len(years_ts) == 0:
            st.warning("该文件内没有落在 1940–2024 的年份数据（请检查 valid_time 覆盖范围）。")
        else:
            st.pyplot(plot_timeseries(years_ts, temps_ts, mode, near_lat, near_lon), use_container_width=True)

            with st.expander("Point info"):
                st.write(
                    {
                        "mode": "Annual" if mode == "Annual" else f"Month {int(mode):02d}",
                        "clicked_lat": lat0,
                        "clicked_lon": lon0,
                        "nearest_grid_lat": near_lat,
                        "nearest_grid_lon": near_lon,
                        "years_covered": f"{int(years_ts.min())}–{int(years_ts.max())}",
                    }
                )

if st.button("See how each country is acting in response to climate change →"):
    st.switch_page("pages/Nation_Commitments.py")

if st.button("Want to test how much I know about climate science and climate change→"):
    st.switch_page("pages/ClimateQuiz.py")
