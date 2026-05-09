import nltk
from nltk.stem import LancasterStemmer
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
import random
import json
import pickle
from flask import Flask, render_template, request, jsonify

# Initialize Flask and NLP tools
app = Flask(__name__)
stemmer = LancasterStemmer()

# --- STEP 1: MOCK DATA (In a real app, load from intents.json) ---
intents = {
    "intents": [
        {"tag": "greeting", "patterns": ["Hi", "Hello", "Hey"], "responses": ["Hello! How are you feeling today?", "Hi there, I'm here to listen."]},
        {"tag": "anxious", "patterns": ["I feel anxious", "I am stressed", "I'm overwhelmed"], "responses": ["Take a deep breath. You're not alone.", "It's okay to feel this way. Let's talk about it."]},
        {"tag": "goodbye", "patterns": ["Bye", "See you later", "Goodbye"], "responses": ["Goodbye! Take care of yourself.", "I'm always here if you need to talk again."]}
    ]
}

# --- STEP 2: PREPROCESSING & MODEL (Simplified for Lab) ---
words = []
classes = []
documents = []
ignore_words = ['?', '!']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = sorted(list(set([stemmer.stem(w.lower()) for w in words if w not in ignore_words])))
classes = sorted(list(set(classes)))

# (Training logic would usually happen in a separate script; 
# here we define the predict function assuming the model exists)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s: bag[i] = 1
    return np.array(bag)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    # In a full app: model.predict() -> get tag -> return random.choice(responses)
    # Humanized fallback for the lab:
    res = "I'm still learning, but I'm listening. Could you tell me more?"
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in msg.lower():
                res = random.choice(intent['responses'])
    return jsonify({"response": res})

if __name__ == "__main__":
    app.run(debug=True)