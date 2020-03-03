# -*- coding: utf-8 -*-
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddCapabilityForm, AddNeedForm, CitySelectionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, City, Capability, Need
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = CitySelectionForm()
    users = User.query.all()
    capabilities = Capability.query.all()
    needs = Need.query.all()
    cities = City.query.all()
    if form.validate_on_submit():
        sel = form.city.data
        if sel == '0':
            users = User.query.all()
        else:
            users = User.query.filter_by(city_id=sel).all()
    return render_template('index.html', form=form, users=users, capabilities=capabilities, needs=needs, cities=cities)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверный логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                    last_name=form.last_name.data, first_name=form.first_name.data,
                    city_id=form.city.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    city = City.query.filter_by(id=user.city_id).first_or_404()
    capabilities = Capability.query.filter_by(user_id=user.id).all()
    needs = Need.query.filter_by(user_id=user.id).all()
    return render_template('user.html', user=user, city=city, capabilities=capabilities, needs=needs)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.last_name = form.last_name.data
        current_user.first_name = form.first_name.data
        current_user.phone = form.phone.data
        current_user.city_id = form.city.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения сохранены.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.last_name.data = current_user.last_name
        form.first_name.data = current_user.first_name
        form.phone.data = current_user.phone
        form.city.data = str(current_user.city_id)
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/add_capability', methods=['GET', 'POST'])
@login_required
def add_capability():
    form = AddCapabilityForm()
    if form.validate_on_submit() and form.name.data != '':
        cap = Capability(user_id=current_user.id, name=form.name.data)
        db.session.add(cap)
        db.session.commit()
        flash('Возможность добавлена!')
        return redirect(url_for('user', username=current_user.username))
    return render_template('add.html', title='Add Something', form=form)


@app.route('/add_need', methods=['GET', 'POST'])
@login_required
def add_need():
    form = AddNeedForm()
    if form.validate_on_submit() and form.name.data != '':
        need = Need(user_id=current_user.id, name=form.name.data)
        db.session.add(need)
        db.session.commit()
        flash('Потребность добавлена!')
        return redirect(url_for('user', username=current_user.username))
    return render_template('add.html', title='Add Something', form=form)

