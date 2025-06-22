# tools.py
import httpx

async def get_crypto_price(user_input: str) -> str:
    user_input = user_input.strip().lower()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.coinlore.net/api/tickers/")
            response.raise_for_status()
            coins = response.json().get("data", [])

            # First: Exact symbol match (e.g. "btc", "eth")
            for coin in coins:
                if user_input == coin.get("symbol", "").lower():
                    return format_crypto_response(coin)

            # Second: Exact name match (e.g. "bitcoin", "ethereum")
            for coin in coins:
                if user_input == coin.get("name", "").lower():
                    return format_crypto_response(coin)

            # Third: Partial name match (e.g. "bit", "eth")
            for coin in coins:
                if user_input in coin.get("name", "").lower():
                    return format_crypto_response(coin)

            return f"❌ Cryptocurrency '{user_input}' not found in top 100."

    except httpx.HTTPError as e:
        return f"⚠️ HTTP Error: {str(e)}"
    except Exception as e:
        return f"⚠️ Failed to fetch data: {str(e)}"

def format_crypto_response(coin: dict) -> str:
    name = coin.get("name", "Unknown")
    symbol = coin.get("symbol", "N/A")
    price = float(coin.get("price_usd", 0))
    rank = coin.get("rank", "N/A")
    market_cap = float(coin.get("market_cap_usd", 0))

    return (
        f"💰 {name} ({symbol})\n"
        f"• Price: ${price:,.2f}\n"
        f"• Rank: #{rank}\n"
        f"• Market Cap: ${market_cap:,.2f}"
    )
