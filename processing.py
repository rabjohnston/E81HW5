from nltk.stem.porter import *
import nltk
#from nltk import TfidfVectorizer
from nltk.corpus import stopwords
from pandas import Series
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

    def df_to_string(s):
        return s.str.cat(sep=' ')


    def remove_stopwords(tokens):
        all_stopwords = stopwords.words('english')  # Add your own stopwords = + ['s','t']
        tokens = [word for word in tokens if word not in all_stopwords]

        return tokens

    def lemmatize_tokens(tokens, lemmatizer=nltk.WordNetLemmatizer()):
        return lemmatizer.lemmatize(tokens)

    def remove_punctuation(text):
        # Create a dictionary using a comprehension - this maps every character from
        # string.punctuation to None. Initialize a translation object from it.
        translator = str.maketrans({key: None for key in string.punctuation})

        # Remove the punctuation using the translator
        return text.translate(translator)

    def pipeline(text, translators):

        transformed_text = text
        for translator in translators:
            transformed_text = translator(transformed_text)

        return transformed_text

    def get_tokens(text, text_translators=None, token_translators=None):
        """
        Remove the punctuation using the character deletion step of translate

        text: lowercase text
        :return: list of tokens
        """

        # If we were given a Series then convert it to a string
        if type(text) is Series:
            text = text.str.cat(sep=' ')

        if text_translators is not None:
            text = Processing.pipeline(text, text_translators)

        tokens = nltk.word_tokenize(text)

        if token_translators is not None:
            tokens = Processing.pipeline(tokens, token_translators)
        return tokens

    def get_tokens2(text):
        #TfidfVectorizer - Convert a collection of raw documents to a matrix of TF-IDF features.

        all_stopwords = stopwords.words('english')  # Add your own stopwords = + ['s','t']

        vectorizer = TfidfVectorizer(tokenizer = tokenizer_porter,
                                     stop_words=all_stopwords,
                                     use_idf=False,
                                     max_features = 100,ngram_range=(1,1))
        train_data_features = vectorizer.fit_transform(text)
        train_data_features = train_data_features.A #toarray()
        vocab = vectorizer.get_feature_names()