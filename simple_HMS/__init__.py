from flask import Flask, render_template
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from os import path

database = SQLAlchemy()
DB_NAME = "posts.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    database.init_app(app)
    # Configure CKEditor
    ckeditor = CKEditor(app)
    # Configure Bootstrap5
    Bootstrap5(app)

    from .views import views
    from .auth import auth

    # For adding profile images to the comment section we configure Flask-Gravatar
    gravatar = Gravatar(app,
                        size=100,
                        rating='g',
                        default='retro',
                        force_default=False,
                        force_lower=False,
                        use_ssl=False,
                        base_url=None)



    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, BlogPost, Comment
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app



def create_database(app):
    db_path = path.join(app.instance_path, DB_NAME)
    print(f'Database Path !{db_path}')
    if not path.exists(db_path):
        with app.app_context():
            database.create_all()
        print('Created Database!')
    else:
        print('Database already exists.')