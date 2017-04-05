from sklearn.ensemble import RandomForestClassifier
from server.core.topic_classification import classifier


class RFClassifier(classifier.Classifier):
    def __init__(self):
        classifier.Classifier.__init__(self)
        self.init_params("rf")
        self.create_model()

    def create_model(self):
        self.model = RandomForestClassifier(n_estimators=100)
        return self.model


if __name__ == "__main__":
    classifier = RFClassifier()
    print(classifier.model)