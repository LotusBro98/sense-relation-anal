import json

import gensim
import numpy as np
from gensim.models import KeyedVectors
import os
import numpy
import tensorflow as tf

MODEL_URL = "http://vectors.nlpl.eu/repository/20/180.zip"
emb_path = os.path.join(os.path.dirname(__file__), "model.bin")
ru_emb = KeyedVectors.load_word2vec_format(emb_path, binary=True)

tag_list = [
    'ADJ',
    'VERB',
    'NOUN',
    'ADV',
    'PRON',
    'PART',
    'NUM',
    'DET',
    'SCONJ',
    'INTJ',
    'ADP',
]

VEC_SIZE = 300
SENSE_VEC_SIZE = 8

SENSE_VALUES_DESC = [
    "relation",
    "knowledge",
    "relation_strength",
    "vision",
    "sound",
    "skin",
    "taste",
    "smell"
]

unknown_vec = np.zeros((VEC_SIZE,))

def get_emb(word):
    global unk
    global know

    for tag in tag_list:
        word_test = word + "_" + tag
        if word_test in ru_emb:
            return ru_emb[word_test]
    # print("Unknown word: {}".format(word))
    return unknown_vec

def SenseModel():
    inputs = tf.keras.layers.Input((VEC_SIZE,))
    x = inputs

    x = tf.keras.layers.Dense(8, activation='sigmoid')(x)

    return tf.keras.Model(inputs=inputs, outputs=x)

def vec_from_entry(word_data):
    word_data = list(word_data)
    if len(word_data) < SENSE_VEC_SIZE:
        word_data += [0] * (SENSE_VEC_SIZE - len(word_data))

    return word_data

def train():
    with open("../sense_words.json", "rt", encoding='utf-8') as f:
        sense_words = json.load(f)

    embeddings = np.array([get_emb(word) for word in sense_words.keys()], dtype=np.float32)
    sense_vectors = np.array([vec_from_entry(vec.values()) for vec in sense_words.values()], dtype=np.float32)

    model = SenseModel()

    model.compile(loss='mae', optimizer='adam')

    model.fit(embeddings, sense_vectors, epochs=20)

    model.save("model.h5")

try:
    model_path = os.path.join(os.path.dirname(__file__), "model.h5")
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    print("No pretrained model found")
    print("Please download from {}".format(MODEL_URL))
    print("Adn put model.bin to model/ folder")

def get_sense(words):
    emb = [get_emb(word) for word in words]
    sense = model.predict(np.array(emb))

    return sense

def test():
    global model

    with open("../samples/perfum.txt", "rt", encoding='utf-8') as f:
        text = f.read()

    model = tf.keras.models.load_model("model.h5")
    words = text.split(" ")

    senses = get_sense(words)

    for word, sense in zip(words, senses):
        sense_dict = dict(zip(SENSE_VALUES_DESC, sense))
        if sense_dict["relation"] < 0.5:
            continue
        print("{}: {}".format(word, sense_dict))

if __name__ == '__main__':

    train()
    test()

