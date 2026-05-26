import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Grok Fact Checker", page_icon="🔍", layout="centered")

st.title("🔍 Grok 真假資訊分辨工具")
st.success("✅ 網頁已成功載入！")

st.divider()

# === Grok API 設定 ===
api_key = st.text_input("輸入你的 XAI API Key（必填）", type="password", placeholder="sk-...")

claim = st.text_area("輸入你要查證的資訊：", height=160, 
                     placeholder="例如：某人話新冠疫苗會改變人類 DNA...")

if st.button("🚀 開始查證", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ 請輸入 XAI API Key")
    elif not claim.strip():
        st.warning("請輸入要查證的內容")
    else:
        with st.spinner("🤖 Grok 正在深度分析中..."):
            try:
                client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
                
                response = client.chat.completions.create(
                    model="grok-4",
                    messages=[
                        {"role": "system", "content": "你係專業、中立的事實查核專家。用繁體中文清晰分析。"},
                        {"role": "user", "content": f"請查核以下資訊真假：\n{claim}"}
                    ],
                    temperature=0.3,
                    max_tokens=900
                )
                
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"API 呼叫失敗：{str(e)}")
                st.info("請檢查 API Key 是否正確，或者額度是否足夠。")

st.caption("HK$38/月 完整版開發中 | 目前為測試版")
