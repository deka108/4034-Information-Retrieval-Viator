from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from sklearn.externals import joblib
import abc
import json


class Classifier(metaclass=abc.ABCMeta):

    def __init__(self):
        self.name = None
        self.check_point = "{}_model.pkl"
        self.score_result = "{}_score.json"
        self.model = None
        self.labels = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None


    def init_params(self, name):
        self.name = name
        self.check_point = self.check_point.format(self.name)
        self.score_result = self.score_result.format(self.name)

    @abc.abstractmethod
    def create_model(self):
        """Implement model"""
        return

    def train_model(self, X_train, y_train, *args):
        self.model.fit(X_train, y_train)
        joblib.dump(self.model, self.check_point)
        self.labels = y_train.unique()
        return self.model

    def predict(self, X_test):
        self.labels = self.y_train.unique()
        self.model = joblib.load(self.check_point)
        return self.model.predict(X_test)

    def compute_score(self, true_y, pred_y):
        print("====={} results=====".format(self.name))
        scores = {
            "accuracy": accuracy_score(true_y, pred_y),
            "precision": precision_score(true_y, pred_y),
            "recall": recall_score(true_y, pred_y),
            "f1_score": f1_score(true_y, pred_y, self.labels)
        }

        for score in scores:
            print("{}: {}".format(score, scores[score]))

        with open(self.score_result, "w") as fh:
            json.dump(scores, fh)

    def run(self, X_train, y_train, X_test, y_test):
        self.create_model()
        self.train_model(X_train, y_train)
        pred_y = self.predict(X_test)
        self.compute_score(y_test, pred_y)

    def print_all(self):
        print(self.name)
        print(self.check_point)
        print(self.score_result)


