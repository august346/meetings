from sqlalchemy.orm.attributes import flag_modified

from db.db import alchemy_db
from db.enums import PhraseType
from db.models import History, Part, Phrase


def test(scenario_id, p0_id, p1_id):
    history_id = start_game(scenario_id, p0_id, p1_id)

    counter = 0

    while part := get_last_part(history_id):
        print(f'#{counter} {part["question"]["file_id"]}')
        for i, answer in enumerate(part['answers']):
            print(f'[{i}] {answer["file_id"]}')
        answer = input()
        add_answer(answer, history_id, counter)
        counter += 1


def start_game(scenario_id, p0_id, p1_id):
    if False:
        pass    # TODO check scenario

    first_part = get_new_part_data(scenario_id, 0)

    h = History(
        scenario_id=scenario_id,
        questioner_id=p0_id,
        answerer_id=p1_id,
        data={'parts': [first_part]}
    )

    s = alchemy_db.session
    s.add(h)
    s.commit()

    return h.id


def get_last_part(history_id):
    return History.query.get(history_id).data['parts'][-1]


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


def add_answer(answer, history_id, part_range):
    session = alchemy_db.session
    h = History.query.get(history_id)
    h.data['parts'][part_range]['answer'] = answer
    h.data['parts'].append(get_new_part_data(h.scenario_id, len(h.data['parts'])))
    flag_modified(h, 'data')
    session.add(h)
    session.commit()


def main():
    test(1, 1, 2)


if __name__ == '__main__':
    main()
