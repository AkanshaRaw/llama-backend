# from fastapi import FastAPI, Request
# import httpx
# import os

# app = FastAPI()

# API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

# HEADERS = {
#     "Authorization": f"Bearer {os.getenv('HF_TOKEN')}"
# }

# @app.get("/")
# def home():
#     return {"message": "LLaMA API running"}


# @app.post("/analyze")
# async def analyze(request: Request):
#     data = await request.json()

#     expected = data.get("expected_text")
#     child = data.get("child_text")

#     prompt = f"""
# You are a friendly teacher helping a child learn to speak.

# Expected sentence: "{expected}"
# Child said: "{child}"

# Instructions:
# - Be positive and encouraging
# - Identify mistakes clearly
# - Suggest correction simply
# - Keep response short and child-friendly
# """

#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             API_URL,
#             headers=HEADERS,
#             json={"inputs": prompt}
#         )

#     result = response.json()

#     return {
#         "feedback": result
#     }
from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

@app.get("/")
def home():
    return {"message": "LLaMA API running"}

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    expected = data.get("expected_text", "")
    child = data.get("child_text", "")

    prompt = f"""You are a friendly teacher helping a child learn to speak.

Expected sentence: "{expected}"
Child said: "{child}"

Give short, positive, child-friendly feedback (2-3 sentences max). Encourage the child and gently note any mistakes.

Feedback:"""

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            API_URL,
            headers=HEADERS,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 120,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
        )

    result = response.json()
    feedback_text = ""

    if isinstance(result, list) and len(result) > 0:
        feedback_text = result[0].get("generated_text", "")
    elif isinstance(result, dict):
        feedback_text = result.get("generated_text", "")

    feedback_text = feedback_text.strip()
    if not feedback_text:
        feedback_text = "Great effort! Keep practising and you will get even better!"

    return {"feedback": feedback_text}
