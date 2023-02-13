import datetime
import json
import uuid

import mlflow
import pandas as pd
import pytz
import utils.schemas as _schemas
import utils.services as _services
import sqlalchemy.orm as _orm
import uvicorn
from fastapi import Depends, FastAPI
import pickle

app = FastAPI()
_services.create_database()

logged_model = "./question_model"
loaded_model = mlflow.pyfunc.load_model(logged_model)

labels = json.load(open("./utils/labels.json"))

def predict_pipeline(data):
    return loaded_model.predict(pd.DataFrame(data))

def amount_words_in_question(raw_input: dict, keys: list, new_keys: list):
    for index, key in enumerate(keys):
        raw_input[new_keys[index]] = [value.count(' ') + 1 for value in raw_input[key]]
    print(raw_input)
    return raw_input


@app.get("/raw_input/")
def read_rawinput(  
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = Depends(_services.get_db)
):
    return _services.get_rawinput(db=db, skip=skip, limit=limit)

@app.get("/predictions/")
def read_predict(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = Depends(_services.get_db)
):
    return _services.get_prediction(db=db, skip=skip, limit=limit)

@app.post("/predict/", response_model=_schemas.Predictions)
def create_predict(
    user: _schemas._CreatePrediction, db: _orm.Session = Depends(_services.get_db)
):
    """1. Raw input data handling"""
    UUID = str(uuid.uuid1())
    created_at = datetime.datetime.now(pytz.timezone('Europe/Amsterdam'))

    user_input = user.dict()
    user_input = amount_words_in_question(user_input, keys=["question1", "question2"], new_keys=["q1_words", "q2_words"])
    #_services.insert_raw_snowflake(input_data=user_input, UUID=UUID, created_at=created_at)
    _services.insert_raw_mongodb(input_data=user_input, UUID=UUID, created_at=created_at)
    _services.create_rawinput(db=db, id=UUID, created_at=created_at, raw_input=user_input)

    """2. Prediction data handling"""
    prediction = predict_pipeline(user_input)
    predictions = [labels[str(single_prediction)] for single_prediction in prediction.tolist()]
    print("Raw Predictions: ", prediction, "\nPredictions:", predictions)
    
    _services.insert_predictions_mongodb(UUID=UUID, created_at=created_at, predictions=predictions)
    #_services.insert_predictions_snowflake(UUID=UUID, created_at=created_at, predictions=predictions)
    return _services.create_prediction(db=db, PredictionID=UUID, created_at=created_at, pred=predictions)

if __name__ == '__main__':
    uvicorn.run(app)