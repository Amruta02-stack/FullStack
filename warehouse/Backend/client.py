# import requests 

# URL=("http://127.0.0.1:8001")
# user_credential1={"username":"Am","user_type":"dispatcher","password":"7852"}
# user_credential={"username":"Amruta","user_type":"manager","password":"7852"}

# querys={"destination":"bangalore","status":"dispatched","arrival_date":"null"}
# packages={
#   "name": "python",
#   "destination": "japan",
#   "weight": 2,
#   "arrival_date": "2026-11-22",
#   "status": "dispatched"
# }

# response = requests.post(url=URL+"/register",json=user_credential)
# print(response.json())

# response=requests.post(url=URL+"/login",json=user_credential1)
# response_json=response.json()
# access_token=response_json["access_token"]
# refresh_token=response_json["refresh_token"]

# print(access_token)

# header={"token":access_token}

# response=requests.get(url=URL+"/package/6",headers=header)
# print(response.json())

# response=requests.post(url=URL+"/registerpackage",json=packages,headers=header)
# print(response.json())


# id=6
# response=requests.delete(url=URL+f"/package/{id}",headers=header)
# print(response.json())

# response=requests.patch(url=URL+f"/package/{id}",json=packages,headers=header)
# print(response.json())


# destination={"destination":"mysore","status":"null","arrival_date":"null"}
# response=requests.get(url=URL+"/search?destination=mysore",headers=header)
# print(response.json())

# response=requests.get(url=URL+"/dispatch?destination=delhi",headers=header)
# print(response.json())

# response=requests.get(url=URL+"/Package_Stats",headers=header)
# print(response.json())
