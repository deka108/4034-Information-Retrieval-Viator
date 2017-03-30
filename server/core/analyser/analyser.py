from server.utils import data_util


def run():
    data = data_util.get_all_posts_with_comments()
    print(data)


if __name__ == "__main__":
    run()