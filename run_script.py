from server.core.data_preprocessing import preprocessing
from server.utils import data_util
from server.core.nlp import sentiment, extract_geocoding, location_ner_stanford
from server.core.data_preprocessing import generate_csv
from server.utils import data_util as du
from server.core.data_preprocessing import statistic
from server.core.topic_classification import topic_classification as tc
from server.core.topic_classification import generate_model as gm
import nltk

# nltk.data.path.append('D:/nltk_data/')


def run():
    # COMMENT / UNCOMMENT AS NECESSARY, all pages vs specific page
    preprocessing.preprocess_all_pages()


    # Example of getting json based on page_id
    # page_id = "koreatourism"
    # korea = data_util.get_preprocessed_json_data_by_page_id(page_id)


    # Computing statistics
    #statistic.compute_words(du.ALL_POSTS_FILENAME)

    # Adding sentiment
    # sentiment.get_sentiment_all_pages()
    # sentiment.get_sentiment(page_id)

    # Topic classification
    gm.run()
    tc.add_topic_to_all_pages()


    # GEOLOCATION: performing Location NER + extract geocoding

    # Performing Location NER
    # Location NER: requires STANFORD API
    # location_ner_stanford.run()
    # location_ner_stanford.run_pageid(page_id)

    # Add Geocoding (coordinates to posts)
    # extract_geocoding.run()
    # extract_geocoding.run_pageid(page_id)




if __name__ == "__main__":
    run()