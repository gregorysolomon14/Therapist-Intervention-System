from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('therapist.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('patient.id'))
)

class Patient(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    fname=db.Column(db.String(140))
    lname=db.Column(db.String(140))
    def __repr__(self):
        return '<Patient {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Therapist(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    fname=db.Column(db.String(140))
    lname=db.Column(db.String(140))
    followed = db.relationship(
        'Patient', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    def __repr__(self):
        return '<Therapist {}>'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Intervention(db.Model):
    intervention_id = db.Column(db.Integer, primary_key=True, unique=True)
    intervention_name=db.Column(db.String(140))
    __pattablename__=Patient.id
    __theptablename__=Therapist.id
    patient_id= db.Column(db.Integer, db.ForeignKey(__pattablename__))
    therapist_id= db.Column(db.Integer, db.ForeignKey(__theptablename__))
    def __repr__(self):
        return '<Intervention {}>'.format(self.intervention_id)

class Session(db.Model):
    session_id = db.Column(db.Integer, primary_key=True, unique=True)
    session_number=db.Column(db.Integer)
    gametype=db.Column(db.String(140))
    date_started=db.Column(db.String(140))
    __pattablename__=Patient.id
    __theptablename__=Therapist.id
    __inttablename__=Intervention.intervention_id
    patient_id= db.Column(db.Integer, db.ForeignKey(__pattablename__))
    therapist_id= db.Column(db.Integer, db.ForeignKey(__theptablename__))
    intervention_id= db.Column(db.Integer, db.ForeignKey(__inttablename__))

@login.user_loader
def load_user(id):
    return Therapist.query.get(int(id))
