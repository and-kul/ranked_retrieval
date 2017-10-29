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
For stemming again *SnowballStemmer* is used. Weighting scheme for ranked retrieval is lnc.ltc:

1. Before asking any queries the system pre-calculates term-document weights, using formula `1 + log10(term_frequency)` and normalizes it by document vector's length (for cosine similarity). It is done only for present term-document pairs from **index.json**, and results are stored in a HashMap (memory efficient, comparing to two-dimensional array) for fast future accesses. Also, inverse document frequency `idf` is computed for all terms. All pre-computations require linear time depending on the present term-document pairs from **index.json**.

2. When free text query is typed, the system computes term-query weights using formula `(1 + log10(term_frequency_in_query)) * idf(term)` and normalizes them too. It requires linear time depending on the query length. 

3. To efficiently calculate document scores term-at-a-time approach is used for query terms: 
    ```python
    for term, query_weight in term_query_weights.items():
        for document_id, document_weight in term_document_weights[term].items():
            from_document_id_to_score[document_id] += query_weight * document_weight
    ```
    Time complexity will linearly depend on number of term-document pairs (from pre-computed HashMap) for query terms.

4. Documents, are sorted by their scores (*O(N log N)*, where *N* is the number of documents, containing query terms) to show top relevant.

## Evaluation
Test set: 100 randomly choosen documents from LISA document collection. **index_builder/documents.json** contains exactly these 100 documents.

Test query: ***information retrieval***

Manually determined relevance for this query of all 100 documents:

| document_id   | relevant?     | document_id   | relevant?     |
|---------------|---------------|---------------|---------------|
|2       | No     |27      | No     |
|158     | No     |214     | No     |
|293     | No     |**398** | **Yes**|
|426     | No     |440     | No     |
|473     | No     |703     | No     |
|811     | No     |951     | No     |
|953     | No     |1019    | No     |
|1020    | No     |1088    | No     |
|1089    | No     |1160    | No     |
|1238    | No     |1305    | No     |
|1319    | No     |1461    | No     |
|1489    | No     |1491    | No     |
|1625    | No     |1675    | No     |
|1709    | No     |1734    | No     |
|**1789**| **Yes**|1830    | No     |
|1854    | No     |1900    | No     |
|1912    | No     |2151    | No     |
|2257    | No     |2311    | No     |
|2359    | No     |2384    | No     |
|2458    | No     |2487    | No     |
|2493    | No     |2507    | No     |
|2525    | No     |2643    | No     |
|2668    | No     |2685    | No     |
|**2789**| **Yes**|**2790**| **Yes**|
|2795    | No     |2808    | No     |
|2843    | No     |**2882**| **Yes**|
|2883    | No     |2981    | No     |
|3066    | No     |3182    | No     |
|3187    | No     |3258    | No     |
|**3388**| **Yes**|3441    | No     |
|3444    | No     |3511    | No     |
|3573    | No     |3586    | No     |
|3748    | No     |3754    | No     |
|3814    | No     |**3910**| **Yes**|
|3955    | No     |4019    | No     |
|4034    | No     |4046    | No     |
|4117    | No     |4148    | No     |
|4231    | No     |4249    | No     |
|4369    | No     |4445    | No     |
|4534    | No     |4535    | No     |
|4554    | No     |4747    | No     |
|4767    | No     |4914    | No     |
|4918    | No     |4941    | No     |
|5023    | No     |5081    | No     |
|5300    | No     |5421    | No     |
|5456    | No     |5522    | No     |
|5578    | No     |5661    | No     |
|5711    | No     |5803    | No     |
|5840    | No     |5968    | No     |
|5971    | No     |5990    | No     |

Let's test the system:

```
PS C:\workspace\ranked_retrieval\search> python main.py --limit 20
> information retrieval
score=0.3585, document_id=1789 <- relevant
score=0.3412, document_id=2790 <- relevant
score=0.3352, document_id=3388 <- relevant
score=0.3332, document_id=398  <- relevant
score=0.3196, document_id=2882 <- relevant
score=0.3021, document_id=2789 <- relevant
score=0.2221, document_id=3182
score=0.1807, document_id=3814
score=0.1798, document_id=5990
score=0.1661, document_id=3910 <- relevant
score=0.1558, document_id=4369
score=0.1517, document_id=5803
score=0.0874, document_id=3258
score=0.0847, document_id=1734
score=0.0831, document_id=3748
score=0.0797, document_id=4747
score=0.0783, document_id=2151
score=0.0773, document_id=2257
score=0.0746, document_id=4046
score=0.0728, document_id=3511
```

It has found all relevant documents.

### Metrics on top 20

Confusion matrix:

| | |
|-|-|
|7| 0 |
|13| 80 |

* *Precision = 7 / 20 = 0.35*
* *Recall = 7 / 7 = 1*
* *F1 Score = 2 * (Precision * Recall) / (Precision + Recall) = 0.519*

## Screenshots
To see working functionality, check out **Screenshots** directory
