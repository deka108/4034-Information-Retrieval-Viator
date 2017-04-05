from server.core.topic_classification import classifier
from sklearn.naive_bayes import MultinomialNB


class NBClassifier(classifier.Classifier):
    def __init__(self):
        classifier.Classifier.__init__(self)
        self.init_params("naive_bayes")
        self.create_model()

    def create_model(self):
        self.model = MultinomialNB()


if __name__ == "__main__":
    classifier = NBClassifier()
    print(classifier.model)