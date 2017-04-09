import abc
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, \
    classification_report
from sklearn.naive_bayes import MultinomialNB

from server.utils import data_util

NUM_CATEGORIES = 5


def plot_confusion_matrix(Y_test, Y_pred):
    sns.set()
    cmatrix = confusion_matrix(y_true=Y_test, y_pred=Y_pred)
    ax = sns.heatmap(cmatrix, xticklabels=["Food", "Events", "Nature",
                                           "Accommodation", "Attraction"],
                     yticklabels=["Food", "Events", "Nature",
                                  "Accommodation",
                                  "Attraction"], annot=True,
                     square=True, cbar=False)
    sns.plt.yticks(rotation=0)
    sns.plt.show()


class BaseClassifier(metaclass=abc.ABCMeta):

    def __init__(self, *args):
        self.name = None
        self.check_point = "{}_model.pkl"
        self.score_result = "{}_score"
        self.model = None
        self.labels = [1, 2, 3, 4, 5]
        self.num_of_categories = len(self.labels)

    def __repr__(self):
        return self.name

    def init_params(self, name):
        self.name = name
        self.check_point = data_util.get_filepath(self.check_point.format(
            self.name))
        self.score_result = data_util.get_filepath(self.score_result.format(
            self.name))

    @abc.abstractmethod
    def create_model(self, *args):
        """Implement model"""
        return

    def train_model(self, X_train, y_train):
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
            "classification_report": classification_report(true_y, pred_y,
                                                           target_names=target)
        }

        for score in scores:
<<<<<<< HEAD
            print("{}: \n {}".format(score, scores[score]))
=======
            log += "{}:\n {}\n".format(score, scores[score])
>>>>>>> ab989a185e42cd101c2ee7e513eacdb014dcda79

        print(log)
        data_util.write_text_to_txt(log, self.score_result)
        # plot_confusion_matrix(true_y, pred_y)

    def run(self, X_train, X_test, y_train, y_test):
        self.train_model(X_train, y_train)
        pred_y = self.predict(X_test)
        self.compute_score(y_test, pred_y)

    def print_all(self):
        print(self.name)
        print(self.check_point)
        print(self.score_result)


class NBClassifier(BaseClassifier):
    """Multinomial Naive Bayes Classifier"""
    def __init__(self):
        BaseClassifier.__init__(self)
        self.init_params("naive_bayes")
        self.create_model()

    def create_model(self):
        self.model = MultinomialNB()


class RFClassifier(BaseClassifier):
    """Random Forest Classifier"""
    def __init__(self):
        BaseClassifier.__init__(self)
        self.init_params("rf")
        self.create_model()

    def create_model(self):
        self.model = RandomForestClassifier(n_estimators=110, random_state=1)
        return self.model


class LRClassifier(BaseClassifier):
    """Logistic Regression Classifier"""
    def __init__(self):
        BaseClassifier.__init__(self)
        self.init_params("lr")
        self.create_model()

    def create_model(self):
        self.model = LogisticRegression(random_state=1)
        return self.model


class VClassifier(BaseClassifier):
    """Ensemble Voting Classifier"""
    def __init__(self, *args):
        BaseClassifier.__init__(self)
        self.init_params("vc")
        self.create_model(*args)

    def create_model(self, *args):
        arg = list()
        for count, clf in enumerate(args):
            a = (clf.name, clf.model)
            arg.append(a)

        self.model=VotingClassifier(estimators=arg, voting='hard')

        return self.model
