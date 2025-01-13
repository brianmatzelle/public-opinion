import requests

from translate.language import Language

class Variations:
  def generate(question: str, language: str, variations: int = 5, model: str = "llama3.1") -> str:
    # translate the variations prompt to the language
    variations_prompt = Language.translate(f"Generate {variations} variations of the following question in JSON array format ['prompt1', 'prompt2', ...]. DO NOT change the meaning of the question, and DO NOT answer the question.", language)
    response = requests.post(
      "http://localhost:11434/api/generate",
      json={"model": model, "prompt": f"{variations_prompt}\n{question}", "stream": False}
    )
    return response.json()['response']
