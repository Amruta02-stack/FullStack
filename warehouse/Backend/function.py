from sqlalchemy import create_engine,Integer,String,Date,Column,Foreignkey

from sqlalchemy.orm import Session,declarative_base
from fastapi import FastAPI,HTTPException
from datetime import date,datetime,timedelta

DB_PATH = "warehouse.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Package(Base):
    __tablename__ = "package"

    id = Column(Integer,primary_key= True)
    name=Column(String) 
    destination = Column(String)
    weight = Column(Integer)
    arrival_date=Column(Date)
    status = Column(String)

class Dispatch(Base):
        __tablename__ = "dispatch"
        id = Column(Integer,primary_key= True)
        package_id=Column(Integer,Foreignkey("package_id"))
        vehicle = Column(String)
        destination = Column(String)
        dstatus=Column(String)

Base.metadata.create_all(engine)

def seed_data():
    session=Session(engine)
    today = date.today()
    if session.query(Package).count() == 0:
        package_record=[
         Package(id=1,name="earbud",destination="bangalore",weight=2,arrival_date=today-timedelta(1),status="pending"),
         Package(id=2,name="Steel Bottel",destination="bangalore",weight=5,arrival_date=today-timedelta(1),status="pending"),
         Package(id=3,name="Face Cream",destination="mysore",weight=5,arrival_date=today-timedelta(2),status="dispatched"),
         Package(id=4,name="Toy Car",destination="kashmir",weight=2,arrival_date=today,status="dispatched"),
         Package(id=5,name="Pen",destination="delhi",weight=7,arrival_date=today-timedelta(5),status="dispatched"),
         Package(id=6,name="Laptop",destination="delhi",weight=5,arrival_date=today-timedelta(3),status="pending"),
        ]
        session.add_all(package_record)
        session.commit()
    if session.query(Dispatch).count() ==0:
        dispatch_record = [
            Dispatch(id=1,package_id=3,vehicle="KA-23-9032",destination="mysore",dstatus="in-transit"),
            Dispatch(id=2,package_id=4,vehicle="MH-03-5432",destination="kashmir",dstatus="created"),  
            Dispatch(id=3,packaage_id=5,vehicle="DH-01-2463",destination="delhi",dstatus="deleverd"),
        ]
        session.add_all(dispatch_record)
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

def registar_package(name,destination,weight,arrival_date,status):
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

def update_pack(id,name,destination,weight,arrival_date,status):
    session=Session(engine)
    package=session.get(Package,id)
    if package is None:
         session.close()
         raise HTTPException(status_code=404,detail="Package Not Found")
    package.name=name
    package.destination=destination
    package.weight=weight
    package.arrival_date=arrival_date
    package.status=status
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

def delete_paackage(id):
    session=Session(engine)
    package=session.get(Package,id)
    if package is None:
          raise HTTPException(status_code=404,detail="Package Not Found")
    if package.status != "dispatched":
        session.delete(package)
        session.commit()
        session.close()

def add_data(vehicle,destination,dstatus,package_id):
    session=Session(engine)
    package=session.get(Package,package_id)
    if package is None:
         session.close()
         
     


