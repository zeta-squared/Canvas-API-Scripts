import json
import requests
import keyring
import sys

TOKEN = keyring.get_password('canvas','<username>')
HEADER = {'Authorization': 'Bearer ' + TOKEN}
URL = 'https://canvas.sydney.edu.au/api/v1'

course_id = sys.argv[1]
quiz_title = sys.argv[2]
quiz_type = sys.argv[3]

quiz = {}
quiz['quiz[title]'] = '%s' %(quiz_title)
quiz['quiz[quiz_type]'] = '%s' %(quiz_type)

END = '/courses/%s/quizzes' %(course_id)

x = requests.post(URL + END, headers=HEADER, data=quiz )

x = x.json()
y = {x.get('id'),x.get('title')}
print(y)
