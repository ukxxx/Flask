import requests

# POST ADVERT
response = requests.post(
    "http://127.0.0.1:8080/advert",
    json={"name": "Cat", "description": "Fluffy, calm", "owner_id": "18"},
)
print(response.text)
print(response.status_code)


# # PATCH ADVERT
# response = requests.patch('http://127.0.0.1:8080/advert/5',
#                           json={"name": "Cat", "description": "Diabolic", "owner_id": "21"})
# print(response.text)
# print(response.status_code)


# DELETE ADVERT
response = requests.delete("http://127.0.0.1:8080/advert/6", json={"owner_id": "18"})
print(response.text)
print(response.status_code)


# # GET ADVERT
# response = requests.get(
#     "http://127.0.0.1:8080/advert/1",
# )
# print(response.text)
# print(response.status_code)


# # POST USER
# response = requests.post('http://127.0.0.1:8080/user',
#                         json={"mail": "John@ringto.to", "password": "sfgfsgdfsgdfsgfsdgf"},
#                         )
# print(response.text)
# print(response.status_code)


# # GET USER
# response = requests.get(
#     "http://127.0.0.1:8080/user/15",
# )
# print(response.text)
# print(response.status_code)


# # DELETE USER
# response = requests.delete(
#     "http://127.0.0.1:8080/user/15",
# )
# print(response.text)
# print(response.status_code)
