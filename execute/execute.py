import requests

# This module calls the local ollama server to execute the prompt
# If you don't have ollama installed and running, this won't work

def execute_prompt(prompt: str, model: str):
  response = requests.post(
    "http://localhost:11434/api/generate",
    json={
    "model": model, 
    "prompt": f"{prompt}",
    "stream": False,
    }
  )

  return response.json()['response']