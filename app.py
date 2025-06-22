# app.py
import streamlit as st
import requests
import datetime
import pandas as pd
import random

# ---------- Multilingual UI ----------
langs = {
    "en": {
        "title": "💸 Real-Time Cryptocurrency Price Tracker",
        "search": "Enter Cryptocurrency Name",
        "button": "🚀 Get Price",
        "history": "Last Searched Coins",
        "updated": "Last Updated",
        "error": "❌ Could not get data.",
        "placeholder": "Try Bitcoin, ETH, Doge...",
        "graph_title": "📈 Last 7 Days Price Chart (USD)",
        "quote_title": "💬 Crypto Quote",
    },
    "ur": {
        "title": "💸 اصل وقت میں کرپٹو قیمتیں",
        "search": "کرپٹو کرنسی کا نام درج کریں",
        "button": "🚀 قیمت حاصل کریں",
        "history": "تاریخ میں تلاش شدہ سکے",
        "updated": "آخری تازہ کاری",
        "error": "❌ ڈیٹا حاصل نہ ہو سکا",
        "placeholder": "Bitcoin، ETH، Doge آزمائیں...",
        "graph_title": "📈 گزشتہ 7 دنوں کا قیمت گراف (USD)",
        "quote_title": "💬 کرپٹو اقوال",
    },
    "ar": {
        "title": "💸 تتبع أسعار العملات الرقمية",
        "search": "أدخل اسم العملة الرقمية",
        "button": "🚀 الحصول على السعر",
        "history": "العملات التي تم البحث عنها",
        "updated": "آخر تحديث",
        "error": "❌ لم يتم الحصول على البيانات",
        "placeholder": "جرب Bitcoin، ETH، Doge...",
        "graph_title": "📈 الرسم البياني لآخر 7 أيام (USD)",
        "quote_title": "💬 اقتباسات العملات الرقمية",
    },
}

quotes = [
    "💡 'In crypto we trust, in code we rely.'",
    "🚀 'Bitcoin is the beginning of something great.'",
    "🔐 'Not your keys, not your coins.'",
    "🌍 'Decentralize everything, empower everyone.'",
    "📈 'HODL tight — the future is volatile but promising.'",
    "⏳ 'Time in the market beats timing the market.'",
    "💎 'Diamond hands never break.'",
    "🔥 'When others panic, crypto warriors buy.'",
]

# ----------- Config -----------
st.set_page_config(page_title="Crypto Tracker", layout="centered")

lang = st.selectbox("🌐 Language", ["en", "ur", "ar"],
                    format_func=lambda x: {"en": "English", "ur": "اردو", "ar": "العربية"}[x])
L = langs[lang]
st.title(L["title"])

crypto_name = st.text_input(f"🔍 {L['search']}", "", placeholder=L["placeholder"])
if "search_history" not in st.session_state:
    st.session_state.search_history = []

@st.cache_data(ttl=3600)
def get_coins_list():
    url = "https://api.coingecko.com/api/v3/coins/list"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else []

@st.cache_data(ttl=3600)
def get_price_history(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": 7}
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        prices = data.get("prices", [])
        df = pd.DataFrame(prices, columns=["timestamp", "price"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df
    return None

def get_coin_id(name, coins):
    name = name.lower()
    for coin in coins:
        if name in [coin["id"].lower(), coin["symbol"].lower(), coin["name"].lower()]:
            return coin["id"]
    return None

def get_current_price_coinlore(query):
    try:
        response = requests.get("https://api.coinlore.net/api/tickers/")
        if response.status_code != 200:
            return None
        data = response.json().get("data", [])
        query = query.lower()
        for coin in data:
            if query in [coin["symbol"].lower(), coin["name"].lower()]:
                return {
                    "name": coin["name"],
                    "symbol": coin["symbol"],
                    "price": float(coin["price_usd"]),
                    "rank": coin["rank"],
                    "market_cap": float(coin["market_cap_usd"]),
                }
        return None
    except Exception:
        return None

# ----------- Action Button -----------
if st.button(L["button"]):
    if not crypto_name.strip():
        st.warning("⚠️ Please enter a cryptocurrency name.")
    else:
        with st.spinner("Fetching data..."):
            # Step 1: Get current price (from CoinLore)
            price_info = get_current_price_coinlore(crypto_name)
            now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

            if price_info:
                price_str = f"{price_info['price']:,.2f} USD"
                st.success(f"💰 {price_info['name']} ({price_info['symbol']})")
                st.write(f"• **Price**: {price_str}")
                st.write(f"• **Rank**: #{price_info['rank']}")
                st.write(f"• **Market Cap**: ${price_info['market_cap']:,.2f}")
                st.caption(f"📅 {L['updated']}: {now}")

                quote = random.choice(quotes)
                st.info(f"{L['quote_title']}: {quote}")

                if crypto_name not in st.session_state.search_history:
                    st.session_state.search_history.append(crypto_name)
                if len(st.session_state.search_history) > 10:
                    st.session_state.search_history.pop(0)

                coins_list = get_coins_list()
                coin_id = get_coin_id(crypto_name, coins_list)
                if coin_id:
                    st.markdown(f"### {L['graph_title']}")
                    df = get_price_history(coin_id)
                    if df is not None and not df.empty:
                        st.line_chart(df.set_index("timestamp")["price"])
                    else:
                        st.info("No price history available.")
                else:
                    st.warning("📉 Could not plot chart. Coin not found on CoinGecko.")
            else:
                st.error(L["error"])

if st.session_state.search_history:
    st.markdown(f"### 🧠 {L['history']}")
    st.write(", ".join(st.session_state.search_history))

