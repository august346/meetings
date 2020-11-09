from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

user = 'postgres'
pw = 'postgres'
url = 'localhost:5432'
db = 'postgres'
DB_URL = f'postgresql+psycopg2://{user}:{pw}@{url}/{db}'


alchemy_db = SQLAlchemy()
migrate = Migrate()
