from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import boto3 
import json
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional, Literal

from dotenv import load_dotenv
import os

load_dotenv()

BUCKET_NAME = os.getenv('BUCKET_NAME')
FOLDER_NAME = os.getenv('FOLDER_NAME')

class Expense(BaseModel):
    id: Optional[str] = uuid4().hex
    ammount: float
    category: Literal["Food","Education","Home","Others"]
    description: Optional[str] = ""

app = FastAPI()
s3 = boto3.resource('s3')

@app.get('/')
async def root():
    return {'message':'Hello world!'}

@app.post('/create')
async def create(expense: Expense):
    
    expense.id = uuid4().hex
    json_expense = jsonable_encoder(expense)
    print(json_expense)
    
    id_store = json_expense['id']

    s3object = s3.Object(BUCKET_NAME, f'{FOLDER_NAME}/{id_store}.json')

    s3object.put(
        Body=(bytes(json.dumps(json_expense).encode('UTF-8')))
    )

    return {"message":"Inserted correctly"}
    
@app.get('/read')
async def read():
    pass

@app.get('/update')
async def update():
    pass

@app.get('/delete')
async def delete():
    pass
