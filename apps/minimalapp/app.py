from email_validator import validate_email, EmailNotValidError
from flask import (
    Flask,
    render_template,
    url_for,
    current_app,
    g,
    request,
    redirect,
    flash,
    make_response,
    session,
)
import logging
from flask_debugtoolbar import DebugToolbarExtension
import os
from flask_mail import Mail, Message

# FLASK_APP…どのファイルがアプリかを教える
# $env:FLASK_DEBUG = "1"により
# ・デバッグモードが自動でオンになる
# ・自動リロードが有効になる

# Flaskをインスタンス化
app = Flask(__name__)  # この"app"をFLASK_APPで指定している

# SECRET_KEYを追加する
app.config["SECRET_KEY"] = "2AZSMss3"

app.logger.setLevel(logging.DEBUG)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)


# URLと実行する関数をマッピングする
@app.route("/")  # デコレーター
def index():
    return "hello, flaskbook!"


@app.route("/hello/<name>", methods=["GET", "POST"], endpoint="hello-endpoint")
def hello(name):
    return f"hello, {name}"


# Flask2からは以下のように記述することが可能
# @app.get("/hello")
# @app.post("/hello")
# def hello():
#     return "hello"


@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)


with app.test_request_context():
    # /
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint", name="world"))
    # /name/ichiro?page=ichiro
    print(url_for("show_name", name="ichiro", page="1"))

# print(current_app.name)
# ここで呼び出すとエラー

ctx = app.app_context()
ctx.push()

print(current_app.name)

g.connection = "connection"
print(g.connection)

with app.test_request_context("/users?updated=true"):
    print(request.args.get("updated"))


@app.route("/contact")
def contact():
    # レスポンスオブジェクトを取得
    responce = make_response(render_template("contact.html"))

    # クッキーを設定する
    responce.set_cookie("flaskbook key", "flaskbook value")

    # セッションを設定する
    session["username"] = "ichiro"
    return responce


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        is_valid = True

        if not username:
            flash("usernameは必須です")
            is_valid = False

        if not email:
            flash("mailadressは必須です")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError:
            flash("mailadressの形式で入力して下さい")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        send_email(
            email,
            "問い合わせありがとうございます",
            "contact_mail",
            username=username,
            description=description,
        )

        flash("問い合わせありがとうございました")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")


def send_email(to, subject, template, **kwargs):
    msg = Message(subject=subject, recipients=[to])
    msg.body = render_template(f"{template}.txt", **kwargs)  # template + ".txt"
    msg.html = render_template(f"{template}.html", **kwargs)

    mail.send(msg)
