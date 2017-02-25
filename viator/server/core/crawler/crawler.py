import facebook
import requests
import json
import urllib.request
import time
import datetime

access_token = 'EAACEdEose0cBAIVoIaZAajt0ZBAVZBLE9Gl4cxJhDSXh1r7WqDN6lut0UiEpHMbJdytQnMpUaNoKuXpnXFa2nidNvkP3xkwmsAywdcXxxgySsyhH3VQwGTapY8lSL4B9tda2bT4jutbkl9L0d5GedCavVLdaZA6SZCaTa4zHhqjMrt3Pk4KTuZB3SyZAAHhK0ZAfDtkjfRLT4gZDZD'
page_id = 'visitchinanow'
base = "https://graph.facebook.com/v2.8"
node = "/%s/posts" % page_id
fields = "/?fields=message,link,created_time,type,name,id," + \
         "comments.limit(0).summary(true),shares,reactions" + \
         ".limit(0).summary(true)"
parameters = "&limit=%s&access_token=%s" % (100, access_token)
url = base + node + fields + parameters


def request_until_succeed(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)
            print("Error for URL %s: %s" % (url, datetime.datetime.now()))
            print("Retrying.")
    return response.read().decode(response.headers.get_content_charset())


def crawl_data(page_id, access_token):
    has_next_page = True
    num_processed = 0
    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(page_id)
    posts = graph.get_connections(profile['id'], 'posts')

    list = []
    while has_next_page:
        list.append(posts)
        for post in posts['data']:
            print(post['created_time'])
            num_processed += 1
            if num_processed % 100 == 0:
                print("%s Statuses Processed: %s" % \
                      (num_processed, datetime.datetime.now()))

        # request next page
        if 'paging' in posts.keys():
            posts = json.loads(request_until_succeed(posts['paging']['next']))

        else:
            has_next_page = False
            print(num_processed)
            file = open('records.txt', 'a')
            file.write("%s" % page_id + ": " + "%s" % num_processed + "\n")
            file.close()

    with open('%s_facebook.json' % page_id, 'a', newline='', encoding='utf-8') as outfile:
        json.dump(list, outfile, sort_keys=True, indent=4)


#if __name__ == '__main__':
def crawl_main():
    crawl_data(page_id, access_token)
    return "yay"


def test():
    return "test"