import xml.etree.ElementTree as ET
import spacy
from spacy.cli import download

tree = ET.parse('sources.xml')
root = tree.getroot()

abstracts = ''
word_counts = {}
stemming_dict = {}
verbs = {}
unique_words = 0
verb_count = 0

# word frequency analysis
for abstract_elem in root.findall('.//abstract'):
    abstracts += abstract_elem.text.lower()

# only download the first time
# download("en_core_web_sm")

nlp = spacy.load("en_core_web_sm")

for token in nlp(abstracts):
    if token.is_alpha and not token.is_stop:
        if token.lemma_ not in stemming_dict:
            stemming_dict[token.lemma_] = 1
            unique_words += 1
        else:
            stemming_dict[token.lemma_] += 1

        if token.pos_ == 'VERB':
            if token.lemma_ not in verbs:
                verbs[token.lemma_] = 1
                verb_count += 1
            else:
                verbs[token.lemma_] += 1

sorted_dict = sorted(stemming_dict.items(), key=lambda x: (-x[1], x[0]))
sorted_verbs = sorted(verbs.items(), key=lambda x: (-x[1], x[0]))
print(sorted_dict)