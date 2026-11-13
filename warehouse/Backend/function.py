#Token JWT
#hashing to encode the password in the DB "Salt" will make sure that different ppl will have different code

from sqlalchemy import create_engine,Integer,String,Date,Column,ForeignKey
from sqlalchemy.orm import Session,declarative_base
from fastapi import FastAPI,HTTPException
from datetime import date,datetime,timedelta,timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel,Field
from typing import Optional

ph=PasswordHasher()

DB_PATH = "warehouse.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

# USERNAME="12345"
# PASSWORD="PASS"
ACCEESS_TOKEN_EXPIRY=5
REFRESH_TOKEN_EXPIRY=7*24*60
SECRET_KEY="SECRET321"
ALGORITHM="HS256"



class PackageIn(BaseModel):
    name: str
    destination: str
    weight: int=Field(gt=0)
    arrival_date: date
    status: str

class PackageUpdate(BaseModel):
    name: Optional[str] = None
    destination: Optional[str] = None
    weight: Optional[int] = Field(default=None, gt=0)
    arrival_date: Optional[date] = None
    status: Optional[str] = None 

class DispatchIn(BaseModel):
    vehicle: str
    destination: str
    dstatus: str
    package_ids: list[int]=Field(min_length=1)


        

class User(Base):
    __tablename__="User"

    user_id=Column(Integer,primary_key=True)
    user_type=Column(String)
    username=Column(String)
    password=Column(String)
    
class Package(Base):
    __tablename__ = "Package"

    id = Column(Integer,primary_key= True)
    name=Column(String) 
    destination = Column(String)
    weight = Column(Integer)
    arrival_date=Column(Date)
    status = Column(String)
    d_id=Column(Integer,ForeignKey("Dispatch.id"),nullable=True)

class Dispatch(Base):
        __tablename__ = "Dispatch"
        id = Column(Integer,primary_key= True)
        vehicle = Column(String)
        destination = Column(String)
        dstatus=Column(String)
       

Base.metadata.create_all(engine)

def seed_data():
    session=Session(engine)
    today = date.today()
    if session.query(Dispatch).count() ==0:
        dispatch_record = [
            Dispatch(id=1,vehicle="KA-23-9032",destination="mysore",dstatus="in-transit"),
            Dispatch(id=2,vehicle="MH-03-5432",destination="kashmir",dstatus="created"),  
            Dispatch(id=3,vehicle="DH-01-2463",destination="delhi",dstatus="delivered"),
        ]
        session.add_all(dispatch_record)
        session.commit()
    if session.query(Package).count() == 0:
        package_record=[
         Package(id=1,name="earbud",destination="bangalore",weight=2,arrival_date=today-timedelta(1),status="pending",),
         Package(id=2,name="Steel Bottel",destination="bangalore",weight=5,arrival_date=today-timedelta(1),status="pending"),
         Package(id=3,name="Face Cream",destination="mysore",weight=5,arrival_date=today-timedelta(2),status="dispatched",d_id=1),
         Package(id=4,name="Toy Car",destination="kashmir",weight=2,arrival_date=today,status="dispatched",d_id=2),
         Package(id=5,name="Pen",destination="delhi",weight=7,arrival_date=today-timedelta(5),status="dispatched",d_id=3),
         Package(id=6,name="Laptop",destination="delhi",weight=5,arrival_date=today-timedelta(3),status="pending"),
        ]
        session.add_all(package_record)
        session.commit()

    session.close()

seed_data()



def get_package(id):
    session = Session(engine)
    package=session.get(Package,id)
    if package is None:
         session.close()
         raise HTTPException(status_code=404,detail="Package not found")
    
    response={
            "id":package.id,
            "name":package.name,
            "destination":package.destination,
            "weight":package.weight,
            "arrival_date":package.arrival_date,
            "status":package.status,
           }

    session.close()
    return response   

def register_package(name,destination,weight,arrival_date,status):
    destination=destination.lower()
    status=status.lower()
    session=Session(engine)
    package=Package(name=name,destination=destination,weight=weight,arrival_date=arrival_date,status=status)
    session.add(package)
    session.commit()
    response={
                "id":package.id,
                "name":package.name,
                "destination":package.destination,
                "weight":package.weight,
                "arrival_date":package.arrival_date,
                "status":package.status,
            }
    session.close()
    return response

def update_pack(id,name=None,destination=None,weight=None,arrival_date=None,status=None):
    
    session=Session(engine)
    
    package=session.get(Package,id)
    if package is None:
         session.close()
         raise HTTPException(status_code=404,detail="Package Not Found")
    if name is not None:
        package.name=name
    if destination is not None:    
        package.destination=destination.lower()
    if weight is not None:    
        package.weight=weight
    if arrival_date is not None:
        package.arrival_date=arrival_date   
    if status is not None:    
        package.status=status.lower()
    
    session.commit()

    response={
        "id":package.id,
        "name":package.name,
        "destination":package.destination,
        "weight":package.weight,
        "arrival_date":package.arrival_date,
        "status":package.status,
    }
    session.close()
    return response


