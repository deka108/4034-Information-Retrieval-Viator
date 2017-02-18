import facebook
import requests
import json
import urllib.request
import time
import datetime


access_token = 'EAACEdEose0cBAIyGEt0HmSXL9QgScefVc9HeEIQG1Pa561At2aoBi7X5ZB92lM4RZBSD2hv9kpJ4ZAoevCHNGY8I52VtA5q1E8WIYKtOIJMbuIMpUZCZBHAobrr3ChjqQogpP7sDmdPD9SDILvrwOtt8OPrlXcazUuoP7fVMZBoX4UrCDYZA5xfrq0e6LFZBlZA7BTR3ZBCmk0GQZDZD'


post_id = 'goturkeytourism'

base = "https://graph.facebook.com/v2.8"
node = "/%s/posts" % post_id
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




def some_action(post):
    try:
        print(post['message'])
    except KeyError as e:
        print(e)

    #print (json.dumps(post),indent=4, sort_keys=True)


def crawl_data(post_id,access_token):
    has_next_page = True
    num_processed = 0
    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object(post_id)
    posts = graph.get_connections(profile['id'], 'posts')
    #comments = graph.get_all_connections(profile['id'], 'comments')
    with open('%s_facebook.json' %post_id, 'w', newline='', encoding='utf-8') as outfile:
        json.dump(posts, outfile, sort_keys=True, indent=4)


    while has_next_page:
        #[some_action(post=post) for post in posts['data']]
        for post in posts['data']:
            num_processed += 1
            if num_processed % 100 == 0:
                print("%s Statuses Processed: %s" % \
                  (num_processed, datetime.datetime.now()))

           #request next page
             #posts = requests.get(posts['paging']['next']).json()
        #with open('%s_facebook_statuses.csv' % page_id, 'w', newline='', encoding='utf-8') as file:
        if('paging' in posts.keys()):
            posts = json.loads(request_until_succeed(posts['paging']['next']))
        else:
            has_next_page = False
            file = open('records.txt', 'a')
            file.write("%s" % post_id + ": " + "%s" % num_processed + "\n")
            file.close()



if __name__ == '__main__':
    crawl_data(post_id, access_token)
