import pandas as pd
import re
import itertools
from nltk.tokenize import WordPunctTokenizer
import csv
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

#Stopword removal and stemming
def stop(text):    
    return (' '.join([word for word in text.split() if word not in (stoplist)]))

def stem(text):
    return stemmer.stem(text)

stoplist = []
with open('data/stopwordbahasa.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        word = ', '.join(line)
        stoplist.append(word)

factory = StemmerFactory()
stemmer = factory.create_stemmer()


# Translate emoticon
emoticon_data_path = 'data/emoticon.txt'
emoticon_df = pd.read_csv(emoticon_data_path, sep='\t', header=None)
emoticon_dict = dict(zip(emoticon_df[0], emoticon_df[1]))

slang_words = pd.read_csv('data/slangword.csv')
slang_dict = dict(zip(slang_words['original'],slang_words['translated']))


def translate_emoticon(t):
    for w, v in emoticon_dict.items():
        pattern = re.compile(re.escape(w))
        match = re.search(pattern,t)
        if match:
            t = re.sub(pattern,v,t)
    return t

def remove_n(text):
    stri = '\\n'
    n = text.replace(stri,' ')
    return n

def remove_newline(text):
    return re.sub('\n', ' ',text)

def remove_kaskus_formatting(text):
    text = re.sub('\[', ' [', text)
    text = re.sub('\]', '] ', text)
    text = re.sub('\[quote[^ ]*\].*?\[\/quote\]', ' ', text)
    text = re.sub('\[[^ ]*\]', ' ', text)
    text = re.sub('&quot;', ' ', text)
    return text

def remove_url(text):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', text)

def remove_excessive_whitespace(text):
    return re.sub('  +', ' ', text)

def tokenize_text(text, punct=False):
    text = WordPunctTokenizer().tokenize(text)
    text = [word for word in text if punct or word.isalnum()]
    text = ' '.join(text)
    text = text.strip()
    return text

def transform_slang_words(text):
    word_list = text.split()
    word_list_len = len(word_list)
    transformed_word_list = []
    i = 0
    while i < word_list_len:
        if (i + 1) < word_list_len:
            two_words = ' '.join(word_list[i:i+2])
            if two_words in slang_dict:
                transformed_word_list.append(slang_dict[two_words])
                i += 2
                continue
        transformed_word_list.append(slang_dict.get(word_list[i], word_list[i]))
        i += 1
    return ' '.join(transformed_word_list)

def remove_non_alphabet(text):
    output = re.sub('[^a-zA-Z ]+', '', text)
    return output

def remove_twitter_ig_formatting(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'\brt\b', '', text)
    return text

def remove_repeating_characters(text):
    return ''.join(''.join(s)[:1] for _, s in itertools.groupby(text))



