"""
 speeches.py = imports Presidential speeches from The Miller Center at the University of Virginia
 https://data.millercenter.org/
 returns: a json file with the speech content
"""
import json, requests, sys

endpoint = "https://api.millercenter.org/speeches"
out_file = "speeches_short.json"

r = requests.post(url=endpoint)
data = r.json()
items = data['Items']

while 'LastEvaluatedKey' in data:
    parameters = {"continue_president": data['LastEvaluatedKey']['president'],
                "continue_doc_name": data['LastEvaluatedKey']['doc_name']}
    r = requests.post(url = endpoint, params = parameters)
    data = r.json()
    items += data['Items']
    print(f'{len(items)} speeches')
    if len(items) >= 100:
        break



with open(out_file, "w") as out:
    out.write(json.dumps(items))
    print(f'wrote results to file: {out_file}')