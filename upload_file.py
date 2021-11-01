import json
import keyring
import requests

def up(file_name, course_id):

    TOKEN = keyring.get_password('canvas','zzea5939')
    HEADER = {'Authorization': 'Bearer ' + TOKEN}
    URL = 'https://canvas.sydney.edu.au/api/v1'
    END = '/courses/%s/files' %(course_id)

    x = requests.post(URL+END, headers=HEADER, data={'name': file_name}).json()

    upload_url = x.get('upload_url')
    payload = x.get('upload_params')

    x = requests.post(upload_url, data=payload, files={file_name: open(file_name,'rb')}).json()

    location = x.get('location')

    x = requests.post(location, headers=HEADER).json()
    x = x.get('id')
    return(x)
