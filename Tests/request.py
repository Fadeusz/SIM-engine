import requests as reqs

response = reqs.post('https://sim.letscode.it/ajax/ApplicationLogin', {'email': 'mejl', 'password':'pass'})
print(response.text)