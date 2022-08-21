"""
 copyrigth © ryanbsdeveloper
 2022 - brazil
"""

from .db import db


class AuthModel(db.Model):
    __tablename__ = "authorization"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def as_dict(self):
        return dict(
            id=self.id,
            username=self.username,
            password=self.password,
        )

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
