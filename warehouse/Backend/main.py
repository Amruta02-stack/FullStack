from fastapi import FastAPI
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
def register_package(name,destination,weight,arrival_date,status):
    return function.register_package(name=name,destination=destination,weight=weight,arrival_date=arrival_date,status=status)
    
@app.get("/package/{id}")
def get_package(id):
    return function.get_package(id)

# @app.patch("/pakage/{id}")


@app.delete("/package/{id}")
def delete_package(id):
    return function.delete_package(id)

# @app.get("/package")
# def get_package():
#     return function.get_package()

# @app.get("")


# @app.post()