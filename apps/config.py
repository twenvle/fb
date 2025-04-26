from pathlib import Path

basedir = Path(__file__).parent.parent


# BaseConfigクラスを作成する
class BaseConfig:
    SECRET_KEY = "qwrty"  # Flask全体のセキュリティキー
    WTF_CSRF_SECRET_KEY = "aiueo"  # CSRF対策のためのセキュリティキー


class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # SQLAlchemyのオブジェクトの変更履歴の追跡機能をオン/オフする設定 普通はオフ
    SQLALCHEMY_ECHO = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = (
        False  # テスト時はCSRFトークンのチェックが面倒になるので無効化するのが一般的
    )
    # 画像アップロード先にtests/detector/imagesを指定する
    UPLOAD_FOLDER = str(
        Path(basedir, "tests", "detector", "images")
    )  # Pathでbasedir/tests/detector/imagesというフォルダのパスを作り、それを文字列化して代入


# config辞書にマッピングする
config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}
