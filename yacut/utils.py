from random import choices
from string import ascii_lowercase, ascii_uppercase, digits

from .models import URL_map


def get_unique_short_id():
    """Сгенерировать короткий идентификатор."""
    LENGTH = 6
    VALID_CHARS = ascii_uppercase + ascii_lowercase + digits

    return ''.join(choices(VALID_CHARS, k=LENGTH))


def is_unique(custom_id):
    """Проверить короткую ссылку на уникальность."""
    return not URL_map.query.filter_by(short=custom_id).first()
