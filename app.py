import streamlit as st
import stripe
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="Grok Fact Checker", page_icon="🔍", layout="centered")

# ==================== Stripe Test Mode ====================
STRIPE_SECRET_KEY = "sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"   # ← 改成你自己的
stripe.api_key = STRIPE_SECRET_KEY
PRICE_ID = "price_xxxxxxxxxxxxxxxxxxxxxxxx"   # ← HK$38 的 Price ID

# ==================== CSS ====================
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .premium-badge { background: linear-gradient(90deg, #4f46e5, #7c3aed); padding: 6px 14px; border-radius: 20px; }
    </style>
""", unsafe_allow_html=True)

# ==================== Session State ====================
if "is_premium" not in st.session_state:
    st.session_state.is_premium = False
if "premium_until" not in st.session_state:
    st.session_state.premium_until = None
if "history" not in st.session_state:
    st.session_state.history = []
if "custom_prompt" not in st.session_state:
    st.session_state.custom_prompt = ""

# ==================== Header ====================
col1, col2 = st.columns([1, 6])
with col1: st.markdown("# 🔍")
with col2: st.title("Grok 真假資訊分辨工具")

st.caption("專業事實查核 • HK$38/月 尊享版")

st.divider()

# ==================== Sidebar ====================
with st.sidebar:
    st.header("💰 月費計劃 - HK$38/月")
    
    if st.session_state.is_premium:
        st.markdown("<span class='premium-badge'>✅ 月費用戶</span>", unsafe_allow_html=True)
        st.success(f"有效至：{st.session_state.premium_until.strftime('%Y-%m-%d')}")
    else:
        st.markdown("**HK$38 / 月**")
        st.write("• 無限查證 + 全部進階功能")
    
    if st.button("💳 立即訂閱 HK$38/月 (Test Mode)", use_container_width=True):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{'price': PRICE_ID, 'quantity': 1}],
                mode='subscription',
                success_url="https://your-app-name.streamlit.app/?success=true",
                cancel_url="https://your-app-name.streamlit.app/?cancel=true",
            )
            st.markdown(f'<script>window.open("{session.url}", "_blank");</script>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"錯誤: {str(e)}")

# ==================== 訂閱成功處理 ====================
if st.query_params.get("success"):
    st.session_state.is_premium = True
    st.session_state.premium_until = datetime.now() + timedelta(days=30)
    st.success("🎉 訂閱成功！所有進階功能已解鎖")
    st.rerun()

# ==================== 自訂提示詞 (月費專享) ====================
if st.session_state.is_premium:
    with st.expander("⚙️ 自訂分析提示詞"):
        st.session_state.custom_prompt = st.text_area(
            "自訂 Grok 分析風格（留空則使用預設）",
            value=st.session_state.custom_prompt,
            height=100,
            placeholder="例如：用香港人角度分析，特別注重政治偏見..."
        )

# ==================== 每日精選假新聞 (月費專享) ====================
if st.session_state.is_premium:
    st.divider()
    st.subheader("📰 今日精選假新聞")
    fake_news = [
        "「某名人已去世」類假消息",
        "「某品牌產品有毒」未經證實",
        "「2026年將實施XX新政策」未確認版本"
    ]
    for news in fake_news:
        st.warning(f"⚠️ {news}")

# ==================== 主查證區 ====================
claim = st.text_area("輸入你要查證的資訊：", height=150, placeholder="輸入陳述...")

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 開始查證", type="primary", use_container_width=True):
        if claim.strip():
            with st.spinner("Grok 深度分析中..."):
                # 在這裡加入 Grok API 呼叫（可貼之前版本）
                result = "【判斷結果】 ⚠️ 半真半假\n【可信度】 中\n詳細解釋..."
                
                st.success("✅ 分析完成")
                
                # 儲存歷史
                st.session_state.history.append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "claim": claim[:120],
                    "result": result
                })
        else:
            st.warning("請輸入內容")

with col2:
    if st.session_state.is_premium and st.button("📦 批量查證", use_container_width=True):
        st.info("批量查證模式已啟用（開發中，可一次輸入多段文字）")

# ==================== 歷史記錄 + AI 總結 ====================
if st.session_state.is_premium and st.session_state.history:
    st.divider()
    st.subheader("📖 我的查證歷史")
    
    for item in reversed(st.session_state.history[-8:]):
        with st.expander(f"{item['time']} | {item['claim']}"):
            st.write(item['result'])
    
    if st.button("🤖 AI 自動總結歷史報告"):
        summary = "根據你過去的查證，主要關注政治、醫療、科技類資訊，較多半真半假內容..."
        st.info(f"AI 總結：{summary}")
    
    if st.button("📥 匯出所有歷史"):
        data = json.dumps(st.session_state.history, ensure_ascii=False, indent=2)
        st.download_button("下載 JSON 報告", data, "fact_check_history.json")

st.divider()
st.caption("HK$38/月 尊享版 • 所有進階功能已開啟 • Stripe Test Mode")