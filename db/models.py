from sqlalchemy import Integer, Column, String, Text, Enum, UniqueConstraint, Table, ForeignKey
from sqlalchemy.orm import relationship

from db.db import alchemy_db
from db.enums import PhraseType


class Scenario(alchemy_db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    parts = relationship('Part', back_populates='scenario')


PartPhrases = Table(
    'part_phrases',
    alchemy_db.metadata,
    Column('part_id', Integer, ForeignKey('part.id')),
    Column('phrase_id', Integer, ForeignKey('phrase.id'))
)


class Part(alchemy_db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    range = Column(Integer, nullable=False)
    scenario_id = Column(Integer, ForeignKey('scenario.id'))
    scenario = relationship('Scenario', back_populates='parts')
    phrases = relationship(
        'Phrase',
        secondary=PartPhrases,
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
