import os

import pymongo
import snowflake.connector
import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = "sqlite:///../sqlite_database.db"

engine = _sql.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()


# MONGO_DB  
client = pymongo.MongoClient("mongodb+srv://fastapi-classifier:{}@{}.bitz3o4.mongodb.net/?retryWrites=true&w=majority".format(
    os.getenv("MONGODB_PASSWORD"), os.getenv("MONGODB_SHARED_CLUSTER_NAME"))
    )
db = client.Questions_classifier_DB
raw_input_mongoDB = db["Raw_input"]
predictions_mongoDB = db["Predictions"]

# SNOWFLAKE_DB
snowflake_connector = None
"""snowflake_connector = snowflake.connector.connect(
    user = os.getenv('SNOWFLAKE_USER'),
    password = os.getenv('SNOWFLAKE_PASSWORD'),
    account = os.getenv('SNOWFLAKE_ACCOUNT'),
    region = os.getenv('SNOWFLAKE_REGION'),
    role = os.getenv('SNOWFLAKE_ROLE'),
    warehouse = os.getenv('SNOWFLAKE_WAREHOUSE'),
    database = os.getenv('SNOWFLAKE_DATABASE')
)"""
