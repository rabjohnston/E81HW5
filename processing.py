from nltk.stem.porter import *
import nltk
import string

class Processing:
    """
    http://www.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html
    """
    def stem_tokens(tokens, stemmer=PorterStemmer()):
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed


    def get_tokens(text):
        """
        Remove the punctuation using the character deletion step of translate

        text: lowercase text
        :return: list of tokens
        """
        no_punctuation = text.translate(None, string.punctuation)
        tokens = nltk.word_tokenize(no_punctuation)
        return tokens

    def lemmatize_tokens(tokens, lemmatizer=nltk.WordNetLemmatizer()):
        return lemmatizer.lemmatize(tokens)