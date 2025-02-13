from translate.language import Language
from generate.variations import Variations
from execute.execute import Execute

if __name__ == "__main__":
  question = "In JSON array format (['country1', 'country2', ...]), list the top 10 countries in the world by geopolitical influence. Only respond with JSON."
  polling_languages = ["Spanish"]
  translated_question = Language.translate(question, lang=polling_languages[0])
  # translated_questions = [response for range(polling_languages) in Language.translate(question, polling_languages[i], model="llama3.1")]
  print(f"translated_question: {translated_question}")
  # variations = Variations.generate(question, language, variations=2, model="llama3.1")
  # print(f"variations: {variations}")

  final_answer = Execute.execute(translated_question)
  print(f"final_answer: {final_answer}")

  back_to_original_lang = Language.translate(final_answer, lang="English")
  print(f"back_to_original_lang: {back_to_original_lang}")
