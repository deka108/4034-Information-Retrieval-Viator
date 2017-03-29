from server.core.data_preprocessing import preprocessing
from server.core.data_preprocessing import topic_labeling
from server.core.data_preprocessing import generate_csv
from server.utils import data_util as du


def run():
    preprocessing.preprocess_all_pages()

    # Example of getting json based on page_id
    # page_id = "koreatourism"
    # korea = data_util.get_preprocessed_json_data_by_page_id(page_id)

    # Example of combining all the preprocessed pages (not recommended, size
    # is too big)
    # data_util.get_preprocessed_json_data_all()

    generate_csv.csv_to_csv()
    generate_csv.shuffle_data()
    topic_labeling.label_data()
    generate_csv.split_csv()

if __name__ == "__main__":
    # run()
    print(len(du.get_all_posts_with_comments()))