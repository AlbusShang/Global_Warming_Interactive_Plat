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

option = st.radio("Click a country to see its international commitments and domestic policies", 
                  ("🇨🇳China", "🇩🇪Germany","🇦🇺Australia","🇮🇳India","🇨🇦Canada","🇯🇵Japan","🇰🇷South Korea","🇫🇷France","🇸🇬Singapore","🇧🇷Brazil","🇷🇺Russia"))

if st.button("Go"):
    if option == "🇨🇳China":
        policy("China")
    if option == "🇩🇪Germany":
        policy("Germany")
    if option == "🇦🇺Australia":
        policy("Australia")
    if option == "🇮🇳India":
        policy("India")
    if option == "🇨🇦Canada":
        policy("Canada")
    if option == "🇯🇵Japan":
        policy("Japan")
    if option == "🇰🇷South Korea":
        policy("South Korea")
    if option == "🇫🇷France":
        policy("France")
    if option == "🇧🇷Brazil":
        policy("Brazil")
    if option == "🇷🇺Russia":
        policy("Russia")
    if option == "🇸🇬Singapore":
        policy("Singapore")
    
    



