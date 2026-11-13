from fastapi import FastAPI,HTTPException,Header,Body
from fastapi.middleware.cors import CORSMiddleware

import function

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/package")
def register_package(p: function.PackageIn, token=Header(None)):
    username = function.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")
    return function.register_package(p.name, p.destination, p.weight, p.arrival_date, p.status)

@app.get("/package/{id}")
def get_package(id,token=Header(None)):
    username = function.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")
    return function.get_package(id)

@app.get("/package")
def search(destination=None,status=None,arrival_date=None,token=Header(None)):
    username = function.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")
    return function.search_pack(destination,status,arrival_date)

@app.patch("/package/{id}")
def update_package(id: int,u: function.PackageUpdate,token=Header(None)):
    username = function.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")
    return function.update_pack(id=id,name=u.name,destination=u.destination,weight=u.weight,arrival_date=u.arrival_date,status=u.status)

# @app.post("/package")
# def register_package(name,destination,weight:int,arrival_date,status,token=Header(None)):
#     username = function.verify_token(token=token,token_type="access")
#     if not username:
#         raise HTTPException(status_code=401,detail="Invalid or Expired token")
#     return function.register_package(name=name,destination=destination,weight=weight,arrival_date=arrival_date,status=status)
    

@app.delete("/package/{id}")
def delete_package(id:int,token=Header(None)):
    username = function.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")
    return function.delete_package(id)

@app.get("/dispatch")
def get_batch(destination=None,vehicle=None,dstatus=None,token=Header(None)):
    username = function.verify_token(token=token,token_type="access")
    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")
    return function.get_batch(destination=destination,vehicle=vehicle,dstatus=dstatus)

@app.get("/Package_Stats")
def get_stats(token=Header(None)):
    username = function.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return function.get_package_stats()  

@app.post("/dispatch")
def add_dispatch(d:function.DispatchIn,token=Header(None)):
    username = function.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return function.add_dispatch(d.vehicle,d.destination,d.dstatus,d.package_id)

@app.post("/login")
def login(username = Body(),password = Body()):
    token=function.verify_login(username=username,password=password)
    if not token:
        raise HTTPException(status_code=401,detail="Accees denied")
    return token


@app.post("/refresh")
def refresh(refresh_token=Header(None)):
    username=function.verify_token(token=refresh_token,token_type="refresh")
    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired refresh token")
    access_token=function.creat_token(username=username,token_type="access")
    return {"access_token":access_token}


@app.post("/register")
def registar_user(username=Body(),password=Body(),user_type=Body()):
    if function.register_user(username=username,password=password,user_type=user_type):
        return {"messege":"User registored successful"}
    raise HTTPException(status_code=400,detail="User_Name alreday exists")
    