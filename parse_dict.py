import json
import csv

### No relation to sense

with open("no_relation_to_sense.txt", "rt", encoding='utf-8') as f:
    no_relation = {}
    for line in f:
        elems = line.split(" ")
        if len(elems) != 8:
            continue
        words = [elems[0:4], elems[4:8]]
        for word_data in words:
            word = word_data[0]
            votes_yes = int(word_data[2])
            votes_no = int(word_data[1])
            votes_dontknow = int(word_data[3])
            no_relation[word] = {
                "relation": votes_yes / (votes_yes + votes_no),
                "knowledge": (votes_no + votes_yes) / (votes_no + votes_yes + votes_dontknow)
            }

# with open("no_relation_to_sense.json", "wt", encoding='utf-8') as f:
#     json.dump(no_relation, f, indent=2, ensure_ascii=False)


### Yes relation to sense

def convert_div(str):
    spl = str.split("\\")
    return int(spl[0]) / (int(spl[0]) + int(spl[1]))

with open("yes_relation_to_sense.txt", "rt", encoding='utf-8') as f:
    sense_words = {}
    for line in f:
        elems = line.split(" ")
        if len(elems) != 10:
            continue

        word = elems[0]
        votes_yes = int(elems[2])
        votes_no = int(elems[1])
        votes_dontknow = int(elems[3])
        relation_strength = (["слабая", "средняя", "сильная"].index(elems[4]) + 1) / 3
        vision = convert_div(elems[5])
        sound = convert_div(elems[6])
        smell = convert_div(elems[7])
        taste = convert_div(elems[8])
        skin = convert_div(elems[9])

        sense_words[word] = {
            "relation": votes_yes / (votes_yes + votes_no),
            "knowledge": (votes_no + votes_yes) / (votes_no + votes_yes + votes_dontknow),
            "relation_strength": relation_strength,
            "vision": vision,
            "sound": sound,
            "skin": skin,
            "taste": taste,
            "smell": smell
        }

sense_words.update(no_relation)

with open("sense_words.json", "wt", encoding='utf-8') as f:
    json.dump(sense_words, f, indent=2, ensure_ascii=False)

with open("sense_words.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f, delimiter=',')
    word = "Слово"
    vec = list(list(sense_words.values())[0].keys())
    writer.writerow([word] + vec)
    for word, vec in sense_words.items():
        writer.writerow([word] + list(vec.values()))