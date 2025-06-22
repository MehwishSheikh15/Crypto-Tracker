# import streamlit as st
# import requests
# import datetime
# import random

# # -------------- Setup --------------
# st.set_page_config(page_title="💰 Crypto Live Price", page_icon="🪙", layout="centered")
# st.title("💸 Real-Time Cryptocurrency Price Tracker")
# st.markdown("Get live prices for your favorite coins. Type or click to explore!")

# # -------------- Coin Emojis (Basic map) --------------
# coin_icons = {
#     "bitcoin": "🟠",
#     "ethereum": "🟣",
#     "solana": "🟩",
#     "dogecoin": "🐶",
#     "shiba inu": "🦊",
#     "cardano": "🔵",
#     "ripple": "💧",
# }

# # -------------- Fun Facts --------------
# fun_facts = {
#     "bitcoin": "Bitcoin was created by the mysterious Satoshi Nakamoto in 2009.",
#     "ethereum": "Ethereum introduced smart contracts to blockchain.",
#     "dogecoin": "Dogecoin started as a joke but now sponsors NASCAR!",
#     "shiba inu": "Shiba Inu is known as the 'Dogecoin Killer'.",
#     "solana": "Solana boasts lightning-fast transaction speeds.",
# }

# # -------------- Input & Suggestions --------------
# crypto_name = st.text_input("🔍 Enter Cryptocurrency", "Bitcoin", placeholder="Try 'eth', 'doge', etc.")

# st.markdown("💡 **Quick Picks:**")
# quick_picks = ["Bitcoin", "Ethereum", "Solana", "Dogecoin", "Shiba Inu", "Cardano", "Ripple"]
# cols = st.columns(len(quick_picks))
# for i, coin in enumerate(quick_picks):
#     if cols[i].button(coin):
#         crypto_name = coin

# # -------------- Get Price Button --------------
# if st.button("🚀 Get Price"):
#     if crypto_name.strip() == "":
#         st.warning("⚠️ Please enter a cryptocurrency name.")
#     else:
#         try:
#             with st.spinner("Fetching data..."):
#                 response = requests.post("http://localhost:8000/get-price/", json={"crypto_name": crypto_name})
#                 now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

#                 if response.status_code == 200:
#                     result = response.json().get("result")
#                     coin_key = crypto_name.strip().lower()

#                     # Coin icon
#                     icon = coin_icons.get(coin_key, "🪙")
#                     st.markdown(f"## {icon} Result for `{crypto_name.title()}`")
#                     st.code(result, language="markdown")

#                     # Fun fact
#                     if coin_key in fun_facts:
#                         st.info(f"📘 Did you know? {fun_facts[coin_key]}")

#                     # Random sentiment
#                     sentiment = random.choice(["🐂 Bullish", "🐻 Bearish", "😐 Neutral"])
#                     st.markdown(f"**📈 Market Mood:** `{sentiment}`")

#                     # Time fetched
#                     st.caption(f"📅 Last Updated: {now}")
#                 else:
#                     st.error("❌ Could not get data.")
#         except Exception as e:
#             st.error(f"⚠️ Error: {str(e)}")

# # -------------- Footer --------------
# st.markdown("---")
# st.markdown("Built with ❤️ using FastAPI + Streamlit + Coinlore API")
import streamlit as st
import requests
import datetime
import pandas as pd
import random

# ----------- Page config -----------
st.set_page_config(page_title="Crypto Tracker with Graph", layout="centered")

# ----------- Multilingual UI Texts -----------
langs = {
    "en": {
        "title": "💸 Real-Time Cryptocurrency Price Tracker with Graph",
        "search": "Enter Cryptocurrency Name",
        "currency": "Select Currency",
        "button": "🚀 Get Price",
        "history": "Last Searched Coins",
        "updated": "Last Updated",
        "error": "❌ Could not get data.",
        "placeholder": "Try Bitcoin, ETH, Doge...",
        "graph_title": "📈 Last 7 Days Price Chart (USD)",
        "quote_title": "💬 Crypto Quote",
    },
    "ur": {
        "title": "💸 اصل وقت میں کرپٹو قیمتیں گراف کے ساتھ",
        "search": "کرپٹو کرنسی کا نام درج کریں",
        "currency": "کرنسی منتخب کریں",
        "button": "🚀 قیمت حاصل کریں",
        "history": "تاریخ میں تلاش شدہ سکے",
        "updated": "آخری تازہ کاری",
        "error": "❌ ڈیٹا حاصل نہ ہو سکا",
        "placeholder": "Bitcoin، ETH، Doge آزمائیں...",
        "graph_title": "📈 گزشتہ 7 دنوں کا قیمت گراف (USD)",
        "quote_title": "💬 کرپٹو اقوال",
    },
    "ar": {
        "title": "💸 تتبع أسعار العملات الرقمية مع رسم بياني",
        "search": "أدخل اسم العملة الرقمية",
        "currency": "اختر العملة",
        "button": "🚀 الحصول على السعر",
        "history": "العملات التي تم البحث عنها",
        "updated": "آخر تحديث",
        "error": "❌ لم يتم الحصول على البيانات",
        "placeholder": "جرب Bitcoin، ETH، Doge...",
        "graph_title": "📈 الرسم البياني لآخر 7 أيام (USD)",
        "quote_title": "💬 اقتباسات العملات الرقمية",
    },
}

