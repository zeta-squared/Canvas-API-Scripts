import sys
import json
import keyring
import requests

TOKEN = keyring.get_password('canvas','<username>')
HEADER = {'Authorization': 'Bearer ' + TOKEN}
URL = "https://canvas.sydney.edu.au/api/v1"

course_id = sys.argv[1]

END = "/courses/%s/quizzes" %(course_id)
x = requests.get(URL+END, headers=HEADER, data={})

x = x.json()
i = 0
y = {}
while i <= len(x)-1:
    y[x[i].get('id')] = (x[i].get('title'))
    i += 1

y = json.dumps(y, indent=2)
print(y)
