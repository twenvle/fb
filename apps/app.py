from flask import Flask


# create_app関数を作成する
def create_app():
    # Flaskをインスタンス化
    app = Flask(__name__)

    # crudパッケージからviewsをインポート
    from apps.crud import views as crud_views

    # register_blueprintを使ってviewsのcrudへ登録する
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app
