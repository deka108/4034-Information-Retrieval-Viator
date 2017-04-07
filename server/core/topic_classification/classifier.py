from server.utils import data_util
from server.core.topic_classification.classification_preprocessing import DOCUMENT_MAX_NUM_WORDS, \
    NUM_FEATURES
from keras.layers import LSTM, Dropout, Dense, Activation
from keras.models import Sequential
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.externals import joblib
import abc
import json

from sklearn.naive_bayes import MultinomialNB

NUM_CATEGORIES = 5


class BaseClassifier(metaclass=abc.ABCMeta):

    def __init__(self):
        self.name = None
        self.check_point = "{}_model.pkl"
        self.score_result = "{}_score"
        self.model = None
        self.labels = [1, 2, 3, 4, 5]
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

    def init_params(self, name):
        self.name = name
        self.check_point = self.check_point.format(self.name)
        self.score_result = self.score_result.format(self.name)

    @abc.abstractmethod
    def create_model(self, *args):
        """Implement model"""
        return

    def train_model(self, X_train, y_train, X_test, y_test):
        self.model.fit(X_train, y_train)
        joblib.dump(self.model, self.check_point)
        return self.model

    def predict(self, X_test):
        self.model = joblib.load(self.check_point)
        result = self.model.predict(X_test)
        return result

    def compute_score(self, true_y, pred_y):
        log = "====={} results=====\n".format(self.name)
        target = ["Food", "Events", "Nature", "Accommodation", "Attraction"]
        scores = {
            "accuracy": accuracy_score(true_y, pred_y),
            "confusion_matrix": confusion_matrix(true_y, pred_y),
            "classification_report": classification_report(true_y, pred_y, target_names=target)
        }

        for score in scores:
            log += "{}:\n {}\n".format(score, scores[score])

        print(log)
        data_util.write_text_to_txt(log, self.score_result)

    def run(self, X_train, y_train, X_test, y_test):
        self.create_model()
        self.train_model(X_train, y_train, X_test, y_test)
        pred_y = self.predict(X_test)
        self.compute_score(y_test, pred_y)

    def print_all(self):
        print(self.name)
        print(self.check_point)
        print(self.score_result)


class RFClassifier(BaseClassifier):
    def __init__(self):
        BaseClassifier.__init__(self)
        self.init_params("rf")
        self.create_model()

    def create_model(self):
        self.model = RandomForestClassifier(n_estimators=110, random_state=1)
        return self.model


class VClassifier(BaseClassifier):
    def __init__(self):
        BaseClassifier.__init__(self)
        self.init_params("vc")
        self.create_model()

    def create_model(self, *args):
        arg = list()
        for count, clf in enumerate(args):
            a = (clf.name, clf.model)
            arg.append(a)

        self.model=VotingClassifier(estimators=arg, voting='hard')

        return self.model


class LRClassifier(BaseClassifier):
    def __init__(self):
        BaseClassifier.__init__(self)
        self.init_params("lr")
        self.create_model()

    def create_model(self):
        self.model = LogisticRegression(random_state=1)
        return self.model


class NBClassifier(BaseClassifier):
    def __init__(self):
        BaseClassifier.__init__(self)
        self.init_params("naive_bayes")
        self.create_model()

    def create_model(self):
        self.model = MultinomialNB()


class NNClassifier(BaseClassifier):
    def __init__(self):
        BaseClassifier.__init__(self)
        self.init_params("nn")
        self.create_model()

    def create_model(self):
        self.model = Sequential()

        self.model.add(LSTM(int(1433 * 1.5),
                       input_shape=(1433, NUM_FEATURES)))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(NUM_CATEGORIES))
        self.model.add(Activation('sigmoid'))

        self.model.compile(loss='binary_crossentropy', optimizer='adam',
                      metrics=['accuracy'])

    def train_model(self, X_train, y_train, X_test, y_test):
        # Train model
        self.model.fit(X_train, y_train, batch_size=128, nb_epoch=5,
                       validation_data=(X_test, y_test))
        return self.model

    def predict(self, X_test):
        y_pred = self.model.predict(X_test, batch_size=128)
        return y_pred

    def evaluate(self, X_test, y_test):

        # Evaluate model
        score, acc = self.model.evaluate(X_test, y_test, batch_size=128)

        print('Score: %1.4f' % score)
        print('Accuracy: %1.4f' % acc)

