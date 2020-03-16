from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from .models import User, City, Capability, Need


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    cities = City.query.all()
    a = []
    for city in cities:
        a.append((str(city.id), city.name))
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    city = SelectField('Город', choices=a)
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Такой логин уже существует!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот электронный адрес уже зарегистрирован!')


class EditProfileForm(FlaskForm):
    cities = City.query.all()
    a = []
    for city in cities:
        a.append((str(city.id), city.name))
    username = StringField('Логин', validators=[DataRequired()])
    last_name = StringField('Фамилия')
    first_name = StringField('Имя')
    phone = StringField('Телефон')
    city = SelectField('Город', choices=a)
    about_me = TextAreaField('Обо мне / мои интересы', validators=[Length(min=0, max=140)])
    submit = SubmitField('Сохранить')


class AddCapabilityForm(FlaskForm):
    name = TextAreaField('Название', validators=[Length(min=0, max=140)])
    submit = SubmitField('Сохранить')


class AddNeedForm(FlaskForm):
    name = TextAreaField('Название', validators=[Length(min=0, max=140)])
    submit = SubmitField('Сохранить')


class CitySelectionForm(FlaskForm):
    cities = City.query.all()
    a = [('0', 'Все города')]
    for city in cities:
        a.append((str(city.id), city.name))
    city = SelectField('Город', choices=a)
    submit = SubmitField('Выбрать')


class MessageForm(FlaskForm):
    message = TextAreaField('Сообщение', validators=[
        DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Отправить')