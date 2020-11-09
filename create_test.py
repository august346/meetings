from collections import namedtuple

from db import models
from db.enums import PhraseType

DBObject = namedtuple('DBObject', (
    'parent_attr',
    'model',
    'number',
    'range_key',
    'attrs',
    'inners'
))

q_phrase = DBObject(
    parent_attr='phrases',
    model=models.Phrase,
    number=1,
    range_key='m',
    attrs=(
        ('context', PhraseType.question),
        ('title', 'test_question_{j}'),
        ('file_id', 'hash_test_question_{j}'),
    ),
    inners=()
)

a_phrase = DBObject(
    parent_attr='phrases',
    model=models.Phrase,
    number=3,
    range_key='k',
    attrs=(
        ('context', PhraseType.answer),
        ('title', 'test_answer_{j}_{k}'),
        ('file_id', 'hash_test_answer_{j}_{k}'),
    ),
    inners=()
)

t_part = DBObject(
    parent_attr='parts',
    model=models.Part,
    number=3,
    range_key='j',
    attrs=(
        ('title', 'test_part_{j}'),
        ('range', ('{j}', int))
    ),
    inners=(q_phrase, a_phrase)
)

t_scenario = DBObject(
    parent_attr=None,
    model=models.Scenario,
    number=1,
    range_key='i',
    attrs=(('name', 'test_scenario_{i}'),),
    inners=(t_part,)
)


def create_object(alchemy_db, db_object: DBObject, format_keys=dict(), need_commit=False):
    results = []

    for i in range(db_object.number):
        format_keys[db_object.range_key] = i
        formatted_attrs = get_formatted_attrs(format_keys, **dict(db_object.attrs))
        obj = db_object.model(**formatted_attrs)
        alchemy_db.session.add(obj)
        results.append(obj)
        for inner_db_object in db_object.inners:
            create_inner(alchemy_db, obj, inner_db_object)

    if need_commit:
        alchemy_db.session.commit()

    return results


def get_formatted_attrs(format_keys, **kwargs):
    result = {}

    for k, v in kwargs.items():
        if isinstance(v, (str, tuple)):
            cast_type = str
            if isinstance(v, tuple):
                cast_type = v[1]
                v = v[0]
            v = cast_type(v.format(**format_keys))
        result[k] = v

    return result


def create_inner(alchemy_db, obj, inner_db_object):
    obj_attr_name = inner_db_object.parent_attr
    to_add = getattr(obj, obj_attr_name)
    to_add.extend(create_object(alchemy_db, inner_db_object))
