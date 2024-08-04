import spacy
from collections import Counter
nlp = spacy.load("en_core_web_sm")

no_blanks = []
# defining categories
sdoh_words = [
    "access", "poverty", "education", "employment", "housing", "nutrition", "environment", 
    "equity", "income", "stress", "safety", "transport", "literacy", "insurance", 
    "community", "resources", "disparity", "inequality", "lifestyle", "socioeconomic", 
    "healthcare", "discrimination", "segregation", "neighborhood", "accessibility", 
    "prevention", "opportunity", "advocacy", "wellness", "infrastructure", "support", 
    "inclusion", "participation", "mobility", "stability", "vulnerability", "diversity", 
    "integration", "outreach", "screening", "services", "policy", "networks", "empowerment", 
    "collaboration", "demographics", "risk", "culture", "barriers", "awareness"
]
sdoh_lemma = [word.lemma_ for word in nlp(' '.join(sdoh_words))]

# cleaning the words:
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

# placing the words from the article in a list / string
with open ('article1.txt', 'r') as f:
    lines = f.readlines()
    stripped_words = [[word.strip().lower() for word in line.split() if len(word) > 0] for line in lines]
    for lst in stripped_words:
        if len(lst) > 0:
            no_blanks.append(lst)

# count word frequencies
article_text = nlp(' '.join([' '.join([word_only(word) for word in lst if type(word_only(word)) != list]) for lst in no_blanks]))
lemma_text = [word.lemma_ for word in article_text if word.is_alpha and not word.is_stop]
word_counts = Counter(lemma_text)
sdoh_count = sum([word_counts[key] for key in word_counts if key in sdoh_lemma])
print(sdoh_count)