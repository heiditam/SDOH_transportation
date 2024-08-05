import spacy, re, nltk
import pandas as pd
from collections import Counter
from scipy import stats
from scipy.stats import pearsonr
from textblob import TextBlob

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

# keywords used to identify the sentiment of the article
positive_keywords = [
    "happy", "joy", "satisfied", "content", "positive", "good", "great", "excellent", 
    "fortunate", "successful", "prosperous", "benefit", "advantage", "healthy", 
    "well", "safe", "secure", "comfortable", "enjoy", "fortunate"
]

negative_keywords = [
    "sad", "unhappy", "dissatisfied", "discontent", "negative", "bad", "poor", 
    "terrible", "unfortunate", "unsuccessful", "struggling", "disadvantage", 
    "harm", "sick", "ill", "unsafe", "insecure", "uncomfortable", "suffer", 
    "unlucky"
]

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
    stripped_words = [[word.strip() for word in line.split() if len(word) > 0] for line in lines]
    for lst in stripped_words:
        if len(lst) > 0:
            no_blanks.append(lst)

# count word frequencies
article_text = ' '.join([' '.join([word_only(word).lower() for word in lst if type(word_only(word)) != list]) for lst in no_blanks])

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
corr1, p1 = pearsonr(freq_table['Health'], freq_table['SES']) # corr = 0.814, p = 4.012 * 10^-5
corr2, p2 = pearsonr(freq_table['SDOH'], freq_table['Health']) # corr = 0.892, p = 6.468 * 10^-7
corr3, p3 = pearsonr(freq_table['Health'], freq_table['Privilege']) # corr = 0.919, p = 7.182 * 10^-8

# determine whether there is a positive or negative correlation relationship between the presence of SES words + pos/neg words
def count_keywords(words, keyword_list):
    return [word in keyword_list for word in words]
ses = sum(count_keywords(article_text.split(), ses_words)) #389
pos = sum(count_keywords(article_text.split(), positive_keywords)) #17
neg = sum(count_keywords(article_text.split(), negative_keywords)) #3
# print(ses, pos, neg)

# article text as full sentences
sentiment_polarity = []
ses_polarity = []
full_text = TextBlob(' '.join([' '.join([word for word in lst]) for lst in no_blanks]))
for sentence in full_text.sentences:
    sentiment_polarity.append(sentence.sentiment.polarity)
    words = sentence.words
    if any(word.lower() in ses_words for word in words):
        ses_polarity.append(sentence.sentiment.polarity)

# see if there is a positive or negative sentiment for sentences that contain SES words
# take the average
overall_sentiment = sum(sentiment_polarity) / len(sentiment_polarity)

if ses_polarity:
    ses_sentiment = sum(ses_polarity) / len(ses_polarity)
else:
    ses_sentiment = 0
 
 # overall sentiment: 0.0207
 # sentiment with SES-related words: 0.026

'''2-sample t-test to see if there is a significant difference between the overall sentiment of ALL words in the text 
and those containing SES related words'''
# H0: Sentiment between all sentences and sentences that contain SES words are similar
# H1: Sentences that contain SES-related words have a sentiment that is significantly less than the overall sentiment of the passage. 
t, p = stats.ttest_ind(ses_polarity, sentiment_polarity, alternative='less')
alpha = 0.05 # significance level
if p < alpha:
    print(f'Since {p} < 0.05, we reject H0. Sentences that contains SES-related words do have a sentiment that is\
    significantly less than the overall sentiment of the passage.')
else:
    print(f'Since {p} > 0.05, we fail to reject H0. Sentences that contain SES-related words do not have a significantly different\
    sentiment compared to the overall passage. ')
    # This is what ended up happening; t = -0.271 and p = 0.393