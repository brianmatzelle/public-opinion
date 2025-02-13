import requests

# call 
# curl http://localhost:11434/api/generate -d '{
#   "model": "llama3.2",
#   "prompt": "Translate the following question to the following language: {question} -> {language}"
# }'
# with the question and language, return the translated question
class Language:
  def translate(prompt: str, lang: str, model: str = "llama3.2") -> str:
    response = requests.post(
      "http://localhost:11434/api/generate",
      json={
      "model": model, 
      "prompt": f"Translate the following prompt to {lang}. Do not answer the prompt. Include nothing else but the translated prompt:\n {prompt}",
      "stream": False,
      }
    )

    return response.json()['response']
