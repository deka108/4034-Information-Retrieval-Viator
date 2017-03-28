import json
import pandas as pd
import numpy as np
from pprint import pprint
import os


url = './cz4034-information-retrieval/server/data/'

name = os.listdir(url)

f = ['records.json', 'initial_records.json', 'Tripviss_facebook.json']
k = 0
message = list()
message_id = list()
for j in range(0, len(name)):
    filename = name[j]
    print(filename)
    if (filename.endswith(".json") and filename not in f):
        newfilename = url + filename
        with open(newfilename) as json_data: 
            data = json.load(json_data)

        for i in range(len(data)):
            temp = ""
            message_id.append(data[i]['id'])
            if 'message' in data[i]:
                temp += data[i]['message']
            if 'description' in data[i]:
                temp += data[i]['description']
            message.append(temp)



csv_column = ['id', 'message+description']

comb = np.column_stack((message_id, message))

df = pd.DataFrame(comb, columns = csv_column)
df.to_csv('ordered_data.csv', index = False, encoding='utf-8')

train = pd.read_csv('ordered_data.csv')

train_shuffled = train.reindex(np.random.permutation(train.index))

df2 = pd.DataFrame(train_shuffled, columns = csv_column)
df2.to_csv('combined_data.csv', encoding='utf-8')