# ----------- Cool crypto quotations -----------
quotes = [
    "💡 'In crypto we trust, in code we rely.'",
    "🚀 'Bitcoin is the beginning of something great.' — Future vision",
    "🔐 'Not your keys, not your coins.'",
    "🌍 'Decentralize everything, empower everyone.'",
    "📈 'HODL tight — the future is volatile but promising.'",
    "⏳ 'Time in the market beats timing the market.'",
    "💎 'Diamond hands never break.'",
    "🔥 'When others panic, crypto warriors buy.'",
]

# ----------- Select language -----------
lang = st.selectbox(
    "🌐 Language",
    ["en", "ur", "ar"],
    format_func=lambda x: {"en": "English", "ur": "اردو", "ar": "العربية"}[x],
)
L = langs[lang]

st.title(L["title"])

crypto_name = st.text_input(f"🔍 {L['search']}", "", placeholder=L["placeholder"])

# Currency selector disabled, kept for UI only with fixed USD
currency = st.selectbox(f"💱 {L['currency']}", ["USD"], index=0)

if "search_history" not in st.session_state:
    st.session_state.search_history = []

@st.cache_data(ttl=3600)
def get_coingecko_coins_list():
    url = "https://api.coingecko.com/api/v3/coins/list"
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    return []

def get_coingecko_id(name, coins):
    name_lower = name.lower()
    for coin in coins:
        if name_lower == coin["id"].lower() or name_lower == coin["symbol"].lower() or name_lower == coin["name"].lower():
            return coin["id"]
    return None

def get_price_history(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": 7}
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        prices = data.get("prices", [])
        if not prices:
            return None
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    return None

coins_list = get_coingecko_coins_list()

if st.button(L["button"]):
    if not crypto_name.strip():
        st.warning("⚠️ Please enter a cryptocurrency name.")
    else:
        try:
            with st.spinner("Fetching data..."):
                backend_res = requests.post(
                    "http://localhost:8000/get-price/",
                    json={"crypto_name": crypto_name},
                )

                now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

                if backend_res.status_code == 200:
                    result = backend_res.json().get("result")

                    # Extract USD price from the result text (assumes format: "... Price: $1234.56")
                    import re
                    price_match = re.search(r"Price: \$([\d,]+\.?\d*)", result)
                    usd_price = None
                    if price_match:
                        usd_price = float(price_match.group(1).replace(",", ""))

                    price_str = f"{usd_price:,.2f} USD" if usd_price is not None else "Price info unavailable"

                    st.success(f"💰 Price info: {price_str}")
                    st.code(result, language="markdown")
                    st.caption(f"📅 {L['updated']}: {now}")

                    # Show random crypto quote
                    quote = random.choice(quotes)
                    st.info(f"{L['quote_title']}: {quote}")

                    # Save search history (limit to 10)
                    if crypto_name not in st.session_state.search_history:
                        st.session_state.search_history.append(crypto_name)
                    if len(st.session_state.search_history) > 10:
                        st.session_state.search_history.pop(0)

                    coin_id = get_coingecko_id(crypto_name, coins_list)
                    if coin_id:
                        st.markdown(f"### {L['graph_title']} (USD)")
                        df = get_price_history(coin_id)
                        if df is not None and "timestamp" in df.columns and not df.empty:
                            df = df.rename(columns={"timestamp": "Date", "price": "Price"})
                            df = df.set_index("Date")
                            st.line_chart(df["Price"])
                        else:
                            st.info("No price history data available.")
                    else:
                        st.info("CoinGecko ID not found, cannot show price chart.")

                else:
                    st.error(L["error"])
        except Exception as e:
            st.error(f"{L['error']} {str(e)}")

if st.session_state.search_history:
    st.markdown(f"### 🧠 {L['history']}")
    st.write(", ".join(st.session_state.search_history))
