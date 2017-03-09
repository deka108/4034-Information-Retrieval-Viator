import facebook
import requests
import json
import urllib.request
import time
import datetime

from server import config
from server import data_util

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
    fields = "posts?fields=id,created_time,message,message_tags,link,likes.limit(0).summary(true)," + \
             "reactions.limit(0).summary(total_count),shares,story,story_tags,actions,from," + \
             "type,status_type,name,object_id,picture,updated_time,comments.summary(true)&filter=toplevel"

    graph = facebook.GraphAPI(access_token,version='2.7')
    profile = graph.get_object(page_id)
    posts = graph.get_connections(profile['id'], fields)
    print(data_util.get_json_file_path(page_id))
    print("Start crawling " + page_id + "\n")
    list = []
    records = {}
    with open(config.RECORDS_DATA_PATH) as record_file:
        if record_file == None :
            pass
        else:
            records = json.load(record_file)
    print(config.RECORDS_DATA_PATH)
    try:
        while has_next_page:
            for post in posts['data']:
                list.append(post)
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
                records[page_id] = num_processed
                with open('records.json', 'w') as fp:
                     json.dump(records, fp)
                # # file = open(config.RECORDS_DATA_PATH, 'a')
                # file.write("%s" % page_id + ": " + "%s" % num_processed + "\n")
                fp.close()


        with open(data_util.get_json_file_path(page_id), 'w', newline='', encoding='utf-8') as outfile:
            json.dump(list, outfile, sort_keys=True, indent=4)
            print("Done crawling " + page_id + "\n")
            return True
    except:
        return False
    

def crawl_all(access_token):
    try:
        fo = open(config.RECORDS_DATA_PATH, "w")
        fo.truncate()
        with open(config.INITIAL_PAGEID_PATH) as f:
            line = f.readlines()
            content = [x.strip() for x in line]
        for page in content:
            crawl_page(page, access_token)
            # print (page)
        return True
    except:
        return False

# page_id = "Tripviss"
# access_token= "EAACEdEose0cBAMcpRfd7VRuKWwQ1qbZAITE8T0wcCM91yGCF7lsfJhh2I33Gj7svQberl0CyB3w8BYEBIZAzWKkBU5nBpfILJUacIcvppEZCVvSVNhfn7tmstEITfDrj3ttjp315xABcY2M2VeYijbVGguYjLMkePmaKEl8gEPqA0JmPednDGQF7NTG0iWLhl65BIReHAZDZD"
# if __name__ == '__main__':
#     crawl_page(page_id,access_token)