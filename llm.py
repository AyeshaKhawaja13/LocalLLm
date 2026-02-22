import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "tinyllama"

def generate_response(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return "❌ Ollama server not reachable. Run: ollama serve"

    except requests.exceptions.Timeout:
        return "⏳ Model took too long to respond."

    except Exception as e:
        return f"⚠️ Error: {e}"
