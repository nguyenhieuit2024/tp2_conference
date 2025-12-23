from datetime import datetime
from .config import db

class Conference(db.Model):
    __tablename__ = 'conferences'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    submission_deadline = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    tracks = db.relationship('Track', backref='conference', cascade='all, delete-orphan')

class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    conference_id = db.Column(db.Integer, db.ForeignKey('conferences.id'), nullable=False)
