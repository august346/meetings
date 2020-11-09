import datetime

from sqlalchemy import Integer, Column, String, Text, Enum, Table, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from db.db import alchemy_db
from db.enums import PhraseType


PartPhrases = Table(
    'part_phrases',
    alchemy_db.metadata,
    Column('part_id', Integer, ForeignKey('part.id')),
    Column('phrase_id', Integer, ForeignKey('phrase.id'))
)


class Scenario(alchemy_db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)

    parts = relationship('Part', back_populates='scenario')

    histories = relationship('History', back_populates='scenario')


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
        back_populates='parts'
    )


class Phrase(alchemy_db.Model):
    id = Column(Integer, primary_key=True)
    context = Column(Enum(PhraseType))
    title = Column(String(80), nullable=False)
    file_id = Column(Text, nullable=False)

    # player_id = Column(Integer, ForeignKey('player.id'))
    # player = relationship('Player', back_populates='phrases')

    parts = relationship(
        'Part',
        secondary=PartPhrases,
        back_populates='phrases'
    )

    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'file_id': self.file_id
        }


class History(alchemy_db.Model):
    id = Column(Integer, primary_key=True)
    data = Column(JSONB)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime)

    # questioner_id = Column(Integer, ForeignKey('player.id'))
    # questioner = relationship('Player', back_populates='q_histories')
    #
    # answerer_id = Column(Integer, ForeignKey('player.id'))
    # answerer = relationship('Player', back_populates='a_histories')

    scenario_id = Column(Integer, ForeignKey('scenario.id'))
    scenario = relationship('Scenario', back_populates='histories')


# class Player(alchemy_db.Model):
#     id = Column(Integer, primary_key=True)
#     nick_name = Column(String(80), nullable=False)
#
#     q_histories = relationship('History', back_populates='questioner')
#     a_histories = relationship('History', back_populates='answerer')
#     phrases = relationship('Phrase', back_populates='player')
