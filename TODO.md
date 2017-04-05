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
    - No of records: 14687
    - No of words: 779261
    - No of unique words: 40899
## Question 2: INDEXING AND QUERYING
- [X] Build a simple Web interface for the search engine
  - [X] Filtering
    - [X] Time ID
    - [X] Page ID
    - [X] Topic
    - [X] Sentiment
    - [X] Location
  - [X] Sort by
    - [X] Latest
    - [X] Relevance
    - [X] Shares count
    - [X] Reactions count
    - [X] Sentiment 
  - POPULARITY DISTRIBUTION
  - This distribution is a combination between comments_cnt, shares_cnt, and reactions_cnt
    - Normal: 0 - 100 (3343 posts)
    - Popular: 100 - 5000 (9926 posts)
    - Very Popular: 5000-10000(685 posts)
    - Extremely Popular: (594 posts)
 
- [ ] A simple UI for crawling and incremental indexing of new data would be a bonus  
(but not compulsory)
- [ ] Write five queries, get their results, and measure the speed of the querying

## Question 3: ENHANCING INDEXING AND RANKING
- [ ] Explain how the enhancement can solve specific problems, illustrated with examples.
  - [X] Spell suggestion and auto correction for user input
- [ ] (50%) Interactive search (refine search results based on spelling mistakes or similar search)
- [ ] Improve search results by integrating machine learning or data mining techniques  
(classification or cluster techniques)
  - [ ] (95%) Sentiment analysis per page id
    - -1 to 0: negative
    -  0 : neutral
    - 0 to 0.5: positive
    - 0.5 to 1: very positive
  - [ ] Auto Categorization
- [ ] (25%) Exploit geo-spatial data (i.e., map information) to refine query results/improve  
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
