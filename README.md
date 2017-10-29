# Information Retrieval. Assignment 2

[boolean_retrieval]: https://github.com/and-kul/boolean_retrieval

This is further improvement of my [boolean_retrieval] project.

## Preparing environment
Technical requirements still the same, you need:
* Python 3.6
* *NLTK* with *NLTK Data*

You can find installation details in [boolean_retrieval] project.

## Structure
There are 2 subprojects in this repository, each responsible for different thing:
1. **index_builder**
2. **search**

You can run each through `python main.py` and see nice help using `python main.py -h` (there you can discover, for example, what arguments to use for changing default filenames)

## index_builer
This subproject creates an inverted index for documents from **documents.json** (default name, could be changed) and stores it in **index.json** (default name, could be changed).

The structure of **documents.json** must be the following:
```json
[
{ "id": 57, "title": "...", "body": "..."},
{ "id": 368, "title": "...", "body": "..."},

]
```

**index.json** now has more information, comparing to [boolean_retrieval],
where we had only posting lists. Here it contains document_frequency for each term and term_frequency for term-document pairs.

The structure of **index.json**:
```json
{
    "museum": {
        "document_frequency": 2,
        "term_frequency": {
            "158": 1,
            "3573": 5
        }
    },
    "cooper": {
        "document_frequency": 5,
        "term_frequency": {
            "158": 2,
            "3754": 7,
            "4148": 1,
            "5522": 2,
            "5578": 1
        }
    },
    
}
```

For stemming *SnowballStemmer* from *nltk* is used.

## search
This simple search engine performs ranked retrieval of documents from **documents.json** using **index.json**.
Comparing to [boolean_retrieval], now you can type free text queries:

```
PS C:\workspace\ranked_retrieval\search> python main.py --verbose --limit=3
> word processing
score=0.2829, document_id=3182
WORD PROCESSING' AN INTRODUCTION AND APPRAISAL.

IDENTIFIES AND DESCRIBES THE FACILITIES AVAILABLE FOR MECHANISING AND AUTOMATING LIBRARY AND INFORMATION SERVICES USING WORD PROCESSING SYSTEMS-TEXT STORAGE AND SEARCHING, ORDER PROCESSING AND BUDGET CONTROL, PREPARATION OF CATALOGUES, CIRCULATION CONTROL, PERIODICALS CONTROL AND CIRCULATION, INFORMATION STORAGE AND RETRIEVAL SYSTEM USE, AND POSSIBLE FUTURE USES.

--------------------------------------------------
score=0.1365, document_id=3444
COMPUTER-ASSISTED PRODUCTION OF BIBLIOGRAPHIC DATABASES IN HISTORY.

PAPER PRESENTED AT THE 2ND INTERNATIONAL CONFERENCE ON DATA BASES IN THE HUMANITIES AND SOCIAL SCIENCES, MADRID 16-19 JUNE 80. DESCRIBES THE USE OF A COMPUTERISED TEXT PROCESSING SYSTEM TO PRODUCE PRINTED AND ON-LINE VERSIONS OF THE BIBLIOGRAPHIC DATA BASES IN HISTORY-2HISTORICAL ABSTRACTS1 AND 2AMERICA' HISTORY AND LIFE1. ABSTRACTS OR CITATIONS OF BOOKS, ARTICLES AND DISSERTATIONS ARE EDITED, SUBJECT-CLASSIFIED, AND SUBJECT AND AUTHOR-INDEXED. THE AMERICAN BIBLIOGRAPHICAL CENTER'S PROFILE INDEX IS A COMPUTER-ASSISTED, ROTATED STRING INDEX, THE VOCABULARY IS A COMBINATION OF NATURAL LANGUAGE KEY WORDS AND PREFERRED SUBJECT HEADINGS SELECTED BY EDITOR-INDEXERS. THE PROCESSING SYSTEM COMPRISES KEYBOARDING, EXTRACTION OF INDEX TERMS, EXPANSION OF ABBREVIATED INDEX TERMS TO FULL TEXT, FILE CORRECTION, SORTING AND PHOTOCOMPOSITION OF PAGES. FILES OF BIBLIOGRAPHIC ENTRIES ARE SORTED FOR USE IN 1 OR MORE DATA BASES, AND ANNUAL INDEX FILES ARE MERGED TO PRODUCT CUMULATIVE INDEXES.

--------------------------------------------------
score=0.0855, document_id=2643
AUDIO-VISUAL MATERIAL IN LIBRARY COLLECTIONS.

IN THE LAST DECADE THE DEMANDS OF SOCIETY FOR INFORMATION HAVE UNDERGONE A GREAT CHANGE. LEARNING AND SELF-EDUCATION ARE PLAYING AN INCREASINGLY GREATER PART IN THE EDUCATION PROCESS AND AUDIO-VISUAL MATERIAL IN LIBRARIES HAVE AN IMPORTANT ROLE. DESCRIBES THE ORGANISATION AND PROCESSING OF AN AUDIO-VISUAL COLLECTION AND THE SERVICES WHICH CAN BE PROVIDED.

--------------------------------------------------
```
With argument `--verbose` you can see full text of documents.
Argument `--limit` limits, how many results to show (default is 20)

### Implemenation details
For stemming again *SnowballStemmer* is used. Weighting scheme for ranked retrieval is lnc.ltc.

1. Before asking any queries the system pre-calculates term-document weights, using formula `1 + log10(term_frequency)` and normalizes it by document vector's length (for cosine similarity). It is done only for present term-document pairs from **index.json**, and results are stored in a hash-map (memory efficient, comparing to two-dimensional array) for fast future accesses. Also, inverse document frequency `idf` is computed for all terms. All pre-computations require linear time depending on the present term-document pairs from **index.json**.

2. When free text query is typed, the system computes term-query weights using formula `(1 + log10(term_frequency_in_query)) * idf(term)` and normalizes them too. It requires linear time depending on the query length. 

3. To efficiently calculate document scores term-at-a-time approach is used for query terms: 
    ```python
    for term, query_weight in term_query_weights.items():
        for document_id, document_weight in term_document_weights[term].items():
            from_document_id_to_score[document_id] += query_weight * document_weight
    ```
    Time complexity will linearly depend on number of term-document pairs (from pre-computed HashMap) for query terms.

4. Documents, are sorted by their scores (*O(N log N)*, where *N* is the number of documents, containing query terms) to show top relevant.


## Screenshots
To see working functionality, check out **Screenshots** directory
