"""
Parsers to support the Un_res Framework
"""
import string
import re
import json
from collections import Counter


def recursion_lower(x):
    """ this code is from https://stackoverflow.com/questions/69194607/lowercase-all-the-letters-in-json"""
    if type(x) is str:
        return x.lower()
    elif type(x) is list:
        return [recursion_lower(i) for i in x]
    elif type(x) is dict:
        return {recursion_lower(k):recursion_lower(v) for k,v in x.items()}
    else:
        return x

def load_stop_words():
        # remove stop words
        # load the stopwords
    with open("stopwords.txt", "r") as stopwords:
        lines = stopwords.readlines()
            # put the stopwords to a list
        stop_words_list = []
            # remove commas and \n s from the stopwords.txt file
        for l in lines:
            as_list = l.split(", ")
            stop_words_list.append(as_list[0].replace("\n", ""))
        # return the list (will be used in the parser
    return stop_words_list

def json_parser(filename):
    f = open(filename)
    raw = json.load(f)
    #labels = raw['nation']
    text = raw['body_en']
    # removing line breaks that occur in downloaded json files
    del_line_breaks_text = re.sub('\n', ' ', text)
    # removing all non letter characters
    cleaned_text = re.sub('[^a-zA-Z\s]', '', del_line_breaks_text)

    # removing all uppercase letters
    new_data = recursion_lower(cleaned_text)
    # same data.split from class notes json_parser on new data
    new_data = new_data.split(" ")
    # remove all stop words
    stop_list = load_stop_words()
    new_data = [item for item in new_data if item not in stop_list]

    wc = Counter(new_data)
    wc_top5 = Counter(new_data).most_common(5)
    num = len(wc)
    f.close()
    return {'wordcount': wc, 'numwords':num, 'top5':wc_top5, 'paragraph':del_line_breaks_text}
