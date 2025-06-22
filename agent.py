# agent.py
from dotenv import load_dotenv
import os
import openai
from tools import get_crypto_price

# Load .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def run_crypto_agent(crypto_name: str) -> str:
    crypto_name = crypto_name.strip().lower()
    tool_result = await get_crypto_price(crypto_name)
    return tool_result
