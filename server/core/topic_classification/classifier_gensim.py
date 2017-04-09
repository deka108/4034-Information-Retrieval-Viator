from keras.layers import LSTM, Dropout, Dense, Activation
from keras.models import Sequential, load_model
from keras import metrics
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard

from server.utils import data_util
from server.core.gensim_models.gensim_model import DOCUMENT_MAX_NUM_WORDS, \
    NUM_FEATURES
from server.core.topic_classification import classification_preprocessing as\
    cp
from server.core.gensim_models import gensim_model
from server.core.topic_classification.classifier import BaseClassifier, \
    NUM_CATEGORIES, RFClassifier

import numpy as np


class NNClassifier(BaseClassifier):
    def __init__(self):
        BaseClassifier.__init__(self)
        self.check_point = "{}_model.h5"
        self.init_params("nn")
        self.create_model()

    def create_model(self):
        self.model = Sequential()

        self.model.add(LSTM(DOCUMENT_MAX_NUM_WORDS,
                       input_shape=(DOCUMENT_MAX_NUM_WORDS, NUM_FEATURES)))
        self.model.add(Dropout(0.1))
        self.model.add(Dense(NUM_CATEGORIES))
        self.model.add(Activation('sigmoid'))

        self.model.compile(loss='binary_crossentropy', optimizer='adam',
                      metrics=['accuracy'])
        return self.model

    def train_model(self, X_train, y_train):
        callbacks = [
            EarlyStopping(monitor='val_acc', verbose=1),
        ]
        self.model.fit(X_train, y_train, batch_size=128, nb_epoch=100,
                       validation_split=0.2, callbacks=callbacks)
        self.model.save(data_util.get_filepath(self.check_point))
        return self.model

    def predict(self, X_test):
        self.model = load_model(data_util.get_filepath(self.check_point))
        result = self.model.predict_classes(X_test)
        return result

    def evaluate(self, X_test, y_test):
        self.model = load_model(data_util.get_filepath(self.check_point))
        # Evaluate model
        score, acc = self.model.evaluate(X_test, y_test, batch_size=128)

        print('Score: %1.4f' % score)
        print('Accuracy: %1.4f' % acc)


def run():
    X, y = gensim_model.generate_features()
    X_train, X_test, y_train, y_test = cp.split_train_test(X, y)
    print(X_train.shape)
    print(y_train.shape)
    print(X_test.shape)

    # classifier = NNClassifier()
    # classifier.train_model(X_train, y_train)
    # print(classifier.model.predict(X_test))
    # print(classifier.model.predict_classes(X_test))
    # print(classifier.model.evaluate(X_test, y_test))


if __name__ == "__main__":
    run()