def delete_package(id):
    session=Session(engine)
    package=session.get(Package,id)
    if package is None:
          session.close()
          raise HTTPException(status_code=404,detail="Package Not Found")
    if package.status != "dispatched":
        response={
                "id":package.id,
                "name":package.name,
                "destination":package.destination,
                "weight":package.weight,
                "arrival_date":package.arrival_date,
                "status":package.status,
            }
        session.delete(package)
        session.commit()
        session.close()
        return response
    session.close()
    raise HTTPException(status_code=409,detail="alreday dispatched")


def search_pack(destination,status,arrival_date):
  
    session=Session(engine)
    
    packages=session.query(Package).all()       
    response=[]
    for package in packages:
        if ((destination is None or package.destination==destination.lower()) and 
            (status is None or package.status==status.lower()) and 
            (arrival_date is None or package.arrival_date==arrival_date)):  
            res={
                    "id":package.id,
                    "name":package.name,
                    "destination":package.destination,
                    "weight":package.weight,
                    "arrival_date":package.arrival_date,
                    "status":package.status,
                    }
            response.append(res)
            
    session.close()
    return response

def get_batch(destination=None,vehicle=None,dstatus=None):
    session=Session(engine)

    dispatchs=session.query(Dispatch).all()       
    response=[]
    for dispatch in dispatchs:
        id=[]
        packs=session.query(Package).filter(Package.d_id==dispatch.id).all()
        for p in packs:
            id.append(p.id)
        if ((destination is None or dispatch.destination==destination.lower()) and 
                (dstatus is None or dispatch.dstatus==dstatus.lower()) and 
                (vehicle is None or dispatch.vehicle==vehicle)):
            res={
                 "id":dispatch.id,
                 "vehicle":dispatch.vehicle,
                "destination":dispatch.destination,
                "dstatus":dispatch.dstatus,
                "Package_id":id,
            }   
            response.append(res)
    session.close()
    return response

def get_package_stats():
    session=Session(engine)
    total_pack=session.query(Package).count()
    pending=session.query(Package).filter(Package.status=="pending").count()
    dispatched=session.query(Package).filter(Package.status=="dispatched").count()
    counts = {}
    packages = session.query(Package).all()
    for package in packages:
        if package.destination in counts:
            counts[package.destination] = counts[package.destination] + 1
        else:
            counts[package.destination] = 1
    session.close()
    responce={
        "total_Package":total_pack,
        "Pending_Package":pending,
        "Dispatched_Package":dispatched,
        "Destination_count":counts
    }
    return responce

def add_dispatch(vehicle,destination,dstatus,package_ids):
    destination=destination.lower()
    dstatus=dstatus.lower()
    session=Session(engine)
    for p_id in package_ids:
        package=session.get(Package,p_id)
        if package is None:
            session.close()
            raise HTTPException(status_code=404,detail="Package not found")
        if package.status == "dispatched":
            session.close()
            raise HTTPException(status_code=409,detail="Package already dispatched")
        if package.destination!= destination:
            session.close()
            raise HTTPException(status_code=400,detail="bad request destination")

    dispatch=Dispatch(vehicle=vehicle ,destination=destination,dstatus=dstatus)
    session.add(dispatch)
    session.commit()  

    for p_id in package_ids:
        package=session.get(Package,p_id)
        package.d_id=dispatch.id
        package.status="dispatched"
    session.commit()       
    response={
        "id":dispatch.id,
        "vehicle":dispatch.vehicle,
        "destination":dispatch.destination,
        "dstatus":dispatch.dstatus,
        "package_id":package_ids
    }  
    session.close()
    return response


def verify_login(username,password):
    session=Session(engine)
    user=session.query(User).filter_by(username=username).first()
    if user is None:
        session.close()
        return False
    try:
        ph.verify(user.password,password)
    except VerifyMismatchError:
        session.close()
        return False
    
    access_token=creat_token(username=username,user_type=user.user_type,token_type="access")
    refresh_token=creat_token(username=username,user_type=user.user_type,token_type="refresh")
    session.close()
    return {"access_token":access_token,"refresh_token":refresh_token}
    
def creat_token(username,user_type,token_type):
    time =ACCEESS_TOKEN_EXPIRY
    if token_type =="refresh":
        time=REFRESH_TOKEN_EXPIRY
    payload={
        "username":username,
        "token_type":token_type,
        "user_type":user_type,
        "exp": datetime.now(timezone.utc)+timedelta(minutes=time),
    }
    token = jwt.encode(payload=payload, key = SECRET_KEY,algorithm=ALGORITHM)
    return token

def verify_token(token,token_type):
    try:
        payload=jwt.decode(jwt=token, key=SECRET_KEY,algorithms=[ALGORITHM])
        
    except:
        return False

    if payload["token_type"]==token_type:
        return payload
    return False


def register_user(username,password,user_type):
    if user_type not in ["owner","dispatcher"]:
            raise HTTPException(status_code=422,detail="incorrect user type")
    session = Session(engine)
    user=session.query(User).filter_by(username=username).first()
    if user is not None:
        session.close()
        return False
    session.add(User(username=username,password=ph.hash(password),user_type=user_type.lower()))
    session.commit()
    session.close()
    return True
