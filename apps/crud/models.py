from datetime import datetime

from apps.app import db
from werkzeug.security import generate_password_hash


# db.Modelに継承することで，これはデータベースのテーブルと繋がるクラスであるとFlaskに伝えている
class User(db.Model):  # userクラスは，データベースとpythonの橋渡し役
    __tablename__ = "users"  # データベースのテーブル名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, index=True)
    email = db.Column(db.String, index=True, unique=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def password(self):
        raise AttributeError("読み取り不可")

    # print(user.password) -> AttributeError: 読み取り不可
    # ・パスワードは見せない
    # ・間違ってもコードから表示できないように
    # セキュリティ対策

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 生のパスワードを受け取ったらgenerate_password_hash()によってハッシュ化して保存する
