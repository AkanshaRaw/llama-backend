from fastapi import FastAPI
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

@app.post("/generate-poem")
async def generate_poem(data: dict):
    try:
        prompt = data.get("text", "")

        payload = {
            "inputs": f"Write a short beautiful poem about {prompt}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL, headers=HEADERS, json=payload)

        result = response.json()

        # Extract text properly
        if isinstance(result, list):
            return {"poem": result[0]["generated_text"]}
        else:
            return {"poem": "Model is loading, try again"}

    except Exception as e:
        return {"poem": "Error occurred"}
