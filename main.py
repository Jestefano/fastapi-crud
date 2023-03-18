from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import boto3 
import json
from pydantic import BaseModel
from uuid import uuid4
from typing import Optional, Literal

from dotenv import load_dotenv
from datetime import date
import os
import awswrangler as wr  

load_dotenv()

BUCKET_NAME = os.getenv('BUCKET_NAME')
FOLDER_NAME = os.getenv('FOLDER_NAME')
DB_NAME = os.getenv('DB_NAME')
TABLE_NAME = os.getenv('TABLE_NAME')

class Expense(BaseModel):
    id_: Optional[str] = uuid4().hex
    day: Optional[date] = date.today()
    amount: float
    category: Literal["Food","Education","Home","Others"]
    description: Optional[str] = ""

app = FastAPI()
s3 = boto3.resource('s3')
athena = boto3.client('athena')

@app.get('/')
async def root():
    return {'message':'Welcome to my app! Explore the methods in /docs'}

@app.post('/create')
async def create(expense: Expense):
    expense.id_ = uuid4().hex
    json_expense = jsonable_encoder(expense)
    print(json_expense)
    
    id_store = json_expense['id_']
    category = json_expense['category']
    del json_expense['category']

    s3object = s3.Object(BUCKET_NAME, f'{FOLDER_NAME}/{category}/{id_store}.json')

    s3object.put(Body=(bytes(json.dumps(json_expense).encode('UTF-8'))))

    return {"message":"Inserted correctly"}
    
@app.get('/get_all/')
async def get_all():
    df = wr.athena.read_sql_query(sql=f"SELECT * FROM {TABLE_NAME}", database=DB_NAME)
    json_df = df.T.to_dict()
    
    return {'data':json_df}

@app.get('/get_category/{category}')
async def get_category():
    pass

@app.get('/get_one/{id}')
async def get_one(id: str):
    pass

@app.get('/update')
async def update():
    pass

@app.get('/delete')
async def delete():
    pass
