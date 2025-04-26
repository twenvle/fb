from flask import Flask
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()

csrf = CSRFProtect()


# create_app関数を作成する
def create_app():
    # Flaskをインスタンス化
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="qwerty",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        # sqlite://はSQLiteを使うためのURI
        # __file__はこのファイルのパスを示す
        # parentは親ディレクトリを示す　cd..と考えるとわかりやすい
        SQLAlchemy_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        # 実行したSQLを確認できるようにする
        WTF_CSRF_SECRET_KEY="aiueo",
    )

    csrf.init_app(app)

    # SQLとはデータベースを操作するための言語
    # 通常，データベースのデータをプログラムから操作するにはSQLを使う必要があるが，
    # SQLAlchemyを使うことで，Pythonのコードでデータベースを操作できるようになる

    # SQLAlchemyとアプリを連携する
    db.init_app(app)
    # Migrateとアプリを連携する
    Migrate(app, db)

    # crudパッケージからviewsをインポート
    from apps.crud import views as crud_views

    # register_blueprintを使ってviewsのcrudへ登録する
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    # app.routeが増えてくると複雑になるので役割ごとに分割したい．　そこで用いるのがBlueprint
    # url_prefix="/crud"で全てのURLに/crudをつける

    return app  # create_app関数の中で箱(Flask)に色々入れて，最後にその箱を返しているのが return app
