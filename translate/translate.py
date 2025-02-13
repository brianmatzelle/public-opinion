import asyncio
from googletrans import Translator

# This uses the googletrans library, which is a wrapper around the Google Translate API.
# Check out the docs here:
# https://py-googletrans.readthedocs.io/en/latest/

async def translate_text_to_lang(text: str, lang: str):
  async with Translator() as translator:
    result = await translator.translate(text, dest=lang)
    return result

# print(asyncio.run(translate_text_to_lang("Hello, world!", dest="es")))