from pathlib import Path
from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

AWS_SERVICE_NAME = 's3'
AWS_S3_ENDPOINT_URL = 'https://s3.ir-thr-at1.arvanstorage.ir'
AWS_ACCESS_KEY_ID = '4b742de1-1a24-4840-8780-a6b64c8d976e'
AWS_SECRET_ACCESS_KEY = '956f1099eacb79723f9a2b97d56a68208bf3ae8e'

AWS_S3_FILE_OVERWRITE = False
FILE_UPLOAD_MAX_MEMORY_SIZE = 0
AWS_STORAGE_BUCKET_NAME = 'bitaxi-s3'
AWS_LOCAL_STORAGE = f'{BASE_DIR}/aws/'