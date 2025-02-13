import asyncio
from generate.variations import generate
from execute.execute import execute_prompt
from translate.translate import translate_text_to_lang

if __name__ == "__main__":
  question = "In JSON array format (['country1', 'country2', ...]), list the top 10 countries in the world by geopolitical influence. Only respond with JSON."

  original_language = "en"
  polling_languages = ["es"]

  translated_question = asyncio.run(translate_text_to_lang(text=question, lang=polling_languages[0]))
  print(f"translated_question: {translated_question}")

  # variations = generate(question, polling_languages[0], variations=2, model="llama3.1")
  # print(f"variations: {variations}")

  final_answer = execute_prompt(translated_question)
  print(f"final_answer: {final_answer}")

  back_to_original_lang = asyncio.run(translate_text_to_lang(text=final_answer, lang=original_language))
  print(f"back_to_original_lang: {back_to_original_lang}")
