from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, Email


class UserForm(FlaskForm):
    # ユーザーフォームのusername属性のラベルとバリデータを設定する
    username = StringField(
        "ユーザ名",
        validators=[
            DataRequired(message="ユーザ名は必須です"),
            length(max=30, message="ユーザ名は30文字以内で入力してください"),
        ],
    )

    # ユーザーフォームのemail属性のラベルとバリデータを設定する
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="メールアドレスは必須です"),
            Email(message="正しいメールアドレスを入力してください"),
        ],
    )

    # ユーザーフォームのpassword属性のラベルとバリデータを設定する
    password = PasswordField(
        "パスワード", validators=[DataRequired(message="パスワードは必須です")]
    )

    submit = SubmitField("新規登録")
