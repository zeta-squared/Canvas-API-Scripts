import json
import requests
import keyring
import sys

TOKEN = keyring.get_password('canvas','<username>')
HEADER = {'Authorization': 'Bearer ' + TOKEN}
URL = 'https://canvas.sydney.edu.au/api/v1'

course_id = sys.argv[1]
quiz_id = sys.argv[2]

END = '/courses/%s/quizzes/%s' %(course_id, quiz_id)

x = requests.delete(URL+END, headers=HEADER, data={})

print(x)
