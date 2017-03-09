from server.core.data_preprocessing import preprocessing


def run():
    page_id = "Tripviss"
    preprocessing.preprocess_page_json(page_id)
    preprocessing.read_csv_by_pageid(page_id)
    preprocessing.compute_words(page_id)


if __name__ == "__main__":
    run()