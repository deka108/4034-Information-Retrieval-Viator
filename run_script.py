from server.core.data_preprocessing import preprocessing


def run():
    preprocessing.preprocess_all_pages()


if __name__ == "__main__":
    run()