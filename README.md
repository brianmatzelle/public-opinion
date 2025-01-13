# About



## Procedure

Listed are different steps -- each step is a folder in the repository.

1. Input questions manually that we'd like to ask.
2. Module - Using a translation LLM, translate the question(s) to N many languages.
3. Module - Using a JSON generation LLM specific to each language, generate N variations for the question(s) in each language, respectively.
4. Module - Translate results of the JSON generation LLM back to English.
5. Module - For now, create matplotlib graphs for each question in each language (later we'll consolidate the data and create a single graph).
