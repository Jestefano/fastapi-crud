import json
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import awswrangler as wr  

def save_json(s3, BUCKET_NAME,FOLDER_NAME,json_data):
    id_item = json_data['id_']
    category = json_data['category']
    del json_data['category']

    s3object = s3.Object(BUCKET_NAME, f'{FOLDER_NAME}/{category}/{id_item}.json')
    s3object.put(Body=(bytes(json.dumps(json_data).encode('UTF-8'))))

def delete_json(s3, BUCKET_NAME,FOLDER_NAME,json_data):
    id_item = json_data['id_']
    category = json_data['category']
    s3.Object(BUCKET_NAME, f'{FOLDER_NAME}/{category}/{id_item}.json').delete()
    
def read_id_to_json(DB_NAME, TABLE_NAME, id_):
    df = wr.athena.read_sql_query(sql = f"SELECT * FROM {TABLE_NAME} WHERE id_ = '{id_}'", 
                                  database = DB_NAME)
    if df.shape[0] == 0:
        raise HTTPException(404, f"Id {id_} not found.")
    
    json_df = df.T.to_dict()[0]
    return jsonable_encoder(json_df)

def get_categories_aux(s3, BUCKET_NAME):
    s3object = s3.Object(BUCKET_NAME, 'conf/categories.json')
    file_content = s3object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)

    return json_content['data']

def process_amount(amount_str: str):
    if len(amount_str.split('.')) == 2:
        amount_int, amount_decimal = amount_str.split('.')
    else:
        amount_int = amount_str
        amount_decimal = ''

    amount_int = int(amount_int)
    if amount_decimal == '':
        amount_decimal = 0
    elif len(amount_decimal) == 1:
        amount_decimal = int(amount_decimal) * 10
    else:
        amount_decimal = int(amount_decimal)
        
    return amount_int * 100 + amount_decimal