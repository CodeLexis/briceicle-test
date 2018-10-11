from datetime import datetime
import time

from flask import current_app, g
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.ext.hybrid import hybrid_method
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.constants.statuses import DELETED_STATUS_ID
from app.models.mixins import HasStatus, HasToken, LookUp, Persistence
from utils import generate_unique_reference
from utils.contexts import (
    get_current_api_ref, get_current_request_data, get_current_request_headers)



class BaseModel(db.Model, HasStatus, Persistence):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(64), default=generate_unique_reference)

    @classmethod
    def get(cls, **kwargs):
        return cls.query.filter(
            cls.status_id != DELETED_STATUS_ID,
        ).filter_by(
            **kwargs
        ).first()


class Question(BaseModel):
    __tablename__ = 'questions'

    body = db.Column(db.String(128))

    @property
    def overall_positive_answer_rate(self):
        positive_answers = [
            answer for answer in self.answers if answer.body == 'YES']

        try:
            return '%.2f%% YES' % (
                    len(positive_answers) / len(self.answers)
                    * 100)
        except:
            return 'N/A'

    @property
    def unit_positive_answers(self):
        unit_positive_answers = {}

        for unit in Unit.query.all():
            positive_answers = [
                answer for answer in self.answers if
                answer.body == 'YES' and answer.unit_id == unit.id]

            all_unit_answers = [
                answer for answer in self.answers if answer.unit_id == unit.id]

            print(positive_answers, all_unit_answers)

            try:
                unit_positive_answers[unit.name] = '%.2f%% YES' % (
                    len(positive_answers) / len(all_unit_answers)
                 * 100)

            except ZeroDivisionError:
                unit_positive_answers[unit.name] = 'N/A'

        return unit_positive_answers

    def as_json(self):
        return {
            'body': self.body,
            'answers': {
                'overall': self.overall_positive_answer_rate,
                **self.unit_positive_answers
            }
        }


class Answer(BaseModel):
    __tablename__ = 'answers'

    body = db.Column(db.Enum('YES', 'NO', name='answer_options'))

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))

    question = db.relationship(
        'Question', backref=db.backref('answers', uselist=True), uselist=False)
    unit = db.relationship(
        'Unit', backref=db.backref('answers', uselist=True), uselist=False)


class Unit(BaseModel):
    __tablename__ = 'units'

    name = db.Column(db.String(16))

    def as_json(self):
        return {
            'name': self.name
        }


class Status(BaseModel, LookUp):
    __tablename__ = 'statuses'


class Staff(HasToken):
    __tablename__ = 'staff'

    name = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(512))
    email = db.Column(db.String(128), unique=True, index=True)
    phone = db.Column(db.String(20), unique=True, index=True)
    profile_photo = db.Column(db.TEXT)

    created_by = db.Column(db.Integer, db.ForeignKey('apps.id'))

    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))

    unit = db.relationship(
        'Unit', backref=db.backref('users', uselist=True))

    @property
    def url(self):
        return '/{}'.format(self.name)

    def as_json(self, keys_to_exclude=None):
        result = {
            'uid': self.uid,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'profile_photo': self.profile_photo,
            'created_at': self.created_at.isoformat(),
        }

        if isinstance(keys_to_exclude, (list, tuple, set)):
            map(lambda excluded: result.pop(excluded, None), keys_to_exclude)

        if isinstance(keys_to_exclude, str):
            result.pop(keys_to_exclude, None)

        return result

    @classmethod
    def get_for_auth(cls, **filter_args):
        user = cls.get(**filter_args)

        # Even if the authentication process outside
        # here fails, we can at least know who the "current_user" is
        g.user = user

        return user

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(
            password, method='pbkdf2:sha512')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=None):
        expiration = expiration or current_app.config['TOKEN_LIFESPAN']

        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        expires_on = datetime.fromtimestamp(time.time() + expiration)

        return s.dumps({'id': self.id}).decode('utf-8'), expires_on


class User(BaseModel):
    __tablename__ = 'users'

    name = db.Column(db.String(64))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
