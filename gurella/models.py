from datetime import datetime

from gurella.extensions import db


class User(db.Model):
    __tablename__ = 'gurella_user'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    activate = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.created_at}', '{self.updated_at}')"
