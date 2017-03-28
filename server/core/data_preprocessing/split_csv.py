import json
import pandas as pd
import numpy as np
import csv
import os



url = "topic_labelled.csv"


csv_column = ['id', 'message+desc', "count_food", "count_events", "count_nature", 
		"count_accommodation", "count_attraction", "count_others", "class_label"]
shuffled = pd.read_csv(url, encoding='utf-8').iloc[:, 1:].astype(str)
data = np.array_split(shuffled, 5)
 
for i in range(len(data)):
	df3 = pd.DataFrame(data[i], columns = csv_column)
	df3.to_csv('./split_csvs/train_data' + str(i) + '.csv', encoding='utf-8')

