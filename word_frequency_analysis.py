import xml.etree.ElementTree as ET
import spacy
from spacy.cli import download

tree = ET.parse('sources.xml')
root = tree.getroot()

abstracts = ''
word_counts = {}

# word frequency analysis
for abstract_elem in root.findall('.//abstract'):
    abstracts += abstract_elem.text.lower()

abstracts = abstracts.strip().split()

def word_only(word):
    while len(word) > 0 and not word[0].isalnum():
        word = word[1:]
    while len(word) > 0 and not word[-1].isalnum():
        word = word[:-1]
        
    if word.__contains__('/'):
        word = word.split('/')

    if word.__contains__('.'):
        word = word.split('.')
        
    return word

cleaned_words = [word_only(word) for word in abstracts if type(word_only(word)) != list]
mult_topics = [item for sublist in cleaned_words for item in sublist if len(item) > 1]
all_words = cleaned_words + mult_topics

for word in all_words:
    if word not in word_counts:
        word_counts[word] = 1
    else:
        word_counts[word] += 1

# sort by the second element (the value) in descending order, and then sort by the key alphabetically
# print(sorted(word_counts.items(), key=lambda x: (-x[1], x[0])))

# download("en_core_web_sm")
nlp = spacy.load("en_core_web_sm")
string_text = nlp(' '.join(word_counts.keys()))

for token in string_text:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)