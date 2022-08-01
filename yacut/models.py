from datetime import datetime

from flask import url_for

from yacut import db


class URL_map(db.Model):
    FIELDS = {
        'url': 'original',
        'custom_id': 'short',
    }

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), unique=True, nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', custom_id=self.short, _external=True
            ),
        )

    def from_dict(self, data):
        for field in self.FIELDS:
            if field in data:
                setattr(self, self.FIELDS[field], data[field])
