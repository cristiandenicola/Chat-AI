import json
import requests
import nltk
import os
from nltk.corpus import wordnet
import spacy
from difflib import get_close_matches

if not os.path.exists('nltk_data'):
    nltk.download('wordnet')
    # Crea un file di segnalazione per indicare che il download è stato eseguito
    open('nltk_data', 'a').close()

## Funzione usata per caricare il json con all'interno le risposte del chatbot
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

## Funzione usata per salvare le risposte e allenare il modello con esse
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent = 2)

def translate_to_english(text):
    url = f"http://api.mymemory.translated.net/get?q={text}&langpair=it|en"
    response = requests.get(url)
    translation = response.json()["responseData"]["translatedText"]
    return translation

def translate_to_italian(text):
    url = f"http://api.mymemory.translated.net/get?q={text}&langpair=en|it"
    response = requests.get(url)
    translation = response.json()["responseData"]["translatedText"]
    return translation

def generate_synonyms_in_english(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms

def extract_keywords(text):
    nlp = spacy.load("it_core_news_sm")
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct and token.pos_ != 'VERB' and len(token.text) > 1]
    return keywords

## Funzione usata per trovare il match migliore tra la domanda fatta dall'utente e le risposte a disposizone del modello
def find_best_match(user_question: str, questions: list[str], knowledge_base: dict) -> str | None:
    user_question_lower = user_question.lower()

    # Check for direct matches
    for q in questions:
        if user_question_lower == q.lower():
            return q
    
    # Check for synonyms in the knowledge base
    for q in knowledge_base["questions"]:
        if user_question_lower in q["question"].lower() or user_question_lower in q.get("synonyms", []):
            return q["question"]

    matches: list = get_close_matches(user_question, questions, n = 1, cutoff = 0.6)
    return matches[0] if matches else None

## Funzione che restituisce la risposta alla domanda fatta dall'utente
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
