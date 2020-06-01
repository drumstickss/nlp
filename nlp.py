import io, os
import re as re
import zipfile as zipfile
import math

stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "'s"]

puncs = ["!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<",
         "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", ",", ". "]

query_result = {}
data = {}
dict_search = {}

def tokenizer(textfile):
    token = re.compile("[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\\w\\-]+")
    return re.findall(token, textfile)


def turn_lower(tokenized_words):
    return [item.lower() for item in tokenized_words]


def remove_pun(lower_tokenized_words):
    for word in lower_tokenized_words:
        if word in puncs:
            lower_tokenized_words.remove(word)
    return  lower_tokenized_words


def remove_stopwords(lower_tokenized_nonpunc_words):
    final_words = []
    for word in lower_tokenized_nonpunc_words:
        if word not in stop_words:
            final_words.append(word)
    return final_words


def all_things(file):
    result = tokenizer(file)
    result1 = turn_lower(result)
    result2 = remove_pun(result1)
    result3 = remove_stopwords(result2)
    return  result3


def read_file():
    i = 1

    with zipfile.ZipFile('30Columnists.zip') as z:
        for zipinfo in z.infolist():
            if zipinfo.filename.endswith('.txt') and re.search('raw_texts', zipinfo.filename):
                with z.open(zipinfo) as f:
                    textfile = io.TextIOWrapper(f, encoding='cp1254', newline='')
                    temp_file = textfile.read()
                    formated_file = all_things(temp_file)
                    index(str(i), formated_file)
                    i +=1


def index(file_id, file_array):

    if file_id not in data:
        data[file_id] = {}

    for word in file_array:
        if word not in data[file_id]:
            data[file_id][word] = 1
        else:
            data[file_id][word] += 1



def search(query):
    label = 1
    while label <= data.__len__():

        if query in data[str(label)]:
            dict_search[label] = data[str(label)][str(query)]
        label += 1



def search_two_query(q1, q2):
    label = 1
    while label <= data.__len__():

        if q1 in data[str(label)]:

            if q2 in data[str(label)]:
                query_all = { q1: data[str(label)][str(q1)], q2: data[str(label)][str(q2)] }
                query_result[label] = query_all

        label += 1



read_file()
search_two_query("obama", "hate")
print("These queries found in '"+ str(len(query_result)) + "' documents.")
for k, v in query_result.items():
    print("document no: ",k,"-",v)
