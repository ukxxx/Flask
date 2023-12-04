import requests

response = requests.post('http://127.0.0.1:8080/hello?name=John&age=20',
                         json={"name": "user1", "password": "1234"},
                         headers={"token": "egdfgsgasdfafadf"}
                         )
print(response.text)
print(response.status_code)