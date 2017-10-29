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


For stemming again *SnowballStemmer* is used.

## Screenshots
To see working functionality, check out **Screenshots** directory
