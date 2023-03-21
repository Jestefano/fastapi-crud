from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

import boto3
import awswrangler as wr  

from typing import Optional, Literal, get_args
from uuid import uuid4
from pydantic import BaseModel

from dotenv import load_dotenv

from datetime import date
import os

from utils import save_json, delete_json, read_id_to_json

load_dotenv()

BUCKET_NAME = os.getenv('BUCKET_NAME')
FOLDER_NAME = os.getenv('FOLDER_NAME')
DB_NAME = os.getenv('DB_NAME')
TABLE_NAME = os.getenv('TABLE_NAME')

class Expense(BaseModel):
    id_: Optional[str] = uuid4().hex
    day: Optional[date] = date.today()
    amount: float
    category: Literal["Food", "Education", "Home", "Others"]
    description: Optional[str] = ""

class ExpenseOptional(Expense):
    __annotations__ = {k: Optional[v] for k, v in Expense.__annotations__.items()}

list_categories = get_args(Expense.__annotations__['category'])

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
    
    save_json(s3, BUCKET_NAME, FOLDER_NAME, json_expense)

    return {'message': 'Inserted correctly'}
    
@app.get('/get_all/')
async def get_all():
    df = wr.athena.read_sql_query(sql=f"SELECT * FROM {TABLE_NAME}", database=DB_NAME)
    json_df = df.T.to_dict()
    
    return {'data': json_df}

@app.get('/get_category/{category}')
async def get_category(category: str):
    if category not in list_categories:
        raise HTTPException(404, f"Category {category} not found.")
    df = wr.athena.read_sql_query(sql=f"SELECT * FROM {TABLE_NAME} WHERE category = '{category}'", 
                                  database=DB_NAME)
    json_df = df.T.to_dict()
    
    return {'data': json_df}

@app.get('/get_one/{id_}')
async def get_one(id_: str):
    json_df = read_id_to_json(DB_NAME, TABLE_NAME, id_)
    
    return {'data': json_df}

@app.put('/update/{id_}')
async def update(id_: str, expense_optional: ExpenseOptional):
    json_df = read_id_to_json(DB_NAME, TABLE_NAME, id_)
    json_expense = jsonable_encoder(expense_optional)
    
    # Delete json
    delete_json(s3, BUCKET_NAME, FOLDER_NAME, json_df)
    
    for key in json_expense:
        if key == 'id_': 
            continue # Don't modify the key
        elif json_expense[key] is not None: 
            json_df[key] = json_expense[key]

    # Save new json
    save_json(s3, BUCKET_NAME, FOLDER_NAME, json_df)
    
    return {'message': 'Updated correctly'}
    
@app.delete('/delete/{id_}')
async def delete(id_: str):
    df_json = read_id_to_json(DB_NAME, TABLE_NAME, id_)
    delete_json(s3, BUCKET_NAME, FOLDER_NAME, df_json)

    return {'message': 'Deleted correctly'}
