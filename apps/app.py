from flask import Flask
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from apps.config import config
from flask_login import LoginManager

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

login_manager.login_view = "auth.signup"
login_manager.login_message = ""


# create_app関数を作成する
def create_app(config_key):
    # Flaskをインスタンス化
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    csrf.init_app(app)

    # SQLとはデータベースを操作するための言語
    # 通常，データベースのデータをプログラムから操作するにはSQLを使う必要があるが，
    # SQLAlchemyを使うことで，Pythonのコードでデータベースを操作できるようになる

    # SQLAlchemyとアプリを連携する
    db.init_app(app)
    # Migrateとアプリを連携する
    Migrate(app, db)

    # login_managerをアプリケーションと連携する
    login_manager.init_app(app)

    # crudパッケージからviewsをインポート
    from apps.crud import views as crud_views

    # register_blueprintを使ってviewsのcrudへ登録する
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    # app.routeが増えてくると複雑になるので役割ごとに分割したい．　そこで用いるのがBlueprint
    # url_prefix="/crud"で全てのURLに/crudをつける

    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    return app  # create_app関数の中で箱(Flask)に色々入れて，最後にその箱を返しているのが return app
