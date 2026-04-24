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

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

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

    response = model.generate(prompt)

    return jsonify({
        "feedback": response
    })
