from http import HTTPStatus
from re import fullmatch

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .utils import get_unique_short_id, is_unique


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_url(short_id):
    url_map = URL_map.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND.value)
    return jsonify(url=url_map.original), HTTPStatus.OK.value


@app.route('/api/id/', methods=['POST'])
def create_id():
    CUSTOM_ID_FIELD = 'custom_id'
    REQUIRED_FIELD = 'url'
    PATTERN = r'^[a-zA-Z0-9]+$'
    MAX_LEN = 16

    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    short_id = data.get(CUSTOM_ID_FIELD)
    if short_id in (None, ''):
        short_id = get_unique_short_id()
        data['custom_id'] = short_id
    elif not fullmatch(PATTERN, short_id) or len(short_id) > MAX_LEN:
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if REQUIRED_FIELD not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    if not is_unique(short_id):
        raise InvalidAPIUsage(f'Имя "{short_id}" уже занято.')

    url_map = URL_map()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED.value
