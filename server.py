import requests
from flask import Flask, abort
#from flask import Blueprint
from flask_login import LoginManager
from handlers import site
from api_links import AUTH
from classes.User import UserObj
# from classes.UserAccount import UserAccount


lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    id_obj = {'id': user_id}
    response = requests.post(AUTH+"get/user/"+user_id, json=id_obj)
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
    app2.register_blueprint(site)
    return app2


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
