import streamlit as st

st.set_page_config(page_title="Grok Fact Checker", page_icon="🔍", layout="centered")

st.title("🔍 Grok 真假資訊分辨工具")
st.success("✅ 網頁已成功載入！")

st.divider()

st.write("**目前狀態：** 基本版本運行正常")

claim = st.text_area("輸入你要查證的資訊：", height=150, 
                     placeholder="例如：某人話新冠疫苗會改變 DNA...")

if st.button("🚀 開始查證", type="primary", use_container_width=True):
    if claim.strip():
        st.info("🔄 分析功能開發中...")
        st.write("你輸入：", claim)
    else:
        st.warning("請輸入內容")

st.caption("簡化測試版 | HK$38/月 完整版準備中")
