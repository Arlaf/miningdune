# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 19:29:17 2018

@author: Arnaud
"""

import spacy
import string

# Reading Dune.txt
with open("D:\Dropbox\M2\Text Mining\Projet\Dune.txt", "r") as f:
#    raw = fo.read().splitlines() 
    raw = f.read().strip()

# remove multiple spaces
#raw = re.sub(' +',' ',raw)

# formating Saints names
raw = raw.replace("St. ", "St-")
raw = raw.replace(" . . . ", ". ")

# word tokenisation
words = raw.split()

# all the book in one string (previous step removed a lot of unwanted spaces)
book = " ".join(words[1:10000])

# remove punctuation (except end of sentence markers)
exclude = [e for e in set(string.punctuation) if e not in ("!", "?", ".")]
book = ''.join(ch for ch in book if ch not in exclude)

# sentence tokenisation
sentences = book.split(". ")
sentences = [s.split("! ") for s in sentences]
sentences = [item for sublist in sentences for item in sublist]
sentences = [s.split("? ") for s in sentences]
sentences = [item for sublist in sentences for item in sublist]
sentences = [s.strip() for s in sentences if len(s) > 1]

# magic happens now
nlp = spacy.load('en') 
doc = nlp(book[1:10000])

for entity in doc.ents:
    print(entity.text, entity.label_)
    