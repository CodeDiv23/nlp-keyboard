import numpy as np
import re
from nltk.tokenize import RegexpTokenizer
from keras.models import  load_model


# path = './Memoirs of a Geisha by Arthur Golden.txt'
path = './novel_medium.txt'
text = open(path,encoding="utf-8").read().lower()
print('length of the corpus is: :', len(text))

tokenizer = RegexpTokenizer(r'\w+')
text = str(text).lower()
text = text.replace('{html}',"") 
text = re.sub(r'<.*?>', '', text)
text = re.sub(r'http\S+', '', text)
text = re.sub('[0-9]+', '', text)
words = tokenizer.tokenize(text)

unique_words = np.unique(words)
unique_word_index = dict((c, i) for i, c in enumerate(unique_words))

model = load_model('./LSTM_prediction.h5')
# history = pickle.load(open("/content/drive/MyDrive/epoch_run_3.p", "rb"))

def prepare_input(text):
    SEQUENCE_LENGTH = len(tokenizer.tokenize(text)) 
    x = np.zeros((len(text), SEQUENCE_LENGTH, len(unique_words)))
    for t, char in enumerate(tokenizer.tokenize(text)):
        x[0, t, unique_word_index[char]] = 1
    return x

def top_n(preds, n=3):
    preds = preds[0]
    preds = preds.tolist()
    preds = [(p,i) for i,p in enumerate(preds)]

    preds.sort(reverse = True)
    preds = preds[0:n]
    
    my_list = []

    for i in preds:
        my_list.append(unique_words[i[1]])        
    return my_list
        
def predict_next(text):
  x = prepare_input(text)
  preds = model.predict(x)
  return top_n(preds, 3)
  
def predict(text):  
    articles = ['the', 'a', 'an']                                       # will be used when size of sentence < 3 words
    text = text.lower().split(' ')
    if (len(text) < 3): 
        text = articles[:(3-len(text))] + text 

    return tuple(predict_next(' '.join(text[-3:])))
    
    
print(predict("there"))