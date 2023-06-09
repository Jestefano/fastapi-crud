# fastapi-crud
## Description
This project creates a CRUD application using FastAPI, S3, Lambda and Athena.
Its main purpose is to manage my personal finance information in a S3 bucket so it can be later use for analytics purposes.

## User stories

## How to use

## Features

## Arquitecture
(arquitecture img)


## Demo


## Why


## How to run the app
- Create a venv with all the requirements.txt
- Create .env file with your BUCKET_NAME, FOLDER_NAME, DB_NAME and TABLE_NAME 
```
export BUCKET_NAME="XX" 
export FOLDER_NAME="YY" 
export TABLE_NAME="ZZ"
export DB_NAME="WW"
```
- Install aws with credentials on terminal

# S3 and Athena config
- To create the partition manually
```
ALTER TABLE table_name ADD
  PARTITION (category = 'Home')
  LOCATION 's3://finance-tracker-jeste-bot/fastapi-finance/Home/';
```  
An alternative is to use a Crawler from AWS Glue 
- See current partitions
```
SHOW PARTITIONS table
``` 
 
## References
- https://github.com/pixegami/fastapi-tutorial
- https://www.youtube.com/watch?v=4Zy90rd0bkU&list=PL7RYfxSUOWozg0PeSaNW6Vb9jWqo-k8O5&index=5&t=1134s
- https://stackoverflow.com/questions/61753056/partial-update-in-fastapi
- https://github.com/MikaelAbehsera/tweeter
- https://www.youtube.com/watch?v=RGIM4JfsSk0&t=14s
- https://github.com/tiangolo/fastapi/issues/13