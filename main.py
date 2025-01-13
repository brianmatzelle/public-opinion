from translate.language import Language
from generate.variations import Variations

if __name__ == "__main__":
  question = Language.translate("In JSON array format, list the top 10 countries in the world by geopolitical influence. Do not include any other information.", "Spanish", model="llama3.1")
  print("question", question)
  variations = Variations.generate(question, "Spanish", variations=2, model="llama3.1")
  print("variations", variations)
