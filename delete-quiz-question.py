import sys
import json
import keyring
import requests
import questiongenerator as qg

TOKEN = keyring.get_password('canvas','<username>')
HEADER = {'Authorization': 'Bearer ' + TOKEN}
URL = 'https://canvas.sydney.edu.au/api/v1'

course_id = sys.argv[1]
quiz_id = sys.argv[2]
option = sys.argv[3]

if option == 'all':
    id_list = qg.questionlist(course_id, quiz_id)
    for i in range(0,len(id_list)):
        END = '/courses/%s/quizzes/%s/questions/%s' %(course_id, quiz_id, id_list[i])
        x = requests.delete(URL+END, headers=HEADER, data={})
        print(x)
else:
    option = option.split(',')
    for i in range(0,len(option)):
        END = '/courses/%s/quizzes/%s/questions/%s' %(course_id, quiz_id, option[i])
        x = requests.delete(URL+END, headers=HEADER, data={})
        print(x)
