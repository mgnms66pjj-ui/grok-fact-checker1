# grok-fact-checker
import streamlit as st
from openai import OpenAI
import os

# ==================== 頁面設定 + 美化 ====================
st.set_page_config(
    page_title="Grok Fact Checker",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 自訂 CSS 美化
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTextArea textarea {
        background-color: #1e2533;
        color: #ffffff;
        border-radius: 12px;
        border: 2px solid #334155;
    }
    .stButton button {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white;
        border-radius: 12px;
        height: 52px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
    .result-box {
        background-color: #1e2533;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #334155;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    h1 {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #a5b4fc, #c4d0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== Header ====================
col1, col2 = st.columns([1, 6])
with col1:
    st.markdown("# 🔍")
with col2:
    st.title("Grok 真假資訊分辨工具")

st.markdown("""
    <p style='font-size: 1.1rem; color: #94a3b8; margin-top: -15px;'>
        使用 xAI Grok 即時分析資訊真偽 • 專業 • 中立 • 快速
    </p>
""", unsafe_allow_html=True)

st.divider()

# ==================== Sidebar ====================
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input(
        "XAI API Key",
        type="password",
        placeholder="sk-...",
        help="前往 https://console.x.ai 申請"
    )
    
    model = st.selectbox(
        "選擇 Grok 模型",
        ["grok-4", "grok-4.3"],
        index=0,
        help="grok-4.3 更強大但費用較高"
    )
    
    st.markdown("---")
    st.markdown("### 💡 使用提示")
    st.markdown("""
    - 輸入明確陳述效果最好  
    - 支援繁體中文同英文  
    - 政治、醫療、科技類最準  
    - AI 分析僅供參考
    """)

# ==================== 主介面 ====================
claim = st.text_area(
    "輸入你要查證的資訊：",
    placeholder="例如：香港 2026 年會實施全民基本收入...",
    height=160,
    label_visibility="visible"
)

# 分析按鈕
if st.button("🚀 開始查證", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ 請輸入 XAI API Key")
    elif not claim.strip():
        st.warning("⚠️ 請輸入要查證的內容")
    else:
        with st.spinner("🤖 Grok 正在深度分析中..."):
            try:
                client = OpenAI(
                    api_key=api_key,
                    base_url="https://api.x.ai/v1"
                )
                
                system_prompt = """
                你是一位極度專業、中立、嚴謹的事實查核專家。
                請用以下格式用繁體中文回覆：

                【判斷結果】 ✅ 真 / ❌ 假 / ⚠️ 半真半假 / ❓ 無法確定
                【可信度】 高 / 中 / 低
                【詳細解釋】（詳細、客觀、有條理）
                【可靠來源建議】
                【風險提醒】
                """
                
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"請查核以下資訊：\n\n{claim}"}
                    ],
                    temperature=0.25,
                    max_tokens=1200
                )
                
                result = response.choices[0].message.content
                
                # 美化結果顯示
                st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                st.success("✅ 分析完成")
                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.caption("⚠️ 此結果由 AI 生成，建議再自行查閱多個權威來源交叉驗證。")
                
            except Exception as e:
                st.error(f"❌ 分析失敗：{str(e)}")

# ==================== Footer ====================
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Made with ❤️ by Grok**")
with col2:
    st.markdown("**Powered by xAI**")
with col3:
    st.markdown("**Streamlit**")

st.caption("美化版本 | 支援繁體中文 | 2026")
streamlit
openai>=1.0.0