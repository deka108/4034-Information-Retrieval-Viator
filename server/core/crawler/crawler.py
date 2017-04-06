import datetime
import json
import time
import urllib.request

import facebook

from server.utils import data_util


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


def crawl_page(page_id, access_token):
    has_next_page = True
    num_processed = 0
    fields = "posts?fields=id,created_time,message,message_tags,caption,description,icon,link,likes.limit(0).summary(true)," + \
             "reactions.limit(0).summary(total_count),shares,story,story_tags,actions,from, " + \
             "type,status_type,name,parent_id,place,source,object_id,picture,full_picture,updated_time,comments.summary(true)&filter=toplevel"

    graph = facebook.GraphAPI(access_token, version='2.7')
    profile = graph.get_object(page_id)
    posts = graph.get_connections(profile['id'], fields)
    print("Start crawling " + page_id + "\n")
    post_list = []
    db_records = data_util.get_db_records()
    print(db_records)

    try:
        while has_next_page:
            for post in posts['data']:
                post_list.append(post)
                print(post['created_time'])
                num_processed += 1
                if num_processed % 100 == 0:
                    print("%s Statuses Processed: %s" % \
                          (num_processed, datetime.datetime.now()))

            # request next page
            if 'paging' in posts.keys():
                posts = json.loads(
                    request_until_succeed(posts['paging']['next']))

            else:
                has_next_page = False
                print(num_processed)
                db_records[page_id] = {
                    "count": num_processed,
                    "last_updated": str(datetime.datetime.now())
                }

        data_util.write_page_data_to_json(post_list, page_id)
        data_util.write_db_records_to_json(db_records)

        print("Done crawling " + page_id + "\n")
        return True
    except:
        return False


def crawl_all(access_token):
    try:
        data_util.init_db_records()
        records = data_util.get_db_records()
        for page_id in records:
            crawl_page(page_id, access_token)
        return True
    except:
        return False

        # page_id = "Tripviss"
        # access_token= "EAACEdEose0cBAMcpRfd7VRuKWwQ1qbZAITE8T0wcCM91yGCF7lsfJhh2I33Gj7svQberl0CyB3w8BYEBIZAzWKkBU5nBpfILJUacIcvppEZCVvSVNhfn7tmstEITfDrj3ttjp315xABcY2M2VeYijbVGguYjLMkePmaKEl8gEPqA0JmPednDGQF7NTG0iWLhl65BIReHAZDZD"
