from google_play_scraper import Sort, reviews_all
import pandas as pd
import nltk
from nltk.corpus import stopwords
from googletrans import Translator
from nltk.probability import FreqDist as fd

stoplist = set(stopwords.words("indonesian"))
translator = Translator()

def translate_indo(text):
    try:
        translated = translator.translate(text, src='en', dest='id')
        return translated.text
    except:
        return text
    
def remove_stopwords(text, stoplist):
    return " ".join([word for word in text.split() if word.lower() not in stoplist])

def fetch_and_save_reviews(star_rating, filename):
    reviews_id = reviews_all(
        'com.indomaret.klikindomaret',
        lang='id',
        country='id',
        sort=Sort.MOST_RELEVANT,
        filter_score_with=star_rating,
        count=100
    )

    reviews_en = reviews_all(
        'com.indomaret.klikindomaret',
        lang='en',
        country='id',
        sort=Sort.MOST_RELEVANT,
        filter_score_with=star_rating,
        count=100
    )

    all_reviews = reviews_id + reviews_en
    for review in all_reviews:
        if review['content']:
            if review['content'] == 'en' and review['replyContent'] == 'en':
                review['content'] = translate_indo(review['content'])
            if 'replyContent' in review and review['replyContent']:
                review['replyContent'] = translate_indo(review['replyContent'])

    df = pd.DataFrame(all_reviews).dropna()
    df.to_csv(filename, index=False)
    print(df.head())

def review_4_star():
    fetch_and_save_reviews(4, 'reviews_4_star.csv')
def review_5_star():
    fetch_and_save_reviews(5, 'reviews_5_star.csv')
review_4_star()
review_5_star()

