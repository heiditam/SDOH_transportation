import spacy

no_blanks = []
sdoh_keywords = {
    'income', 'education', 'employment', 'housing', 'environment', 
    'healthcare', 'nutrition', 'poverty', 'inequality', 'disparities', 
    'social', 'determinants', 'access', 'community', 'neighborhood',
    'stress', 'transportation', 'racism', 'discrimination', 'violence',
    'safety', 'support', 'resources', 'services', 'insurance', 
    'policy', 'legislation', 'economy', 'workplace', 'sanitation',
    'infrastructure', 'water', 'air', 'food', 'mental health', 
    'wellbeing', 'lifestyle', 'behavior', 'education level', 'income level', 
    'socioeconomic', 'status', 'health', 'equity', 'marginalization', 'vulnerability', 
    'health', 'literacy', 'employment', 'family', 'support', 'childcare', 'public health'
}

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

with open ('article1.txt', 'r') as f:
    lines = f.readlines()
    stripped_words = [[word.strip().lower() for word in line.split() if len(word) > 0] for line in lines]
    for lst in stripped_words:
        if len(lst) > 0:
            no_blanks.append(lst)

nlp = spacy.load("en_core_web_sm")
article_text = ' '.join([' '.join([word_only(word) for word in lst if type(word_only(word)) != list]) for lst in no_blanks])

print(article_text)