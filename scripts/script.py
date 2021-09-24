import json
import boto3
import string
import os
import sys

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table('alexa_solutions_table')


check = os.listdir()
test = open("scripts/test.json")
# reads the json document
qs = json.load(test)
# going into the nested list
results = qs["results"]
id_inc = 0

# looping through the results list of dictionaries to separate the items needed to be put in dynamo
for result in results:
    id_inc = id_inc + 1
    answers = result["prompt"]["answers"]
    len_ans = len(answers)
    letters = list(string.ascii_lowercase[:len_ans])
    options = dict(zip(letters, answers))
    question = result.get("question_plain")
    if question is None:
        question = result['prompt']["question"]
    item = {
        'id': id_inc,
        'question': question,
        'options': options,
        'correct': result["correct_response"]
    }
    # putting the item dictionary into my dynamo table
    response = table.put_item(Item=item)

# adds count to dynamo. count holds the number of questions in the table
table.put_item(Item={
    "id": 0,
    "count": id_inc
}
)

print("success")
