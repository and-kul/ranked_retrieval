import argparse
import json
import string

from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

DEFAULT_DOCUMENTS_JSON = r"./documents.json"
DEFAULT_INDEX_JSON = r"./index.json"


def main():
    parser = argparse.ArgumentParser(description="builds an index file for documents")
    parser.add_argument("--input",
                        help='path to json with documents, default="' + DEFAULT_DOCUMENTS_JSON + '"',
                        default=DEFAULT_DOCUMENTS_JSON)
    parser.add_argument("--output",
                        help='where to store json with index, default="' + DEFAULT_INDEX_JSON + '"',
                        default=DEFAULT_INDEX_JSON)
    args = parser.parse_args()


    with open(args.input, "r") as json_file:
        documents = json.load(json_file)

    stemmer = SnowballStemmer("english")
    index = dict()

    for document in documents:
        text = document["title"] + " " + document["body"]

        # without punctuation tokens
        raw_tokens = [token for token in word_tokenize(text) if token not in string.punctuation]

        terms = [stemmer.stem(token) for token in raw_tokens]

        # from term to term frequency for the current document
        from_term_to_term_frequency = defaultdict(int)

        for term in terms:
            from_term_to_term_frequency[term] += 1

        for term, term_frequency in from_term_to_term_frequency.items():
            if term not in index:
                index[term] = {
                    "document_frequency": 0,
                    "term_frequency": {}
                }

            term_info = index[term]
            term_info["document_frequency"] += 1
            term_info["term_frequency"][document["id"]] = term_frequency
        pass

    with open(args.output, "wt") as index_json_file:
        json.dump(index, index_json_file)
    exit(0)


if __name__ == '__main__':
    main()
