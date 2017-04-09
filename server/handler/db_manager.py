import json
import os

from flask import Blueprint, abort, jsonify, request, make_response

from server.utils import data_util
from server.core.data_preprocessing import preprocessing
from server.core.nlp import sentiment, extract_geocoding, location_ner_stanford
from server.core.topic_classification import topic_classification, generate_model
from server.core.crawler import crawler
# access_token = 'EAACEdEose0cBAP9s5lDmTubZAGr2KBKnAaQulX54mUvVV0mniQrhvbRDG3xcvzmsaMfMQFbkF2UFpluEX18kP7w5dgFjNjORmy7xJenpP8j4AbXZBD2DNfh4VsGTEgP0S5I5tChl7mY4UmtRt9pzvWBAyMEsz3LR63aTmscU0uVURQQUxIsO7a8lg77o5ZBHH5oyzif7wZDZD'

db_manager = Blueprint('db_manager', __name__, static_folder='static')

@db_manager.route('/crawl/', methods=['POST'])
def crawl():
    try:
        request_data = json.loads(request.get_data())
        print("Crawling...")

        if request_data:
            page_id = request_data.get("page_id")
            access_token = request_data.get("token")
            print(page_id)
            print(access_token)

        if access_token:
            if not page_id:
                crawler.crawl_all(access_token)
                preprocessing.preprocess_all_pages()
                sentiment.get_sentiment_all_pages()
                # generate_model.run()
                topic_classification.add_topic_to_all_pages()

                print("Success Crawling all pages!")
                page_id = "all"
            else:
                crawler.crawl_page(page_id, access_token)
                preprocessing.preprocess_page_json(page_id)
                sentiment.get_sentiment(page_id)
                # generate_model.run()
                topic_classification.add_topic(page_id)

                print("Success crawling {}".format(page_id))

        return jsonify({
            "page_id": page_id,
            "access_token": access_token
        })
    except Exception as e:
        print(e)
        return make_response(str(e), 404)


@db_manager.route('/classify_location/', methods=["POST"])
def add_location():
    try:
        request_data = json.loads(request.get_data())
        print("Performing location recognition...")

        if request_data:
            page_id = request_data.get("page_id")

        if not page_id:
            location_ner_stanford.run()
            extract_geocoding.run()
            page_id = "all"
        else:
            location_ner_stanford.run_pageid(page_id)
            extract_geocoding.run_pageid(page_id)

        return jsonify({
            "page_id": page_id,
            "status": "Added topic class to page: {}".format(page_id)
        })
    except Exception as e:
        print(e)
        return make_response(str(e), 404)


@db_manager.route('/db_records/', methods=['GET'])
def get_all_data():
    db_records = data_util.get_db_records()
    if db_records:
        return jsonify(db_records)
    return make_response("Record does not exist", 404)


@db_manager.route('/solr_records/', methods=['GET'])
def get_all_time_data():
    solr_infos = data_util.get_solr_records()
    if solr_infos:
        return jsonify(solr_infos)
    return make_response("Record does not exist", 404)


@db_manager.route('/read/', defaults={'page_id': None})
@db_manager.route('/read/<page_id>', methods=['GET'])
def read_data(page_id):
    if page_id:
        data = data_util.get_preprocessed_json_data_by_page_id(page_id)
        if data:
            return jsonify(data)
    else:
        # not recommended, data is too big
        page = int(request.args.get('p'))
        data = data_util.get_preprocessed_json_data_all()
        from_index = page*10
        to_index = from_index+10
        if data:
            return jsonify(data[from_index:to_index])
    return make_response("Unable to retrieve data", 404)


@db_manager.route('/delete/', methods=['GET'])
def delete_all_data():
    if data_util.delete_db_records():
        return make_response("All data is deleted successfully", 200)
    return make_response("Fail to delete all pages", 404)


@db_manager.route('/delete/<page_id>', methods=['GET'])
def delete_data(page_id):
    if data_util.delete_db_record(page_id):
        return make_response("{} is deleted successfully".format(page_id), 200)
    return make_response("Fail to delete page id: {} data".format(page_id),
                         404)


@db_manager.route('/read_split/<split_id>', methods=['GET'])
def retrieve_split_data(split_id):
    try:
        csv_path = data_util.get_splitted_csv_filepath(split_id)
        data = data_util.get_json_data_from_csv(csv_path)
        if data:
            return jsonify(data)
    except:
        print("Error")
    return make_response("Split data Id does not exist", 404)
