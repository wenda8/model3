import pymorphy2
import nltk
import re



# text = '''text'''


def clean_word(text):
    morph = pymorphy2.MorphAnalyzer()
    only_alpha = nltk.tokenize.RegexpTokenizer('[а-яА-ЯЁё]+')
    words_token = only_alpha.tokenize(text)
    new_words = []

    # # make every alpha small
    # small_words = only_alpha.tokenize(text.lower())
    
    # # delete stop words
    # stop_words = set(nltk.corpus.stop_words.words('russian'))
    # without_stop_words = [(morph.parse(w)[0]).normal_form for w in only_alpha if w not in stop_words and len(w) > 1 ]
    # return without_stop_words

    for w in words_token:
        normal_form = morph.parse(w)[0].normal_form
        new_words.append(normal_form)
        
    return new_words




# print(set(clean_word(text)))