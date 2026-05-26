import streamlit as st

st.set_page_config(page_title="Grok Fact Checker", page_icon="🔍", layout="centered")

st.title("🔍 Grok 真假資訊分辨工具")
st.success("✅ 網頁成功載入！（Stripe 暫時停用）")

st.divider()

claim = st.text_area("輸入你要查證的資訊：", height=160)

if st.button("🚀 開始查證", type="primary", use_container_width=True):
    if claim.strip():
        st.info("🤖 Grok 正在分析中...（功能開發中）")
        st.write("你輸入咗：", claim)
    else:
        st.warning("請輸入內容")

st.caption("簡化測試版 | HK$38/月 版本準備中")
