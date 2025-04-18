from flask import Flask, render_template, url_for, current_app, g, request, redirect

# FLASK_APP…どのファイルがアプリかを教える
# $env:FLASK_DEBUG = "1"により
# ・デバッグモードが自動でオンになる
# ・自動リロードが有効になる

# Flaskをインスタンス化
app = Flask(__name__)  # この"app"をFLASK_APPで指定している


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
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")
