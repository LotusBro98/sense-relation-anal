import json
import tkinter as tk
from tkinter import filedialog
import re

import numpy as np

import model.model as model

RELATION_THRESHOLD = 0.5

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

with open(file_path, "rt", encoding='utf-8') as f:
    text = f.read()

delimiters = ['\n', ' ', ',', '.', '?', '!', ':']
words = [text]
for delimiter in delimiters:
    new_words = []
    for word in words:
        new_words += word.split(delimiter)
    words = new_words
words = [word.lower() for word in words]

senses = model.get_sense(words)

counters = {
    "total": 0,
    "related": 0
}

weighted = {
    "vision": 0,
    "sound": 0,
    "skin": 0,
    "taste": 0,
    "smell": 0
}

for word, sense in zip(words, senses):
    sense_dict = dict(zip(model.SENSE_VALUES_DESC, sense))

    counters["total"] += 1

    if sense_dict["relation"] < 0.5:
        continue

    counters["related"] += 1
    for key in weighted:
        weighted[key] += sense_dict[key]

    print("{}: {}".format(word, dict([(k, round(v, 3)) for k, v in sense_dict.items()])))

for key in weighted:
    weighted[key] /= counters["related"]

print(counters)
print(dict([(k, round(v, 3)) for k, v in weighted.items()]))

input()