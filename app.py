import streamlit as st
from openai import OpenAI
from datetime import datetime

st.set_page_config(page_title="Grok Fact Checker", page_icon="🔍", layout="centered")

st.title("🔍 Grok 真假資訊分辨工具")
st.success("✅ 網頁成功載入！")

st.divider()

# ==================== Grok API 設定 ====================
api_key = st.text_input("輸入你的 XAI API Key", type="password", placeholder="sk-...")

claim = st.text_area("輸入你要查證的資訊：", height=160, placeholder="例如：香港2026年會有全民基本收入...")

if st.button("🚀 開始查證", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ 請輸入 XAI API Key")
    elif not claim.strip():
        st.warning("請輸入要查證的內容")
    else:
        with st.spinner("🤖 Grok 正在深度分析..."):
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                
                response = client.chat.completions.create(
                    model="grok-4",
                    messages=[
                        {"role": "system", "content": "你係專業事實查核專家，用繁體中文客觀分析。"},
                        {"role": "user", "content": f"請查核以下資訊：\n{claim}"}
                    ],
                    temperature=0.3,
                    max_tokens=800
                )
                
                result = response.choices[0].message.content
                st.markdown(result)
                
            except Exception as e:
                st.error(f"API 錯誤：{str(e)}")

st.caption("簡化版 | HK$38/月 完整版準備中")
