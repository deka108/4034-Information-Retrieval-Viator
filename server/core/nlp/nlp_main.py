from server.core.nlp import sentiment, location_ner_stanford


def run():
    sentiment.run()
    #location_ner_stanford.run()


if __name__ == "__main__":
    run()