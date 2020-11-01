from flask import Flask
from flask_sqlalchemy import SQLAlchemy

user = 'postgres'
pw = 'postgres'
url = 'localhost:5432'
db = 'postgres'
DB_URL = f'postgresql+psycopg2://{user}:{pw}@{url}/{db}'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
alchemy_db = SQLAlchemy(app)
