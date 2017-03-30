from server.utils import data_util
from server.utils import text_util
from pycorenlp import StanfordCoreNLP
import ast

nlp = StanfordCoreNLP('http://localhost:9000')


def run():
    texts = text_util.get_text_data_all()
    texts['locations'] = texts['full_text'].apply(extract_location_from_text)
    data_util.write_df_to_existing_csv(texts, ['locations'],
                                       data_util.ALL_POSTS_COMMENTS_FILENAME)


def extract_location_from_text(text):
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,ner',
        'outputFormat': 'json'
    })

    if type(output) == str:
        output = ast.literal_eval(output)

    # for each sentence in a text / post
    locations = set()
    for sentence in output['sentences']:
        # extract location (combine consecutive ner location)
        prev_loc = False
        location = ""
        for token in sentence['tokens']:
            if token['ner'] == 'LOCATION':
                if prev_loc:
                    location += " " + token['originalText']
                else:
                    location = token['originalText']
                prev_loc = True
            else:
                if prev_loc:
                    locations.add(location)
                    location = ""
                prev_loc = False

        if prev_loc:
            locations.add(location)

    if len(locations) > 0:
        return '$$'.join(locations)
    else:
        return ""


if __name__ == "__main__":
    run()