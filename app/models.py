from app import db, login
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    region = db.Column(db.String(32), nullable=False)
    users = db.relationship('User', backref='from_city', lazy='dynamic')

    def __repr__(self):
        return '<City {}>'.format(self.name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String(32))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    about_me = db.Column(db.String(140))
    password_hash = db.Column(db.String(128))
    capabilities = db.relationship('Capability', backref='owner', lazy='dynamic')
    needs = db.relationship('Need', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=monsterid&s={}'.format(digest, size)


class Capability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(140))

    def __repr__(self):
        return '<Capability {}>'.format(self.name)


class Need(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(140))

    def __repr__(self):
        return '<Need {}>'.format(self.name)