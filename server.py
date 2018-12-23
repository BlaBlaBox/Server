import requests
from flask import Flask, abort, render_template
from flask_login import LoginManager
from handlers import site, login
from api_links import AUTH
from classes.User import UserObj


lm = LoginManager()
lm.login_view = login

@lm.user_loader
def load_user(user_id):
    response = requests.get(AUTH+"user/get/"+user_id)
    res_val = response.json()
    if res_val["result"] == 'Success':
        return UserObj(**res_val["user"])
    return None


@lm.unauthorized_handler
def unauthorized_access():
    return abort(401)


def create_app():
    app2 = Flask(__name__)
    app2.config.from_object("settings")
    app2.config['UPLOAD_FOLDER'] = '/static'
    app2.register_blueprint(site)
    lm.init_app(app2)
    return app2


app = create_app()


@app.errorhandler(401)
def unauthorized_access_page(err):
    return render_template("error/401.html")

@app.errorhandler(403)
def access_denied_page(err):
    return render_template("error/403.html")

@app.errorhandler(404)
def page_not_found(err):
    return render_template("error/404.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
