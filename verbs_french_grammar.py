import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
import pandas as pd
import re
import spacy
nlp = spacy.load('en_core_web_sm')

# Lire le fichier texte 

with open('link_to_your_directory', 'r') as file:
    text = file.read()
doc = nlp(text)

# la partie initialisation 
verbs = []
infinitives = []
regularity = []
tenses = []
subjects = []
last_subj = None

# decomposer les phrases en mots et definir les verbes et leurs sujets 
#(si un verbe n'a pas de sujet il prend le sujet du verb précedent) et les mettre dans [subjects]

for token in doc:
    if token.pos_ == 'VERB' or token.lemma_ == 'be':
        subj = None
        for child in token.children:
            if child.dep_ == 'nsubj':
                subj = child.text
        if subj is None and last_subj is not None:
            subjects.append(last_subj)
        else:
            subjects.append(subj)
            last_subj = subj

# definir si le verbe est : regulier / irregulier dans la colomn [regularity]

        verbs.append(token.text)
        lemma = token.lemma_
        infinitives.append(lemma)
        if re.search(r'\b(\w+)(ed|d|ied)$', token.text):
            regularity.append('Regular')
        else:
            regularity.append('Irregular')

# definir le temps du verbe employé dans la case [Tense]

        if token.tag_.startswith('VB'):
          if token.tag_ == 'VB':
            tenses.append('Infinitive')
          elif token.tag_ == 'VBD':
            tenses.append('Past Simple')
          elif token.tag_ == 'VBG':
            tenses.append('Present Participle')
          elif token.tag_ == 'VBN':
            tenses.append('Past Participle')
          elif token.tag_ == 'VBP' or token.tag_ == 'VBZ':
            if token.text.lower() == 'will' or token.text.lower() == 'shall':
              tenses.append('Future Simple')
            else:
              tenses.append('Present Simple')
          elif token.tag_.lower() == 'would':
            tenses.append('Simple Conditional')


# On a ajouter le verb (to be) car il n'etait pas definit

          elif token.lemma_ == 'be':
                if token.tag_ == 'VBD':
                    tenses.append('Past Simple')
                elif token.tag_ == 'VBG':
                    tenses.append('Present Participle')
                elif token.tag_ == 'VBN':
                    tenses.append('Past Participle')
                elif token.tag_ == 'VBP' or token.tag_ == 'VBZ':
                    tenses.append('Present Simple')
                else:
                    tenses.append('Unknown')
            
          else:
                tenses.append('Unknown')
        else:
            tenses.append('Unknown')


# la creation de la table qui contient [verb , infinitive , regularity , tense , subject] et la nommer DF

df = pd.DataFrame({'Verb': verbs, 'Infinitive': infinitives, 'Regularity': regularity, 'Tense': tenses, 'Subject': subjects})

# afficher la table : DF

print(df)
