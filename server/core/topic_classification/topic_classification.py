from server.utils import data_util


def add_topic(page_id):
    print(page_id)


def add_topic_to_allpages():
    page_ids = data_util.get_all_posts()
    for page_id in page_ids:
        add_topic(page_id)


if __name__ == "__main__":
    add_topic_to_allpages()