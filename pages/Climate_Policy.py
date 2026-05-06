import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Climate Policies of Each Country", page_icon="📖", layout="wide")
st.title("Climate Policies of Each Country")

HERE = Path(__file__).resolve().parent  # pages/ 目录（Nation_Commitments.py 所在目录）

def policy(country: str, txt_dir: Path = HERE, expanded: bool = False):
    """
    Create one expander for a country.
    Inside expander: render the markdown content from <txt_dir>/<country>.txt
    """
    file_path = txt_dir / f"{country}.txt"

    with st.expander(country, expanded=expanded):
        if not file_path.exists():
            st.error(f"Missing file: {file_path.name}")
            return

        # 读取文本（默认 UTF-8；如果你txt是GBK可改成 encoding="gbk"）
        try:
            md = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            md = file_path.read_text(encoding="gbk", errors="ignore")

        st.markdown(md)

# 国家列表（显示名称 -> 文件名称）
countries = {
    "🇦🇺Australia": "Australia",
    "🇧🇷Brazil": "Brazil",
    "🇨🇦Canada": "Canada",
    "🇨🇳China": "China",
    "🇫🇷France": "France",
    "🇩🇪Germany": "Germany",
    "🇮🇳India": "India",
    "🇯🇵Japan": "Japan",
    "🇰🇷South Korea": "South Korea",
    "🇷🇺Russia": "Russia",
    "🇸🇬Singapore": "Singapore"
}

# 按字母排序
sorted_options = sorted(countries.keys(), key=lambda x: x.split("🇦🇺")[-1])

option = st.radio(
    "Click a country to see its international commitments and domestic policies",
    sorted_options
)

if st.button("Go"):
    policy(countries[option])