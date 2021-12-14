from flask import Flask
from flask import redirect, url_for, request

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security, current_user

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
db.init_app(app)
with app.app_context():
    db.create_all()

from models import *

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass



class HomeAdminView(AdminMixin, AdminIndexView):
    @expose('/')
    def index(self):
        user = current_user
        if user.is_authenticated:
            user = security.datastore.add_role_to_user(user, 'admin')
        return self.render('admin.html', user=user)


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.generate_slug()
        return super().on_model_change(form, model, is_created)


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'abstract', 'body', 'tags']


class TagAdminView(AdminMixin, BaseModelView):
    pass


admin = Admin(app, 'Ponimazi', url='/',
              index_view=HomeAdminView(name='Admin'))

admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))

# Flask-security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
