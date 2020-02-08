import json
import tkinter as tk
from tkinter import filedialog
import re

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

with open("sense_words.json", "rt", encoding='utf-8') as f:
    dictionary = json.load(f)

counters = {
    "total": 0,
    "unknown": 0,
    "unrelated": 0,
    "related": 0
}

weighted = {
    "vision": 0,
    "sound": 0,
    "skin": 0,
    "taste": 0,
    "smell": 0
}

endings = ["ой", "ий", "ый", "ого", "его", "ому", "ему", "им", "ым", "ом", "ем", "ая", "яя", "ей", "ую", "юю", "ое", "ее", "ие", "ые", "их", "ых", "им", "ым", "ие", "ые", "ими", "ыми", "их", "ых"]
good_endings = ["ой", "ий", "ый"]

for word in words:
    word = word.lower()

    unified = word + " "
    for ending in endings:
        unified = unified.replace(ending+" ", "* ")
    forms = [word]
    for ending in good_endings:
        if "* " in unified:
            forms.append(unified.replace("* ", ending+" ")[:-1])

    # print(forms)

    counters["total"] += 1
    found = False
    for form in forms:
        if form not in dictionary:
            continue

        found = True

        data = dictionary[form]
        if "vision" not in data:
            counters["unrelated"] += 1
            break

        counters["related"] += 1
        for sense in ["vision", "sound", "skin", "taste", "smell"]:
            weighted[sense] += data[sense]
        print(form, data)
        break

    if not found:
        counters["unknown"] += 1

for sense in weighted:
    weighted[sense] /= counters["related"]

print(counters)
print(weighted)