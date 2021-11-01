import json
import requests
import keyring

TOKEN = keyring.get_password('canvas','<username>')
HEADER = {'Authorization': 'Bearer ' + TOKEN}
URL = "https://canvas.sydney.edu.au/api/v1"

x = requests.get(URL + "/courses", headers=HEADER, data={})

x = x.json()
i = 0
y = [None]*len(x)
while i <= len(x)-1:
    y[i] = {'id': x[i].get('id'), 'name': x[i].get('name'), 'workflow_state': x[i].get('workflow_state')}
    i += 1

y = json.dumps(y, indent=2)
print(y)
