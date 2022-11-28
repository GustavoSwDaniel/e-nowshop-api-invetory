import os


class Config:
    BROKER_URL = os.getenv('BROKER_URL', 'localhost:9092')

    DATABASE_URL = os.getenv(
        'A-POSTGRES_DATABASE_URL', 'postgresql+asyncpg://enowshop:enowshop@127.0.0.1:5432/enowshop')

    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME', 'sa-east-1')
