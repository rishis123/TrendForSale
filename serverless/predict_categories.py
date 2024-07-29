import json
import os

import pandas as  pd
import spacy

import seaborn as sns
import string

from tqdm import tqdm
from textblob import TextBlob

from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
import re
import matplotlib.pyplot as plt


    
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, FunctionTransformer
from sklearn.feature_extraction import DictVectorizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
import swifter

"""
https://soumilshah1995.blogspot.com/2021/04/simple-machine-learning-model-to.html.

Include other components. Make the initial training JSON with all mentioned categories.
"""
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


#This is the JSON file containing a list of stories in each category -- see details here: https://www.kaggle.com/datasets/rmisra/news-category-dataset?resource=download
df = pd.read_json("./News_Category_Dataset_v3.json", lines=True)

# Graph categories
# df['category'].value_counts().plot( kind='bar', figsize=(15,10))
# plt.show() #All categories are well-represented in the articles as expected

# Used this snippets of code from 
# https://github.com/ArmandDS/news_category/blob/master/News_Analysis_AO.ipynb

#Cleans up news-stories by removing below stopwords, punctuation, and other filler characters.


stop_words_ = set(stopwords.words('english'))
wn = WordNetLemmatizer()
my_sw = ['make', 'amp',  'news','new' ,'time', 'u','s', 'photos',  'get', 'say']

def black_txt(token):
    return  token not in stop_words_ and token not in list(string.punctuation)  and len(token)>2 and token not in my_sw
  
def clean_txt(text):
    clean_text = []
    clean_text2 = []
    text = re.sub("'", "",text)
    text=re.sub("(\\d|\\W)+"," ",text)    
    clean_text = [ wn.lemmatize(word, pos="v") for word in word_tokenize(text.lower()) if black_txt(word)]
    clean_text2 = [word for word in clean_text if black_txt(word)]
    return " ".join(clean_text2)

#TextBlob library -- https://textblob.readthedocs.io/en/dev/ for NLP purposes
#0 is objective, 1 is subjective. 
def subj_txt(text):
    return  TextBlob(text).sentiment[1]
def polarity_txt(text):
    return TextBlob(text).sentiment[0]

#Check of lexical diveristy (unique words / total words)
def len_text(text):
    if len(text.split())>0:
         return len(set(clean_txt(text).split()))/ len(text.split())
    else:
         return 0

#Making a new column in our dataframe df for just the headline and short_description
df['text'] = df['headline']  +  " " + df['short_description']

#swifter package effectively just a map function for dfs. We apply above functions
df['text'] = df['text'].swifter.apply(clean_txt)
df['polarity'] = df['text'].swifter.apply(polarity_txt)
df['subjectivity'] = df['text'].swifter.apply(subj_txt)
df['len'] = df['text'].swifter.apply(lambda x: len(x))



