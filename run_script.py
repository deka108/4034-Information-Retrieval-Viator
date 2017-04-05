from server.core.data_preprocessing import preprocessing
from server.core.nlp import nlp_main
from server.core.data_preprocessing import generate_csv
from server.utils import data_util as du
from server.core.data_preprocessing import statistic
from server.core.topic_classification import topic_classification as tc
from server.core.topic_classification import generate_model as gm
import nltk

# nltk.data.path.append('D:/nltk_data/')

def run():
    preprocessing.preprocess_all_pages()
    # generate_csv.generate_splitted_csv_for_labelling()
    # statistic.compute_words(du.ALL_POSTS_FILENAME)
    nlp_main.run()




    # Example of getting json based on page_id
    # page_id = "koreatourism"
    # korea = data_util.get_preprocessed_json_data_by_page_id(page_id)

    # Example of combining all the preprocessed pages (not recommended, size
    # is too big)
    # data_util.get_preprocessed_json_data_all()


    """CLASSIFY BY TOPIC"""
    gm.run()
    tc.add_topic_to_all_pages()


if __name__ == "__main__":
    run()