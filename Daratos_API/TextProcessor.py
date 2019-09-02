import nltk
import pickle
import string
import re
import numpy
from keras.preprocessing import sequence as sqc

class ProcessRaw:
    max_words = 50
    stemmer = None
    tokenizer = None
    stop_words = None

    def __init__(self):
        with open('../Daratos_ML/SentenceNN/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
            
        self.stemmer = nltk.stem.PorterStemmer()
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        

    def full_clean(self, content):
        '''
        Greatly simplifies the input string into its' root meaning.

        Parameters: 
            content (str): File to read from in csv format
    
        Returns: 
            str: Fully cleaned string
        '''

        if not content:
            return [[]]
        content=content.lower()
        content=re.sub(r'\d+', '', content)
        content=content.translate(str.maketrans('','', string.punctuation))
        content=content.strip()
        print(content)
        tokens=nltk.tokenize.word_tokenize(content)
        content=" ".join([self.stemmer.stem(i) for i in tokens if not self.stemmer.stem(i) in self.stop_words])
        encoded_content = self.tokenizer.texts_to_sequences([content])
        encoded_content = sqc.pad_sequences(encoded_content, maxlen=self.max_words)
        content_train = numpy.array(encoded_content)
        print(content_train)
        return content_train