from server.utils import text_util as tu
from server.utils import data_util as du
from textblob.en.np_extractors import ChunkParser, FastNPExtractor
from textblob import TextBlob
from textblob.tokenizers import  SentenceTokenizer

np_extractor = FastNPExtractor()
sent_tokenizer = SentenceTokenizer()

def extract_pronoun():
    all_posts = extract_pos_tag_from_posts()
    pronouns = set()
    pronoun = ""
    prev_nnp = False
    for post in all_posts:
        for token in post:
            if token[1] == 'NNP':
                if prev_nnp:
                    pronoun += " " + token[0]
                else:
                    pronoun = token[0]
                prev_nnp = True
            else:
                if prev_nnp:
                    pronouns.add(pronoun)
                prev_nnp = False
                pronoun = ""
    if prev_nnp:
        pronouns.add(pronoun)
    pronouns = list(pronouns)
    pronouns.sort()
    print(pronouns)


def extract_pos_tag_from_post(text):
    sentences = TextBlob(text)

    return sentences.tags


def extract_pos_tag_from_posts():
    page_ids = du.get_page_ids()
    for page_id in page_ids:
        text_data = tu.get_text_data_by_page_id(page_id)
        for idx, row in text_data.iterrows():
            for sent in sent_tokenizer.tokenize(row['full_text']):
                print(np_extractor.extract(sent))



if __name__ == "__main__":
    # extract_pronoun()
    extract_pos_tag_from_posts()