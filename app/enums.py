from enum import Enum
from app.utils import get_categories_aux
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.resource('s3')
BUCKET_NAME = os.getenv('BUCKET_NAME')

list_categories = get_categories_aux(s3, BUCKET_NAME)
dict_categories = {cat.upper():cat.title() for cat in list_categories}

TypeEnum = Enum("CategoryType", dict_categories)