"""
 copyrigth © ryanbsdeveloper
 2022 - brazil
"""
from .db import db


class ClientModel(db.Model):
    __tablename__ = "clients"
    
    id = db.Column(db.Integer, primary_key=True)
    jwt_identity = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=True)


    def as_dict(self):
        return dict(
            name=self.name,
            email=self.email,
            password=self.password,
            phone=self.phone,

        )

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email, jwt):
        return cls.query.filter_by(email=email, jwt_identity=jwt).first()

    @classmethod
    def get_all_jwt_identity(cls, identity):
        return cls.query.filter_by(jwt_identity=identity).all()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
