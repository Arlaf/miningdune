# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 18:13:47 2018

@author: Arnaud
"""

import nltk
import numpy as np
import pandas as pd

with open("D:\Dropbox\M2\Text Mining\Projet\Dune.txt", "r") as f:
    raw = f.read().strip()

stopwords = set(nltk.corpus.stopwords.words('english'))

tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
corpus = tokenizer.tokenize(raw)
#corpus = [t.lower() for t in corpus if t not in stopwords]

#ps = nltk.stem.PorterStemmer()
#stemmed = [ps.stem(t) for t in corpus]

#dico = list(set(corpus))
#dico.sort()



#from sklearn.feature_extraction.text import CountVectorizer

#count_vect = CountVectorizer()
#TermCountsDoc = count_vect.fit_transform(corpus)
#Terms = np.array(count_vect.vocabulary_.keys())




#N = len(corpus)
#D = [''] * N
#
## Taille de la fenetre
#f = 2
#
## Ajout de mots NULL au début et à la fin du corpus
#corpus = (['<<NULL>>'] * f) + corpus + (['<<NULL>>'] * f)
#    
#for i in range(0, N-2*f):
#    D[i] = [corpus[i+f]] + corpus[(i):(i+f)] + corpus[(i+f+1):(i+2*f+1)]



corpus = ['aaf',
          'ezrh',
          'paul',
          '<seg',
          'egeg',
          'zeg',
          'jean',
          'zeg',
          'paul',
          'zhgz',
          'zegz']
names = ['jean','paul']
max_gap = 3
i = 6
j = 8

def get_key(name1, name2):
    l = [name1, name2]
    l.sort()
    key = l[0] + '_' + l[1]
    return key

def find_cooc(names, corpus, max_gap = 8):
    
    corpus = pd.DataFrame(corpus)
    # Occurrences de tous les noms
    df = corpus.loc[corpus.iloc[:,0].isin(names)]
    
    # Initialisation du dictionnaire des cooccurrences
    cooc = {}
    
    
    for name in names:
        # Occurences du nom en cours
        df_name = df.loc[df.iloc[:,0] == name]
        # On retire le nom en cours de df
        df = df.loc[df.iloc[:,0] != name]
        # si ce n'est pas le dernier nom
        if len(df) > 0:
            # Pour toutes les occurrences du nom en cours
            for i in df_name.index:
                # Toutes les occurrences des autres noms dans le voisinage
                temp = df.loc[(df.index >= i-max_gap) & (df.index <= i+max_gap)]
                # Pour tous les couples nom_en_cours / autre_nom_dans_le_voisinage
                for j in temp.index:
                    # Récupération de l'autre nom
                    name2 = temp.loc[temp.index == j].iloc[0,0]
                    key = get_key(name, name2)
                    # récupération du contexte
                    ind = round((i+j)/2)
                    context =  corpus.iloc[max((ind - max_gap), 0):min((ind + max_gap+1), len(corpus)),0].values.tolist()
                    context.remove(name)
                    context.remove(name2)
                    # Si la clé n'existe pas dans cooc on la crée
                    if key not in cooc:
                        cooc[key] = [context]
                    else:
                        cooc[key].append(context)
    return cooc
    
    
    # Pour tous les tokens i du corpus
    for i in range(0, len(corpus)):
        # Si le token i est un dans la liste des noms fournie
        if corpus.iloc[i, 0] in names:
            # Identification de l'entité
            name = corpus.iloc[i, 0]
            others = names[:]
            others.remove(name)
            # Construction du voisinage
            # index des tokens précédents
            inf = list(range(max(0, i - max_gap), i))
            # index des tokens suivants
            sup = list(range((i+1), min(len(corpus), i+max_gap)))
            neighborhood = inf + sup
            # 
            neighbors = pd.DataFrame(data=None, columns=corpus.columns)
            # Pour tous les mots du voisinage
            for j in neighborhood:
                # le token est-il un nom ?
                if corpus.iloc[j,0] in others:
                    neighbors.append(corpus.iloc[j, ])
            # S'il y a un voisin dans le voisinage
            if len(neighbors > 0):
                
                
                    
                
                        
    return D

