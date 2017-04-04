from server.core.nlp import sentiment, extract_geocoding


def run():
    sentiment.run()
    # extract_geocoding.run()
    # extract_geocoding.run()

    #location_ner_stanford.run()


if __name__ == "__main__":
    run()