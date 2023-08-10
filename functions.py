import json
import nltk
import os
from nltk.corpus import wordnet
from difflib import get_close_matches
import requests
import spacy
from nltk.corpus import wordnet
import numpy as np
from keybert import KeyBERT
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

if not os.path.exists('nltk_data'):
    nltk.download('wordnet')
    # Crea un file di segnalazione per indicare che il download è stato eseguito
    open('nltk_data', 'a').close()

# Carica il modello e il tokenizer
model_name = "gpt2"  # Puoi scegliere un modello diverso, ad esempio "gpt2-medium"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def translate_to_eng(text):
    url = f"http://api.mymemory.translated.net/get?q={text}&langpair=it|en"
    response = requests.get(url)
    translation = response.json()["responseData"]["translatedText"]
    return translation

def translate_to_it(text):
    url = f"http://api.mymemory.translated.net/get?q={text}&langpair=en|it"
    response = requests.get(url)
    translation = response.json()["responseData"]["translatedText"]
    return translation

## Funzione usata per caricare il json con all'interno le risposte del chatbot
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

## Funzione usata per salvare le risposte e allenare il modello con esse
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent = 2)

def generate_synonyms(keyword_list):
    synonyms_list = []

    for word in keyword_list:
        synonyms = []
        synsets = wordnet.synsets(word)
        for syn in synsets:
            for lemma in syn.lemmas():
                lemma_name = lemma.name()
                synonyms.append(lemma_name.lower())
                if len(synonyms) >= 3:
                    break
            if len(synonyms) >= 3:
                break
        synonyms_list.append(synonyms)

    return synonyms_list

def extract_keywords_BERT(text, top_n=5, language='en', max_features=1000, min_score=0.1):
    # Crea un'istanza del modello KeyBERT
    model = KeyBERT()
    # Estrai le parole chiave
    keywords = model.extract_keywords(text, keyphrase_ngram_range=(1, 1), top_n=top_n)

    keyword_list = [keyword for keyword, score in keywords]

    return keyword_list

def generate_answer(prompt, max_length=100, temperature = 0.7, top_p = 0.9):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)

    # Genera la risposta utilizzando il modello con temperature e top_k sampling
    output = model.generate(
        input_ids,
        attention_mask=attention_mask,
        max_length=max_length,
        num_return_sequences=1,
        temperature=temperature,
        top_p = top_p
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    response_it = translate_to_it(response)
    return response_it

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
