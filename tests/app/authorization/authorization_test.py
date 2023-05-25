import os
import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# définition de l'adresse de l'API
api_address = "51.77.222.243"  # os.environ.get('API_ADDRESS')

# port de l'API
api_port = "8000"  # os.environ.get('API_PORT')

response = []

users = [
    {'username': 'alice', 'password': 'wonderland', 'right': 'market'},
    {'username': 'bob', 'password': 'builder', 'right': 'fundamental'},
    {'username': 'damien', 'password': 'vannetzel', 'right': 'admin'},
]

for user in users:
    r = requests.get(
        url='https://{address}:{port}/admin'.format(address=api_address, port=api_port),
        auth=HTTPBasicAuth(user['username'], user['password']),
        verify=False  # Ignore SSL verification
    )
    response.append([user['username'], user['right'], r])

output = '''
============================
    Authorization test
============================

request done at "/admin"
username = {username}
rights = {right}
expected result = 200
actual result = {status_code}

==>  {test_status}

'''

for combo in response:
    username = combo[0]
    right = combo[1]
    r = combo[2]

    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == 200:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    print(output.format(status_code=status_code, test_status=test_status, username=username, right=right))

    # impression dans un fichier
    if os.environ.get('LOG') == "1":
        with open('/logs/api_test.log', 'a') as file:
            file.write(output.format(status_code=status_code, test_status=test_status, username=username, right=right))
