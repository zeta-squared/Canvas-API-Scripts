import json
import requests
import keyring
import sys

TOKEN = keyring.get_password('canvas','<username>')
HEADER = {'Authorization': 'Bearer ' + TOKEN}
URL = "https://canvas.sydney.edu.au/api/v1"

course_id = sys.argv[1]
quiz_id = sys.argv[2]
detail = sys.argv[3]

END = '/courses/%s/quizzes/%s/questions' %(course_id, quiz_id)

x = requests.get(URL+END, headers=HEADER, data={})

if detail == 'all':
    x = x.json()
    x = json.dumps(x, indent=2)
    print(x)
elif detail == 'id':
    x = x.json()
    i = 0
    y = [None]*len(x)
    while i <= len(x)-1:
        y[i] = x[i].get('id')
        i += 1
    y = json.dumps(y, indent=2)
    print(y)
else:
    x = x.json()
    i = 0
    y = {}
    while i <= len(x)-1:
        y[x[i].get('id')] = (x[i].get('question_name'), x[i].get('question_text'))
        i += 1
    y = json.dumps(y, indent=2)
    print(y)
