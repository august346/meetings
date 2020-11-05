import datetime

from sqlalchemy import Integer, Column, String, Text, Enum, Table, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship

from db.db import alchemy_db
from db.enums import PhraseType


PartPhrases = Table(
    'part_phrases',
    alchemy_db.metadata,
    Column('part_id', Integer, ForeignKey('part.id')),
    Column('phrase_id', Integer, ForeignKey('phrase.id'))
)


ScenarioHistory = Table(
    'scenario_history',
    alchemy_db.metadata,
    Column('scenario_id', Integer, ForeignKey('scenario.id')),
    Column('history_id', Integer, ForeignKey('history.id'))
)


class Scenario(alchemy_db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    parts = relationship('Part', back_populates='scenario')

    histories = relationship(
        'History',
        secondary=ScenarioHistory,
        back_populates='scenarios')


class Part(alchemy_db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    range = Column(Integer, nullable=False)
    scenario_id = Column(Integer, ForeignKey('scenario.id'))
    scenario = relationship('Scenario', back_populates='parts')
    phrases = relationship(
        'Phrase',
        secondary=PartPhrases,
        lazy='dynamic',
        back_populates='parts')


class Phrase(alchemy_db.Model):
    id = Column(Integer, primary_key=True)
    context = Column(Enum(PhraseType))
    title = Column(String(80), unique=True, nullable=False)
    file_id = Column(Text, nullable=False)
    parts = relationship(
        'Part',
        secondary=PartPhrases,
        back_populates='phrases')

    def as_dict(self):
        return {
            'title': self.title,
            'file_id': self.file_id
        }


class History(alchemy_db.Model):
    id = Column(Integer, primary_key=True)
    scenario_id = Column(Integer)
    questioner_id = Column(Integer)
    answerer_id = Column(Integer)
    data = Column(JSON)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime)

    scenarios = relationship(
        'Scenario',
        secondary=ScenarioHistory,
        back_populates='histories')
