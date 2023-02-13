
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /CODE
COPY ["main.py", "./"]
COPY question_model question_model
COPY utils utils

WORKDIR /CODE/fastAPI
COPY sqlite_database.db sqlite_database.db
WORKDIR /CODE

EXPOSE 8020

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8020" ]