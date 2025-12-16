import streamlit as st
import xarray as xr
import numpy as np
import pandas as pd
import pydeck as pdk
import matplotlib as mpl
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="🌍 Interactive Map for Global Warming", layout="wide")

# 你的 ERA5 数据目录（按你给的路径）
DATA_DIR = (
    Path.home()
    / "Desktop"
    / "Albus"
    / "工作生活"
    / "实习"
    / "千禧年计划"
    / "Global Warming Interactive Platform"
    / "ERA5_monthly"
)

# 兜底：如果你实际目录是下划线版本
if not DATA_DIR.exists():
    alt = (
        Path.home()
        / "Desktop"
        / "Albus"
        / "工作生活"
        / "实习"
        / "千禧年计划"
        / "Global_Warming_Interactive_Platform"
        / "ERA5_monthly"
    )
    if alt.exists():
        DATA_DIR = alt

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
    # 处理边界
    lat_edges = edges_from_centers(lat)
    lon_edges = edges_from_centers(lon)

    # 色标范围：分位数，避免极端值挤压
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

    # 生成每个格子的 polygon（四角）
    # 注意：pydeck polygon 坐标顺序是 [lon, lat]
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


# ----------------------------
# UI
# ----------------------------
st.title("🌍 Interactive Map for Global Warming")

if not DATA_DIR.exists():
    st.error(f"找不到 ERA5 数据文件夹：{DATA_DIR}")
    st.stop()

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
    year = st.slider("Select a year", min_value=year_min, max_value=year_max, value=year_min, step=1)

    st.markdown("---")
    cmap_name = st.selectbox("Color", ["turbo", "viridis", "plasma", "inferno"], index=0)
    opacity = st.slider("Opacity", 0.2, 1.0, 0.85, 0.05)
    show_edges = st.toggle("Show Grid", value=False)

    st.caption(f"数据目录：{DATA_DIR}")

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
        map_style=BASEMAP,  # ✅ 国界/海岸线/地名
        tooltip=tooltip,
        
    )

    st.pydeck_chart(deck, use_container_width=True)

    st.markdown("**Colorbar**")
    st.pyplot(draw_colorbar(vmin, vmax, cmap_name), use_container_width=False)

    with st.expander("Current slice info"):
        st.write(pd.Series(df_poly["temp_c"]).describe(percentiles=[0.05, 0.5, 0.95]))