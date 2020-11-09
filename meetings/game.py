from sqlalchemy.orm.attributes import flag_modified

from db.db import alchemy_db
from db.enums import PhraseType
from db.models import History, Phrase, Part


class Game:

    @staticmethod
    def create(scenario_id, p0_id, p1_id):
        if False:
            pass  # TODO check scenario

        first_part = Game.get_new_part_data(scenario_id, 0)

        h = History(
            scenario_id=scenario_id,
            # questioner_id=p0_id,
            # answerer_id=p1_id,
            data={'parts': [first_part]}
        )

        s = alchemy_db.session
        s.add(h)
        s.commit()

        return h.id

    @staticmethod
    def get_history_data(history_id):
        return History.query.get(history_id).data

    @staticmethod
    def get_new_part_data(scenario_id, part_range):
        part = Part.query.filter(Part.scenario_id == scenario_id, Part.range == part_range).first()

        if part is None:
            return None

        question = part.phrases.filter(Phrase.context == PhraseType.question).first()
        answers = part.phrases.filter(Phrase.context == PhraseType.answer)

        return {
            'question': question.as_dict(),
            'answers': [a.as_dict() for a in answers],
            'answer': None
        }

    @staticmethod
    def add_answer(answer, history_id, part_range):
        session = alchemy_db.session
        h = History.query.get(history_id)
        parts = h.data['parts']

        if parts and parts[-1] is None:
            return

        h.data['parts'][part_range]['answer'] = answer
        h.data['parts'].append(Game.get_new_part_data(h.scenario_id, len(h.data['parts'])))
        flag_modified(h, 'data')
        session.add(h)
        session.commit()
