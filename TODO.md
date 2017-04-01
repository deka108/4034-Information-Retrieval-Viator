## Question 1: CRAWLING
- [ ] How you crawled the corpus:
  - [X] Crawl the corpus (source, keywords, API, library): 
    - API: Facebook Graph API 
    - Library: Facebook SDK for Python 
    - Source: 12 Facebook Travel Pages
    - Keywords: ? 
  - [X] How you stored them? (whether a record corresponds to a file or a line, meta information like publication date, author  
  name, record ID)
    - Each pages is saved inside json file. Each json header corresponds to the field or information of the posts (post ID,  
    author, created_time)
- [ ] Information users might like to retrieve from your crawled corpus:
  - [ ] Example queries
- [X] Statistics:
  - [X] The numbers of records, words, and types(UNIQUE WORDS) in the corpus
    - No of records: 16009
    - No of words: 
    - No of unique words: 
## Question 2: INDEXING AND QUERYING
- [ ] Build a simple Web interface for the search engine
- [ ] A simple UI for crawling and incremental indexing of new data would be a bonus  
(but not compulsory)
- [ ] Write five queries, get their results, and measure the speed of the querying

## Question 3: ENHANCING INDEXING AND RANKING
- [ ] Explain how the enhancement can solve specific problems, illustrated with examples.
- [ ] Interactive search (refine search results based on spelling mistakes or similar search)
- [ ] Improve search results by integrating machine learning or data mining techniques  
(classification or cluster techniques)
- [ ] Go beyond text-based search (implement image retrieval or multimedia retrieval)
- [ ] Exploit geo-spatial data (i.e., map information) to refine query results/improve  
presentation/visualization

## Question 4: CLASSIFICATION TASKS
- [ ] Motivate the choice of classification approach in relation with the state of the art
- [ ] Data preprocessing
- [ ] Build an evaluation dataset by manually labeling 10% of the collected data with an 
inter-annotator agreement of at least 80%.
- [ ] Provide evaluation metrics such as precision, recall, and F-measure and discuss results
- [ ] Discuss performance metrics, e.g., records classified per second, and scalability  
of the system
- [ ] A simple UI for visualizing classified data would be a bonus (but not compulsory)

## Question 5: ENHANCING CLASSIFICATION
- [ ] Provide some innovation for classification and explain why they are important with  
examples
- [ ] Ensemble classification
- [ ] Cognitive classification
- [ ] Multi-faceted classification
