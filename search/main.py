import argparse
import json
import string
from collections import defaultdict
from typing import List

import math
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer

DEFAULT_DOCUMENTS_JSON = r"../index_builder/documents.json"
DEFAULT_INDEX_JSON = r"./index.json"

stemmer = SnowballStemmer("english")


def get_term_weights_for_query(query: str, idf: dict) -> dict:
    # without punctuation tokens
    raw_query_tokens = [token for token in word_tokenize(query) if token not in string.punctuation]

    query_terms = [stemmer.stem(token) for token in raw_query_tokens]

    result = defaultdict(int)
    for term in query_terms:
        result[term] += 1

    for term in result:
        result[term] = (1 + math.log10(result[term])) * (idf.get(term, 0))

    vector_length = 0
    for weight in result.values():
        vector_length += weight ** 2
    vector_length = math.sqrt(vector_length)

    # normalization
    for term in result:
        result[term] /= vector_length

    return result


def main():
    parser = argparse.ArgumentParser(description="search documents for specified queries")
    parser.add_argument("--documents",
                        help='path to json with documents, default="' + DEFAULT_DOCUMENTS_JSON + '"',
                        default=DEFAULT_DOCUMENTS_JSON)
    parser.add_argument("--index",
                        help='path to json with index, default="' + DEFAULT_INDEX_JSON + '"',
                        default=DEFAULT_INDEX_JSON)
    parser.add_argument("-v", "--verbose", help="show full text of documents",
                        action="store_true")
    parser.add_argument("-l", "--limit", help="specify, how many documents to show, default=20",
                        type=int,
                        default=20)
    args = parser.parse_args()


    with open(args.documents, "r") as json_file:
        documents_list = json.load(json_file)

    documents_count = len(documents_list)

    all_documents = {
        int(document["id"]):
            {
                "title": document["title"],
                "body": document["body"]
            }
        for document in documents_list}


    with open(args.index, "r") as json_file:
        index = json.load(json_file)


    # from document_id to document's vector length (normalization factor)
    document_length = defaultdict(int)

    idf = dict()
    term_document_weights = defaultdict(dict)

    for term, term_info in index.items():
        idf[term] = math.log10(documents_count / term_info["document_frequency"])
        for document_id, tf in term_info["term_frequency"].items():
            weight = 1 + math.log10(tf)
            term_document_weights[term][document_id] = weight
            document_length[document_id] += weight ** 2

    for document_id in document_length:
        document_length[document_id] = math.sqrt(document_length[document_id])


    # normalization
    for term in term_document_weights:
        for document_id in term_document_weights[term]:
            term_document_weights[term][document_id] /= document_length[document_id]


    query = input("> ")

    term_query_weights = get_term_weights_for_query(query, idf)

    from_document_id_to_score = defaultdict(int)

    for term, query_weight in term_query_weights.items():
        for document_id, document_weight in term_document_weights[term].items():
            from_document_id_to_score[document_id] += query_weight * document_weight

    document_score_pairs = [(document_id, score) for document_id, score in from_document_id_to_score.items()]

    document_score_pairs.sort(key=lambda pair: pair[1], reverse=True)

    for pair in document_score_pairs[:args.limit]:
        document_id = int(pair[0])
        score = pair[1]
        title = all_documents[document_id]["title"]
        body = all_documents[document_id]["body"]

        print("score={0:.4f}, document_id={1}".format(score, document_id))
        if args.verbose:
            print(title)
            print()
            print(body)
            print()
            print("-" * 50)

    return


if __name__ == '__main__':
    main()
