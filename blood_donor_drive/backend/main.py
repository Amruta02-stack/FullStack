from fastapi import FastAPI, HTTPException,Header,Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
import AM_functions as a
import SU_functions
import NA_functions
from typing import Optional
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
def register(u:a.UserIn):
    if a.register_user(username=u.username,user_type=u.user_type.lower(),password=u.password):
        return{"message":"user registered successfully"}
    raise HTTPException(status_code=400,detail="Username alreday exists")

@app.post("/login")
def login(username=Body(),password=Body()):
    token=a.verify_login(username=username,password=password)
    if not token:
        raise HTTPException(status_code=401,detail="Access denied")
    return token

@app.post("/refresh")
def refresh_token(refresh_token=Header(None)):
    payload=a.verify_token(token=refresh_token,token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401,detail="Invaild or token expired")
    access_token=a.creat_token(username=payload["username"],user_type=payload["user_type"],token_type="access")
    return {"access_token":access_token}

#E1 GET all donors
@app.get("/donors")
def donors(blood_group:Optional[str]=None,token=Header(None)):
    payload=a.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invaild or expired Token")
    if payload["user_type"] !="manager":
        raise HTTPException(status_code=403,detail="Forbidden request for the user")
    return SU_functions.get_all_donors(blood_group=blood_group)

#E8 GET eligible donors by blood group
@app.get("/donors/eligible")                              
def get_eligible_donors(blood_group,token=Header(None)): 
    payload=a.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invaild or expired Token")
    if payload["user_type"] !="manager":
        raise HTTPException(status_code=403,detail="Forbidden request for the user")
    response = NA_functions.get_eligible_donors(blood_group)
    return response


#E2 GET DONORS by roll number
@app.get("/donors/{roll_no}")
def get_donor(roll_no: str,token=Header(None)):
    payload=a.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invaild or expired Token")
    return SU_functions.get_donor(roll_no.upper())

#E3 Add donor
@app.post("/donors")
def add_donor(d:a.DonorIn,token=Header(None)):
    payload=a.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invaild or expired Token")
    return SU_functions.add_donor(roll_no=d.roll_no, name=d.name, blood_group=d.blood_group, weight_kg=d.weight_kg,last_donated_on=d.last_donated_on)

#E4 Book appointment
@app.post("/appointments")
def book_appoint(appoint:a.AppoinmentIn,token=Header(None)):
    payload=a.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invaild or expired Token")
    return a.book_appoint(appoint.roll_no.upper(), appoint.drive_date, appoint.slot.lower())

#E5 Cancel appointment
@app.patch("/appointments/{id}/cancel")
def cancel_appoint(id:int,token=Header(None)):
    payload=a.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or Expired Token")
    return a.cancel_appoint(id)

#E6 Mark appointment
@app.patch("/appointments/{id}/status")
def mark_appoint(id:int, s:a.MarkIn,token=Header(None)):
    payload=a.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or Expired Token")
    if payload["user_type"] != "manager":
        raise HTTPException(status_code=403,detail="Forbidden for your role")
    return a.mark_appoint(id, s.status.lower())

#E7 GET appointments by date
@app.get("/appointments") 
def get_appointments(drive_date:date,token=Header(None)):
    payload=a.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or expired Token")
    if payload["user_type"]!= "manager":
        raise HTTPException(status_code=403,detail="Forbidden for your role")
    response = NA_functions.get_appointments_by_date(drive_date)
    return response 

#E9 GET units donated by blood group
@app.get("/appointments/status/units")                                         
def get_units(token=Header(None)):
    payload=a.verify_token(token=token,token_type="access")
    if not payload:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")
    if payload["user_type"]!="manager":
        raise HTTPException(status_code=403,detail="Forbidden for your role")
    
    return NA_functions.get_units()