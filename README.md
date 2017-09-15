# Viator Application

Demo: https://www.youtube.com/watch?v=fcOc4POJIS0

Dependencies:
1. Please use Python 3.6 or PyCharm.
2. Install the required python package dependencies in requirements.txt:
`pip install -r requirements.txt`
3. Download and install solr. 
4. Please run solr at port 8983 (follow instruction at solr_instruction.txt) 
5. [Optional] Please run StanfordCoreNLP server at port 9000 in order to perform. This server can be downloaded
from https://stanfordnlp.github.io/CoreNLP/download.html. Run the server 
by using java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

How to run:
1. Run the solr server folllowing the instruction in solr directory.
2. Edit the `run_script.py` as necessary. Note that the location NER for geolocation can only be performed 
if the StanfordCoreNLP server is running, therefore it is commented by default.
3. Run `python run_script.py` to pre-processed files necessary for indexing.
4. Run `python run.py` to start the server at localhost:8888
5. Open browser and http://localhost:8888 to see our Viator engine :D
