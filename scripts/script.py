import json
import boto3
import string
from bs4 import BeautifulSoup

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table('alexasolutionsquiz')

test = open("test.json")
test2 = open("test2.json")
test3 = open("test3.json")
test4 = open("test4.json")
test5= open("test5.json")
#reads the json document
qs = json.load(test)
#going into the nested list 
results = qs["results"]
id_inc = 0

#looping through the results list of dictionaries to separate the items needed to be put in dynamo 
for result in results + results2 + results3 + results4 + results5:
    id_inc = id_inc + 1
    answers = result["prompt"]["answers"]
    len_ans= len(answers)
    letters = list(string.ascii_lowercase[:len_ans])
    options = dict(zip(letters,answers))
    item ={
        'id': id_inc,
        'question':(result["question_plain"]),
        'options':options,
        'correct':result["correct_response"]
    }
    #putting the item dictionary into my dynamo table
    response = table.put_item(Item=item)

#adds count to dynamo. count holds the number of questions in the table   
table.put_item(Item={
    "id":0,
"count":id_inc
}
)




