from sklearn.datasets.twenty_newsgroups import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans

import numpy as np
import pandas as pd

categories = ['food', 'events', 'nature', 'accommodation', 'attraction']
true_k = 5

dictionary = list()
dictionary = ['food', 'predilection', 'restaurant', 'gustatory_modality', 'intellectual_nourishment', 'taste_sensation',
              'taste_perception', 'sample', 'sweet', 'gustatory_perception', 'delicious', 'taste', 'eating_place', 'savour',
              'meal', 'eatery', 'dejeuner', 'dinner_party', 'tiffin', 'perceptiveness', 'try', 'mouthful', 'gustation',
              'try_out', 'Delicious', 'afters', 'scrumptious', 'dinner', 'breakfast', 'gastronomy', 'penchant',
              'food_for_thought', 'nutrient', 'delightful', 'toothsome', 'solid_food', 'repast', 'dessert', 'luscious',
              'discernment', 'tasting', 'delectable', 'smack', 'preference', 'pleasant-tasting',
              'gustatory_sensation', 'lunch', 'luncheon', 'appreciation', 'sense_of_taste', 'yummy', 'savor', 'eating_house']

dictionary += ['east_wind', 'exhibit', 'grocery_store', 'case', 'securities_industry', 'show', 'outcome', 'bear_witness',
               'evidence', 'market_place', 'read', 'demo', 'usher', 'record', 'fete', 'issue', 'lionise', 'Christmastide',
               'register', 'display', 'depict', 'Noel', 'testify', 'upshot', 'food_market', 'commercialise', 'lionize',
               'evince', 'Yuletide', 'Easter', 'shew', 'Christmas_Day', 'result', 'point', 'present', 'grocery',
               'designate', 'indicate', 'Xmas', 'render', 'easter', 'celebrate', 'Christmas', 'Christmastime',
               'firework', 'festival', 'establish', 'demonstrate', 'observe', 'keep', 'prove', 'effect',
               'marketplace', 'commercialize', 'picture', 'show_up',
               'pyrotechnic', 'Dec_25', 'mart', 'event', 'consequence', 'easterly', 'market', 'appearance', 'express',
               'concert', 'Yule']

dictionary += ['J._J._Hill', 'sight', 'timber', 'wad', 'muckle', 'raft', 'hiking', 'lot', 'heyday', 'flock',
               'Benny_Hill', 'woods', 'falls', 'peak', 'afforest', 'tidy_sum', 'efflorescence', 'timberland',
               'Hill', "pitcher's_mound", 'forest', 'wood', 'mess', 'Alfred_Hawthorne', 'quite_a_little', 'tramp',
               'peck', 'blossom', 'bloom', 'mickle', 'deal', 'prime', 'flush', 'slew', 'batch', 'pot', 'canyon',
               'mint', 'hill', 'undermine', 'plenty', 'ocean', 'waterfall', 'mount', 'flower', 'stack', 'nature', 'landscape',
               'hike', 'landscape_painting', 'mountain', 'great_deal', 'boost', 'James_Jerome_Hill', 'mass', 'passel',
               'hike_up', 'spate','woodland', 'heap', 'mound', 'sea', 'pile', 'canon', 'cave', 'river',
               'hatful', 'spelunk', 'lake', 'beach', 'good_deal']

dictionary += ['detain', 'motel', 'check', 'night', 'stop', 'persist', 'halt', 'stay', 'bide', 'appease',
               'student_lodging', 'backpacker', 'last_out', 'outride', 'hotel', 'hostel', 'hostelry', 'stick',
               'stay_put', 'ride_out', 'nighttime', 'hitch', 'abide', 'Night', 'delay', 'arrest', 'youth_hostel',
               'dark', 'Nox', 'stoppage', 'lodge', 'remain', 'stick_around', 'quell', 'stay_on', 'auberge',
               'inn', 'continue', 'rest', 'packer']

dictionary += ['bridge_deck', 'fence_in', 'church_service', 'bridge_circuit', 'wall', 'bridge_over', 'church',
               'surround', 'nosepiece', 'zoo', 'parkland', 'sail', 'aquarium', 'marine_museum', 'green',
               'museum', 'zoological_garden', 'Mungo_Park', 'architecture', 'ballpark', 'cruise', 'park', 'Park',
               'Christian_church', 'mosque', 'computer_architecture', 'car_park', 'parking_area', 'paries', 'span',
               'bridgework', 'enshrine', 'castle', 'commons', 'palisade', 'menagerie', 'bridge', 'fish_tank',
               'church_building', 'fence', 'bulwark', 'pagoda', 'shrine', 'palace', 'temple', 'common',
               'parking_lot', 'tabernacle', 'synagogue', 'rampart']

df = pd.read_csv('combined_data.csv').astype(str)
dataset = df.iloc[:,2]

vectorizer = TfidfVectorizer(max_df=0.5, max_features=446, min_df=2, vocabulary=dictionary,
                             stop_words='english', use_idf=True)

X=vectorizer.fit_transform(dataset)

km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1, verbose=True)
km.fit(X)

order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :80]:
        print(' %s' % terms[ind], end='')
    print()


cols = ["unnamed", "id", "description", "class"]
comb =  np.column_stack((df, km.labels_))
dfWrite = pd.DataFrame(comb, columns=cols)
dfWrite.to_csv('result.csv')
