# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_crypto_agent

app = FastAPI()

class Query(BaseModel):
    crypto_name: str

@app.post("/get-price/")
async def get_crypto(query: Query):
    response = await run_crypto_agent(query.crypto_name)
    return {"result": response}
