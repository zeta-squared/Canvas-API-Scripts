import json
import keyring
import requests

def questionlist(course_id, quiz_id):
    TOKEN = keyring.get_password('canvas','<username>')
    HEADER = {'Authorization': 'Bearer ' + TOKEN}
    URL = "https://canvas.sydney.edu.au/api/v1/courses/%s/quizzes/%s/questions" %(course_id, quiz_id,)
    x = requests.get(URL, headers=HEADER, data={})
    x = x.json()
    i = 0
    y = [None]*len(x)
    while i <= len(x)-1:
        y[i] = x[i].get('id')
        i += 1
    return y
