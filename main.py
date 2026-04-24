from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
}

@app.get("/")
def home():
    return {"message": "LLaMA API running"}


@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()

    expected = data.get("expected_text")
    child = data.get("child_text")

    prompt = f"""
You are a friendly teacher helping a child learn to speak.

Expected sentence: "{expected}"
Child said: "{child}"

Instructions:
- Be positive and encouraging
- Identify mistakes clearly
- Suggest correction simply
- Keep response short and child-friendly
"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt}
        )

    result = response.json()

    return {
        "feedback": result
    }
