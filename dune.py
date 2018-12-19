# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 18:13:47 2018

@author: Arnaud
"""

import nltk
import pandas as pd

with open("D:\Repo_git\miningdune\Dune.txt", "r") as f:
    raw = f.read().strip()

stopwords = set(nltk.corpus.stopwords.words('english'))

tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
corpus = tokenizer.tokenize(raw)
corpus = [t.lower() for t in corpus if t not in stopwords]

pd_gaz = pd.read_csv("D:\Repo_git\miningdune\gazetier.csv", sep = ',')

# Construction du gazetier
gaz = {}
for i in range(len(pd_gaz)):
    j = 1
    while j < len(pd_gaz.columns):
        key = pd_gaz.iloc[i,j]
        if not isinstance(key, str):
            break
        gaz[key] = pd_gaz.iloc[i,0]
        j = j+1

keys = list(gaz.keys())

# Transformation des noms du corpus
i = 0
while i < len(corpus):
    if i < len(corpus)-1:
        test = corpus[i] + ' ' + corpus[i+1]
        if test in keys:
            corpus[i] = gaz[test]
            corpus.pop(i+1)
        elif corpus[i] in keys:
            corpus[i] = gaz[corpus[i]]
    elif corpus[i] in keys:
        corpus[i] = gaz[corpus[i]]
    i = i+1

def get_key(name1, name2):
    l = [name1, name2]
    l.sort()
    key = l[0] + '&' + l[1]
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
                        cooc[key] = {'names' : [name, name2],
                                     'context' : [context]}
                    else:
                        cooc[key]['context'].append(context)
    return cooc

names = pd_gaz.id.tolist()

cooc = find_cooc(names, corpus, 10)

# Importation du lexique
lexicon = pd.read_csv("D:\Repo_git\miningdune\lexicon.txt", sep="\t", header=None)
lexicon.columns = ["word", "emotion", "value"]
lexicon = lexicon.loc[~lexicon.emotion.isin(['anticipation', 'surprise']),]
lexicon['word'] = lexicon['word'].astype(str)
lexicon['word'].astype(str)

# Liste des différentes émotions
emotions = lexicon.emotion.unique().tolist()

# Liste de tous les couples de personnage observés
pairs = list(cooc.keys())

# Initialisation d'un df des emotions caractérisants un couple de personnages
d = {'pair' : sum(([p]*len(emotions) for p in pairs),[]),
     'cooc' : [0] * len(pairs) * len(emotions),
     'emotion' : emotions * len(pairs),
     'value' : [0] * len(pairs) * len(emotions)}
emo = pd.DataFrame(d)


for pair in pairs:
    print(pair)
    # Nombre de cooccurrences de cette paire
    emo.loc[emo.pair == pair, 'cooc'] = len(cooc[pair]['context']) 
    # 
    context = [item for sublist in cooc[pair]['context'] for item in sublist]
    for token in context:
        if len(lexicon.loc[lexicon.word == token,:]) > 0:
            for emotion in emotions:
                emo.loc[(emo.pair == pair) & (emo.emotion == emotion), 'value'] = emo.loc[(emo.pair == pair) & (emo.emotion == emotion), 'value'].values + lexicon.loc[(lexicon.word == token) & (lexicon.emotion == emotion), 'value'].values
                
emo.to_csv('C:\\Users\\arnau\\Desktop\\emo.txt', sep='\t', encoding='utf-8')

#d = {'names' : names}
#df = pd.DataFrame(d)
#df.to_csv('C:\\Users\\arnau\\Desktop\\names.txt', sep='\t', encoding='utf-8')