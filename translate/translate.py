import asyncio
from googletrans import Translator, LANGUAGES
from pprint import pprint

"""
This uses the googletrans library, which is a wrapper around the Google Translate API.
Check out the docs here:
https://py-googletrans.readthedocs.io/en/latest/

USAGE:
if you wanna translate a single text to a language, use the following:
print(asyncio.run(translate_text_to_lang("Hello, world!", dest="es")))

if you wanna translate a list of texts to a language, use the following:
print(asyncio.run(bulk_translate_text_to_lang(["Hello, world!", "Goodbye, world!"], dest="es")))
"""

def print_all_languages():
  pprint(LANGUAGES)

async def translate_text(text: str, dest: str, src: str = "en") -> str:
  async with Translator() as translator:
    result = await translator.translate(text, dest=dest)
    return result.text

async def bulk_translate_text(texts: list[str], dest: str, src: str = "en") -> list[str]:
  async with Translator() as translator:
    results = await translator.translate(texts, dest=dest)
    return [result.text for result in results]