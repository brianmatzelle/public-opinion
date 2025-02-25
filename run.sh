#!/bin/bash

python sample.py -m llama3.2 -s en -d es -i 10 -q "Historically, what civilations have been the most dominant and influencial of all time?"

python visualize.py -p data/llama3.2/es_10/results.json