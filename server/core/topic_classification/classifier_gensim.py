from keras.layers import LSTM, Dropout, Dense, Activation
from keras.models import Sequential
from keras.wrappers.scikit_learn import KerasClassifier

from server.core.gensim_models.gensim_model import DOCUMENT_MAX_NUM_WORDS, \
    NUM_FEATURES
from server.core.topic_classification import classification_preprocessing as\
    cp
from server.core.gensim_models import gensim_model
from server.core.topic_classification.classifier import BaseClassifier, \
    NUM_CATEGORIES


class NNClassifier(BaseClassifier):
    def __init__(self):
        BaseClassifier.__init__(self)
        self.init_params("nn")
        self.create_model()

    def create_model(self):
        self.model = KerasClassifier(build_fn=self.build_keras_model(),
                                     batch_size=128, nb_epoch=5)
        return self.model

    def build_keras_model(self):
        model = Sequential()

        model.add(LSTM(DOCUMENT_MAX_NUM_WORDS ,
                   input_shape=(DOCUMENT_MAX_NUM_WORDS, NUM_FEATURES)))
        model.add(Dropout(0.3))
        model.add(Dense(NUM_CATEGORIES))
        model.add(Activation('sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam',
                  metrics=['accuracy'])
        return model


    # def create_keras_model(self):
    #     self.model = Sequential()
    #
    #     self.model.add(LSTM(DOCUMENT_MAX_NUM_WORDS ,
    #                    input_shape=(DOCUMENT_MAX_NUM_WORDS, NUM_FEATURES)))
    #     self.model.add(Dropout(0.3))
    #     self.model.add(Dense(NUM_CATEGORIES))
    #     self.model.add(Activation('sigmoid'))
    #
    #     self.model.compile(loss='binary_crossentropy', optimizer='adam',
    #                   metrics=['accuracy'])
    #
    # def train_model(self, X_train, y_train):
    #     # Train model
    #     self.model.fit(X_train, y_train, batch_size=128, nb_epoch=5)
    #     return self.model
    #
    # def predict(self, X_test):
    #     y_pred = self.model.predict(X_test, batch_size=128)
    #     return y_pred
    #
    # def evaluate(self, X_test, y_test):
    #
    #     # Evaluate model
    #     score, acc = self.model.evaluate(X_test, y_test, batch_size=128)
    #
    #     print('Score: %1.4f' % score)
    #     print('Accuracy: %1.4f' % acc)


def run():
    X, y = gensim_model.generate_features()
    X_train, X_test, y_train, y_test = cp.split_train_test(X, y)
    classifier = NNClassifier()
    classifier.train_model(X_train, y_train)
    classifier.evaluate(X_test, y_test)
    #
    # y_pred = classifier.predict(X_test)
    # print(y_pred)
    # classifier.compute_score(y_test, y_pred)
    # classifier.evaluate(X_test, y_test)

if __name__ == "__main__":
    run()