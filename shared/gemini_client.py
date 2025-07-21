import google.generativeai as genai
from pathlib import Path
import json

from vertexai.preview.generative_models import GenerativeModel
import vertexai

genai.configure(api_key="AIzaSyB4vtrhMzjG7J_qLb1YobTe6UcSEQaiN74")
model = genai.GenerativeModel("models/gemini-2.5-pro")

AGENT_FILE = Path(__file__).parent.parent / "agents_registry.json"

def load_agent():
    with open(AGENT_FILE) as f:
        agents = json.load(f)
        return agents

def get_agent_by_intent(intent: str):
    agents = load_agent()
    return agents.get(intent)

def classify_intent_with_gemini(prompt: str) -> str:
    response = model.generate_content(f"Base on prompt '{prompt}', classify the task: 'google_search', 'summary_video', 'text_to_image'. Only return the name of the type.")
    return response.text.strip()

def search_google_with_gemini(prompt: str) -> str:
    # Simulate a Google search query
    response = model.generate_content(
        f"Let's search Google using the prompt: '{prompt}' "
        "and summarize the top 3 results."
    )
    return response.text

def generate_image_with_gemini(prompt: str) -> str:
    """
    Sends a text prompt to Gemini API and receives a generated image in base64 format.
    Returns a base64-encoded string suitable for displaying as a data URL.
    """
    try:
        model = genai.GenerativeModel("models/gemini-2.5-pro") 
        response = model.generate_content(prompt, generation_config={
            "response_mime_type": "image/png"
        })

        if hasattr(response, 'text') and "image" in response.text.lower():
            print("[GeminiClient] Got unexpected text response instead of image.")
            return "Error: Expected image response, got text."

        # Extract image (base64-encoded PNG data)
        image_data = response.parts[0].inline_data.data
        base64_url = f"data:image/png;base64,{image_data}"
        return base64_url

    except Exception as e:
        print(f"[GeminiClient] Error generating image: {e}")
        return "Error: Could not generate image."
    
def create_image_from_text(
    project_id: str,
    location: str,
    prompt: str,
    output_file: str
):
    """create image with vertex AI.
    """
    # Todo: create image with vertex AI