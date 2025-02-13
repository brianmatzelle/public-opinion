import requests

class Execute:
  def execute(prompt: str, model: str = "llama3.2"):
    response = requests.post(
      "http://localhost:11434/api/generate",
      json={
      "model": model, 
      "prompt": f"{prompt}",
      "stream": False,
      }
    )

    return response.json()['response']