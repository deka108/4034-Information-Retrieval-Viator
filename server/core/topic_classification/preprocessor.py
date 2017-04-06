import abc

from sklearn.feature_extraction.text import TfidfVectorizer


class BasePreprocessor(metaclass=abc.ABCMeta):
    def __init__(self, name):
        self.name = name
        self.vectorizer = None

    @abc.abstractmethod
    def create_vectorizer(self):
        return

    @abc.abstractmethod
    def preprocess(self):
        return

    @abc.abstractmethod
    def generate_features(self):
        return


class TfIdfPrerocessor(BasePreprocessor):
    def create_vectorizer(self):
        self.vectorizer = TfidfVectorizer()