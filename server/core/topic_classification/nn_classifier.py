from keras.layers import LSTM, Dropout, Dense, Activation
from keras.models import Sequential
from server.core.topic_classification import classifier
from server.core.topic_classification.word2vec import \
    DOCUMENT_MAX_NUM_WORDS, NUM_FEATURES

NUM_CATEGORIES = 5


class NNClassifier(classifier.Classifier):
    def __init__(self):
        classifier.Classifier.__init__(self)
        self.init_params("nn")
        self.create_model()

    def create_model(self):
        self.model = Sequential()

        self.model.add(LSTM(int(DOCUMENT_MAX_NUM_WORDS * 1.5),
                       input_shape=(DOCUMENT_MAX_NUM_WORDS, NUM_FEATURES)))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(NUM_CATEGORIES))
        self.model.add(Activation('sigmoid'))

        self.model.compile(loss='binary_crossentropy', optimizer='adam',
                      metrics=['accuracy'])

    def train_model(self, X_train, y_train, *args):
        # Train model
        self.model.fit(X_train, y_train, batch_size=128, nb_epoch=5,
                  validation_data=(args[0], args[1]))

    def predict(self, X_test, *args):

        # Evaluate model
        score, acc = self.model.evaluate(X_test, args[0], batch_size=128)

        print('Score: %1.4f' % score)
        print('Accuracy: %1.4f' % acc)


if __name__ == "__main__":
    classifier = ()
    print(classifier.model)