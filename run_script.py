from server.core.data_preprocessing import preprocessing
from server.core.data_preprocessing import generate_csv
from server.utils import data_util as du


def run():
    preprocessing.preprocess_all_pages()
    generate_csv.generate_splitted_csv_for_labelling()

    # Example of getting json based on page_id
    # page_id = "koreatourism"
    # korea = data_util.get_preprocessed_json_data_by_page_id(page_id)

    # Example of combining all the preprocessed pages (not recommended, size
    # is too big)
    # data_util.get_preprocessed_json_data_all()

if __name__ == "__main__":
    run()
    print(len(du.get_all_posts_with_comments()))