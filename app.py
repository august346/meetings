from flask import Flask, request, jsonify

from create_test import t_scenario, create_object
from db.db import DB_URL, migrate
from db.models import *
from meetings.game import Game

app = Flask(__name__, instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

alchemy_db.init_app(app)
migrate.init_app(app, alchemy_db)

with app.app_context():
    alchemy_db.create_all()


@app.route('/create', methods=['POST'])
def create_game():
    r_json = request.json

    history_id = Game.create(*(r_json[x] for x in (
        'scenario_id',
        'questioner_id',
        'answerer_id'
    )))

    return jsonify({'id': history_id})


@app.route('/add_answer', methods=['POST'])
def add_answer():
    r_json = request.json
    Game.add_answer(*(r_json[x] for x in (
        'answer_id',
        'history_id',
        'part_range'
    )))
    return jsonify({'added': True})


@app.route('/get_history_data', methods=['GET'])
def get_history_data():
    r_json = request.json
    return jsonify(Game.get_history_data(r_json['history_id']))


@app.route('/create_test')
def create_test():
    create_object(alchemy_db, t_scenario, need_commit=True)
    return jsonify('ok')

