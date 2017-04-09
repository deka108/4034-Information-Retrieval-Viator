from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from server.core.topic_classification import classification_preprocessing as\
    cp
from server.core.topic_classification.classifier import NBClassifier, \
    RFClassifier, LRClassifier
from server.utils import text_util


def get_data_set():
    X, y = cp.get_all_data_with_name()
    X = [" ".join(text_util.preprocess_text(text, lemmatize=True)) for text
         in X]
    X_train, X_test, y_train, y_test = cp.split_train_test(X, y)
    return X_train, X_test, y_train, y_test


def vectorize_data(vectorizer, X_train, X_test):
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)
    return X_train, X_test


def classify(X_train, X_test, y_train, y_test):
    tfidf_vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5,
                                       stop_words='english')
    count_vectorizer = CountVectorizer()
    vectorizers = {
        'tf-idf': tfidf_vectorizer,
        'count-vectorizer': count_vectorizer
    }
    X_train = [post for post in X_train if isinstance(post, str) and len(
        post) > 0]
    X_test = [post for post in X_test if isinstance(post, str) and len(post)
              > 0]

    for vectorizer in vectorizers:
        print(vectorizer)
        procX_train, procX_test = vectorize_data(vectorizers[vectorizer],
                                              X_train, X_test)
        naive_bayes(procX_train, procX_test, y_train, y_test)
        random_forest(procX_train, procX_test, y_train, y_test)
        logistic_regression(procX_train, procX_test, y_train, y_test)


def naive_bayes(X_train, X_test, y_train, y_test):
    print("Naive bayes")
    clf = NBClassifier()
    clf.run(X_train, X_test, y_train, y_test)


def random_forest(X_train, X_test, y_train, y_test):
    print("Random forest")
    clf = RFClassifier()
    clf.run(X_train, X_test, y_train, y_test)


def logistic_regression(X_train, X_test, y_train, y_test):
    print("Logistic regresssion")
    clf = LRClassifier()
    clf.run(X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = get_data_set()
    classify(X_train, X_test, y_train, y_test)