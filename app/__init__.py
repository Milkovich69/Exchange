# -*- coding: utf-8 -*-
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."
bootstrap = Bootstrap(app)

from .models import User, City, Capability, Need, MyAdminIndexView, MyModelView, MyUserAdmin

admin = Admin(app, index_view=MyAdminIndexView(menu_icon_type='glyph', menu_icon_value='glyphicon-home'),
              template_mode='bootstrap3')
admin.add_view(MyModelView(City, db.session))
admin.add_view(MyUserAdmin(User, db.session))
admin.add_view(MyModelView(Capability, db.session))
admin.add_view(MyModelView(Need, db.session))


from . import routes, models, errors