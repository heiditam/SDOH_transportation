import spacy
import re
import pandas as pd
from collections import Counter
from scipy.stats import pearsonr

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

health_words = [
    "wellness", "fitness", "nutrition", "exercise", "diet", "sleep", 
    "hydration", "immunity", "mental", "physical", "cardio", "strength", 
    "flexibility", "stamina", "endurance", "wellbeing", "prevention", 
    "care", "balance", "vitality", "resilience", "recovery", "therapy", 
    "meditation", "yoga", "aerobic", "anaerobic", "mindfulness", "holistic", 
    "detox", "cleanse", "rehabilitation", "healing", "hygiene", "sanitation", 
    "vaccination", "protection", "antioxidant", "protein", "carbohydrate", 
    "vitamin", "mineral", "herbs", "remedy", "treatment", "diagnosis", 
    "symptom", "prevention", "cure"
]
health_lemma = [word.lemma_ for word in nlp(' '.join(health_words))]

# socioeconomic status
ses_words = [ 
    "income", "poverty", "wealth", "equity", "disparity", "access",
    "housing", "healthcare", "nutrition", "employment", "education",
    "insurance", "transportation", "infrastructure", "affordability",
    "hygiene", "disability", "mobility", "diversity", "inclusion",
    "community", "neighborhood", "segregation", "gentrification",
    "economics", "resources", "services", "support", "barriers",
    "inequality", "standards", "living", "conditions", "facilities",
    "safety", "sanitation", "environment", "pollution", "stress",
    "wellbeing", "prevention", "disease", "mortality", "morbidity",
    "accessibility", "outreach", "awareness", "advocacy", "policy"
]
ses_lemma = [word.lemma_ for word in nlp(' '.join(ses_words))]

privilege_words = [
    "access", "equity", "disparity", "income", "healthcare", "insurance", 
    "affordability", "nutrition", "housing", "transportation", "education", 
    "resources", "opportunity", "wellness", "sanitation", "inclusion", 
    "barriers", "mobility", "coverage", "support", "availability", "services", 
    "facilities", "safety", "environment", "employment", "disability", "poverty", 
    "proximity", "outreach", "community", "public", "private", "prevention", 
    "accessibility", "inequality", "justice", "discrimination", "diversity", 
    "stigma", "mental", "physical", "chronic", "acute", "care", "policy", 
    "advocacy", "rights", "wellbeing"
]
privilege_lemma = [word.lemma_ for word in nlp(' '.join(privilege_words))]


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
article_text = ' '.join([' '.join([word_only(word) for word in lst if type(word_only(word)) != list]) for lst in no_blanks])

# divide text into sections by label
def split_by_label(text, labels):
    pattern = '|'.join(re.escape(label) for label in labels)
    sections = re.split(pattern, text)
    return sections

labels = ['Abstract', 'Multifaceted Nature of Transportation Insecurity Among Patients With Cancer',\
          'Prevalence of Transportation Insecurity Among Patients With Cancer', \
            'Consequences of Transportation Insecurity Among Patients With Cancer', \
            'Screening for Transportation Insecurity Among Patients With Cancer', \
            'Efforts to Address Transportation Insecurity for Patients With Cancer', \
            'Policy Agenda for Addressing Transportation Insecurity for Patients With Cancer', \
            'Data Infrastructure Research Agenda to Address Transportation Insecurity for Patients With Cancer']

chunks = split_by_label(article_text, [label.lower() for label in labels])
sdoh_count_list = []
health_count_list = []
ses_count_list = []
privilege_count_list = []

# word frequency for lemmatized words for each section in the text
for chunk in chunks:
    doc = nlp(chunk)
    lemma_text = [word.lemma_ for word in doc if word.is_alpha and not word.is_stop]
    word_counts = Counter(lemma_text)
    sdoh_count = sum([word_counts[key] for key in word_counts if key in sdoh_lemma])
    health_count = sum([word_counts[key] for key in word_counts if key in health_lemma])
    ses_count = sum([word_counts[key] for key in word_counts if key in ses_lemma])
    privilege_count = sum([word_counts[key] for key in word_counts if key in privilege_lemma])
    sdoh_count_list.append(sdoh_count)
    health_count_list.append(health_count)
    ses_count_list.append(ses_count)
    privilege_count_list.append(privilege_count)

data = {
    'SDOH': sdoh_count_list,
    'Health': health_count_list,
    'SES': ses_count_list,
    'Privilege': privilege_count_list
}
freq_table = pd.DataFrame(data)
# corr, p = pearsonr(freq_table['Health'], freq_table['SES']) # corr = 0.814, p = 4.012 * 10^-5
# corr, p = pearsonr(freq_table['SDOH'], freq_table['Health']) # corr = 0.892, p = 6.468 * 10^-7
corr, p = pearsonr(freq_table['Health'], freq_table['Privilege'])

print(corr, p)
