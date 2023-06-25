# UserRegistration-fastapi-two-database

################
***important****
create a folder "static" in the root directory
create virtualenv and run "pip install -r requirements.txt'
##################
****important***
create file ".env" in root directory and add the following details
DB_NAME_1 will be postgres database name 
mongo_db will be mongo db name
mongo_collection will be your collection name in mongo db
""""
DB_NAME_1=
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/db_name
base_url = "http://127.0.0.1:8000"
mongo_db =
mongo_collection =
"""""
###############
to create postgres table use "alembic upgrade head"
to run application use "uvicorn main:app --reload"
