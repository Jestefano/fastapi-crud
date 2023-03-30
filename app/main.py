from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder

import boto3
import awswrangler as wr  

from typing import get_args
from uuid import uuid4

from dotenv import load_dotenv

import os

from app.utils import save_json, delete_json, read_id_to_json, get_categories_aux, process_amount
from app.models import Expense, ExpenseOptional

load_dotenv()

BUCKET_NAME = os.getenv('BUCKET_NAME')
FOLDER_NAME = os.getenv('FOLDER_NAME')
DB_NAME = os.getenv('DB_NAME')
TABLE_NAME = os.getenv('TABLE_NAME')

list_categories = get_args(Expense.__annotations__['category'])

app = FastAPI()
s3 = boto3.resource('s3')

@app.get('/')
async def root():
    return {'message':'Welcome to my app! Explore the methods in /docs'}

@app.post('/create', status_code = status.HTTP_201_CREATED)
async def create(expense: Expense):
    expense.id_ = uuid4().hex
    json_expense = jsonable_encoder(expense)
    
    # Validate categories
    list_categories = get_categories_aux(s3, BUCKET_NAME)
    if json_expense['category'] not in list_categories:
        category = json_expense['category']
        HTTPException(404, f"Category {category} not found. See /get_categories for more info.")

    # Process amount
    json_expense['amount_int'] = process_amount(json_expense['amount'])
    
    save_json(s3, BUCKET_NAME, FOLDER_NAME, json_expense)

    return {'message': 'Inserted correctly'}
    
@app.get('/get_all/', status_code = status.HTTP_200_OK)
async def get_all():
    df = wr.athena.read_sql_query(sql=f"SELECT * FROM {TABLE_NAME}", database=DB_NAME)
    json_df = df.T.to_dict()
    
    return {'data': jsonable_encoder(json_df)}

@app.get('/get_category/{category}', status_code = status.HTTP_200_OK)
async def get_category(category: str):
    list_categories = get_categories_aux(s3, BUCKET_NAME)
    if category not in list_categories:
        raise HTTPException(404, f"Category {category} not found. See /get_categories for more info.")
    df = wr.athena.read_sql_query(sql=f"SELECT * FROM {TABLE_NAME} WHERE category = '{category}'", 
                                  database=DB_NAME)
    json_df = df.T.to_dict()
    
    return {'data': jsonable_encoder(json_df)}

@app.get('/get_one/{id_}', status_code = status.HTTP_200_OK)
async def get_one(id_: str):
    json_df = read_id_to_json(DB_NAME, TABLE_NAME, id_)
    
    return {'data': jsonable_encoder(json_df)}

@app.put('/update/{id_}', status_code = status.HTTP_202_ACCEPTED)
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
    
@app.delete('/delete/{id_}', status_code = status.HTTP_202_ACCEPTED)
async def delete(id_: str):
    df_json = read_id_to_json(DB_NAME, TABLE_NAME, id_)
    delete_json(s3, BUCKET_NAME, FOLDER_NAME, df_json)

    return {'message': 'Deleted correctly'}
