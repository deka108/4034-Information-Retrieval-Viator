from server.utils import data_util
import numpy as np
import pandas as pd

data_path = data_util.get_csv_filepath(data_util.SHUFFLED_DATA_FILENAME)

dictionary = list()
dict_food = ['food', 'predilection', 'restaurant', 'gustatory_modality', 'intellectual_nourishment', 'taste_sensation',
              'taste_perception', 'sample', 'sweet', 'gustatory_perception', 'delicious', 'taste', 'eating_place', 'savour',
              'meal', 'eatery', 'dejeuner', 'dinner_party', 'tiffin', 'perceptiveness', 'try', 'mouthful', 'gustation',
              'try_out', 'Delicious', 'afters', 'scrumptious', 'dinner', 'breakfast', 'gastronomy', 'penchant',
              'food_for_thought', 'nutrient', 'delightful', 'toothsome', 'solid_food', 'repast', 'dessert', 'luscious',
              'discernment', 'tasting', 'delectable', 'smack', 'preference', 'pleasant-tasting',
              'gustatory_sensation', 'lunch', 'luncheon', 'appreciation', 'sense_of_taste', 'yummy', 'savor', 'eating_house']

dict_nature = ['east_wind', 'exhibit', 'grocery_store', 'case', 'securities_industry', 'show', 'outcome', 'bear_witness',
               'evidence', 'market_place', 'read', 'demo', 'usher', 'record', 'fete', 'issue', 'lionise', 'Christmastide',
               'register', 'display', 'depict', 'Noel', 'testify', 'upshot', 'food_market', 'commercialise', 'lionize',
               'evince', 'Yuletide', 'Easter', 'shew', 'Christmas_Day', 'result', 'point', 'present', 'grocery',
               'designate', 'indicate', 'Xmas', 'render', 'easter', 'celebrate', 'Christmas', 'Christmastime',
               'firework', 'festival', 'establish', 'demonstrate', 'observe', 'keep', 'prove', 'effect',
               'marketplace', 'commercialize', 'picture', 'show_up',
               'pyrotechnic', 'Dec_25', 'mart', 'event', 'consequence', 'easterly', 'market', 'appearance', 'express',
               'concert', 'Yule']

dict_events = ['J._J._Hill', 'sight', 'timber', 'wad', 'muckle', 'raft', 'hiking', 'lot', 'heyday', 'flock',
               'Benny_Hill', 'woods', 'falls', 'peak', 'afforest', 'tidy_sum', 'efflorescence', 'timberland',
               'Hill', "pitcher's_mound", 'forest', 'wood', 'mess', 'Alfred_Hawthorne', 'quite_a_little', 'tramp',
               'peck', 'blossom', 'bloom', 'mickle', 'deal', 'prime', 'flush', 'slew', 'batch', 'pot', 'canyon',
               'mint', 'hill', 'undermine', 'plenty', 'ocean', 'waterfall', 'mount', 'flower', 'stack', 'nature', 'landscape',
               'hike', 'landscape_painting', 'mountain', 'great_deal', 'boost', 'James_Jerome_Hill', 'mass', 'passel',
               'hike_up', 'spate','woodland', 'heap', 'mound', 'sea', 'pile', 'canon', 'cave', 'river',
               'hatful', 'spelunk', 'lake', 'beach', 'good_deal']

dict_acc = ['detain', 'motel', 'check', 'night', 'stop', 'persist', 'halt', 'stay', 'bide', 'appease',
               'student_lodging', 'backpacker', 'last_out', 'outride', 'hotel', 'hostel', 'hostelry', 'stick',
               'stay_put', 'ride_out', 'nighttime', 'hitch', 'abide', 'Night', 'delay', 'arrest', 'youth_hostel',
               'dark', 'Nox', 'stoppage', 'lodge', 'remain', 'stick_around', 'quell', 'stay_on', 'auberge',
               'inn', 'continue', 'rest', 'packer']

dict_attr = ['bridge_deck', 'fence_in', 'church_service', 'bridge_circuit', 'wall', 'bridge_over', 'church',
               'surround', 'nosepiece', 'zoo', 'parkland', 'sail', 'aquarium', 'marine_museum', 'green',
               'museum', 'zoological_garden', 'Mungo_Park', 'architecture', 'ballpark', 'cruise', 'park', 'Park',
               'Christian_church', 'mosque', 'computer_architecture', 'car_park', 'parking_area', 'paries', 'span',
               'bridgework', 'enshrine', 'castle', 'commons', 'palisade', 'menagerie', 'bridge', 'fish_tank',
               'church_building', 'fence', 'bulwark', 'pagoda', 'shrine', 'palace', 'temple', 'common',
               'parking_lot', 'tabernacle', 'synagogue', 'rampart']

def label_data():
  df = pd.read_csv(data_path).astype(str)
  postId = df.iloc[:,1]
  post = df.iloc[:, 2]
  comments = df.iloc[:, 3]


  count_food = np.zeros((len(post), 1))
  count_events = np.zeros((len(post), 1))
  count_nature = np.zeros((len(post), 1))
  count_accommodation = np.zeros((len(post), 1))
  count_attraction = np.zeros((len(post), 1))
  count_others = np.zeros((len(post), 1))
  class_label = np.zeros((len(post), 1))

  col = ["id", "message+desc", "comments", "count_food", "count_events", "count_nature", 
  		"count_accommodation", "count_attraction", "count_others", "class_label"]

  categories = ['food', 'events', 'nature', 'accommodation', 'attraction', 'others']

  i = 0
  for p in post:
  	temp = p.split(" ")
  	#print(temp)
  	for word in temp:
  		if word in dict_nature:
  			count_nature[i][0] += 1
  		if word in dict_food:
  			count_food[i][0] += 1
  		if word in dict_events:
  			count_events[i][0] += 1
  		if word in dict_acc:
  			count_accommodation[i][0] += 1
  		if word in dict_attr:
  			count_attraction[i][0] += 1
  	if count_food[i][0]==0 and count_nature[i][0]==0 and count_events[i][0]==0 and count_accommodation[i][0]==0 and count_attraction[i][0]==0:
  		count_others[i][0] += 1
  	i += 1

  toWrite = np.column_stack((postId, post))
  toWrite = np.column_stack((toWrite, comments))
  toWrite = np.concatenate((toWrite, count_food, count_events, count_nature,
  	count_accommodation, count_attraction, count_others, class_label), axis=1)
  df2 = pd.DataFrame(toWrite, columns = col)
  df2.to_csv(data_util.get_csv_filepath(data_util.TOPIC_LABELLED_FILENAME), encoding='utf-8')

  print("topic_labelled.csv successfully generated")





