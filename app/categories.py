from app.utils import get_categories_aux
from app.main import app, s3, BUCKET_NAME

@app.get('/get_categories/')
def get_categories():
    return get_categories_aux(s3, BUCKET_NAME)

