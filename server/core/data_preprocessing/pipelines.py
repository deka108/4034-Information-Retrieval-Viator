import multiprocessing
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from server.core.topic_classification import classification_preprocessing as cp
from server.utils import text_util
from server.utils.text_util import tokenize


def run_multinomial_countvectorizer(X_train, X_test, y_train, y_test):
    count_vectorizer = CountVectorizer()
    multinomialNB = MultinomialNB()

    # Define pipeline

    mn_cv_nb_pipeline = Pipeline([('vectorizer', count_vectorizer),
                                 ('multinomial_nb', multinomialNB)])

    # Grid search parameters
    mn_cv_nb_param_grid = [
        {
            # 'vectorizer__min_df': [ 1, 2, 3, 4, 5 ],
            'vectorizer__min_df': [3,],
            'vectorizer__ngram_range': [ (1, 1), (1, 2), (1, 3) ],
            # 'multinomial_nb__alpha': [ 0.0, 0.25, 0.5, 0.75, 1.0 ],
            'multinomial_nb__alpha': [0.5]
        }
    ]

    # Perform grid search
    mn_cv_nb_gs = GridSearchCV(estimator=mn_cv_nb_pipeline, param_grid=mn_cv_nb_param_grid,
                               scoring='accuracy', cv=4,
                               n_jobs=multiprocessing.cpu_count())

    mn_cv_nb_gs.fit(X_train, y_train)

    # Create an instance of the best estimator
    mn_cv_nb_best = mn_cv_nb_gs.best_estimator_
    mn_cv_nb_best.fit(X_train, y_train)

    print('Best model: %s' % str(mn_cv_nb_gs.best_params_))
    print('Best score: %f' % mn_cv_nb_gs.best_score_)
    print('Best test accuracy: %f' % mn_cv_nb_best.score(X_test, y_test))


def run():
    X_train, X_test, y_train, y_test = cp.run()
    tokenizer_func = np.vectorize(text_util.tokenize)
    print(X_train.shape)
    X_train = tokenizer_func(X_train)
    print(X_train.shape)
    X_test = tokenizer_func(X_test)
    # run_multinomial_countvectorizer(X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    run()