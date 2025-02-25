# About



## Procedure

Listed are different steps -- each step is a folder in the repository.

1. Input questions manually that we'd like to ask.
2. Module - Using a translation LLM, translate the question(s) to N many languages.
3. Module - Using a JSON generation LLM specific to each language, generate N variations for the question(s) in each language, respectively.
4. Module - Translate results of the JSON generation LLM back to English.
5. Module - For now, create matplotlib graphs for each question in each language (later we'll consolidate the data and create a single graph).


## Demo
The main scripts are `sample.py` and `visualize.py`

### Flags

#### All scripts
-m, --model == select the model you'd like to sample
-d, --destination == the destination language code, ie the one you'd like to poll
-i, --iterations == how many times you'd like to poll the LLM

#### sample.py
-q, --question == question you wish to poll

*experimental*
-s, --source == the source language, ie the language that the question you ask is in. Default is English

#### visualize.py
-t, --type == the type of analysis to view (either averaged or weighted)

### Code
1. `python sample.py -m llama3.2 -d es -i 10`
2. `python visualize.py -m mistral -d es -i 10 -t weighted`
