import requests
import spacy
from nltk.corpus import wordnet
import numpy as np

def translate_to_english(text_list):
    translated_list = []

    for word in text_list:
        url = f"http://api.mymemory.translated.net/get?q={word}&langpair=it|en"
        response = requests.get(url)
        translation = response.json()["responseData"]["translatedText"]
        translated_list.append(translation)

    return translated_list

def translate_to_italian(text):
    url = f"http://api.mymemory.translated.net/get?q={text}&langpair=en|it"
    response = requests.get(url)
    translation = response.json()["responseData"]["translatedText"]
    return translation

def generate_synonyms_in_english(word_list):
    synonyms_list = []

    for word in word_list:
        synonyms = []
        synsets = wordnet.synsets(word)
        for syn in synsets:
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
                if len(synonyms) >= 3:
                    break
            if len(synonyms) >= 3:
                break
        synonyms_list.append(synonyms)

    return synonyms_list

def extract_keywords(text):
    nlp = spacy.load("it_core_news_sm")
    doc = nlp(text)
    keywords = [token.text for token in doc if not token.is_stop and not token.is_punct and token.pos_ != 'VERB' and len(token.text) > 1]
    return keywords

def extract_keywords2(text):
    nlp = spacy.load("it_core_news_sm")
    doc = nlp(text)
    keywords = []

    for token in doc:
        if not token.is_stop and not token.is_punct and len(token.text) > 1:
            if token.pos_ not in ['VERB', 'ADJ', 'ADV', 'CONJ', 'PRON', 'DET']:
                keywords.append(token.lemma_)

    return keywords

if __name__ == '__main__':
    input = input()
    #estrazione keywords
    keywords = extract_keywords(input)
    keywords2 = extract_keywords2(input)
    #traduzione keywords
    keywords_eng = translate_to_english(keywords)
    print(keywords_eng)

    keywords_eng2 = translate_to_english(keywords2)
    print(keywords_eng2)

    #ricerca sinonimi keyws in eng
    syn_eng = generate_synonyms_in_english(keywords_eng)
    print(syn_eng)
    #traduzione sin eng in ita
    #salvataggio
