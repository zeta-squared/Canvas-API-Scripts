import sys
import json
import parse
import keyring
import requests

TOKEN = keyring.get_password('canvas','<username>')
HEADER = {'Authorization': 'Bearer ' + TOKEN}
URL = 'https://canvas.sydney.edu.au/api/v1'

file = sys.argv[1]
course_id = sys.argv[2]
quiz_id = sys.argv[3]

q_data = parse.build(file)

for i in range(0,len(q_data)):
    END = '/courses/%s/quizzes/%s/questions' %(course_id, quiz_id)
    x = requests.post(URL+END, headers=HEADER, data=q_data[i])
    print(x)
