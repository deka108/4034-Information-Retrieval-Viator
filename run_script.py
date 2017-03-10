from server.core.data_preprocessing import preprocessing
from server.utils import data_util


def run():
    preprocessing.preprocess_all_pages()

    # Example of getting json based on page_id
    # page_id = "koreatourism"
    # korea = data_util.get_preprocessed_json_data_by_page_id(page_id)

    # Example of combining all the preprocessed pages (not recommended, size
    # is too big)
    # data_util.get_preprocessed_json_data_all()


if __name__ == "__main__":
    run()