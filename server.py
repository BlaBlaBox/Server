import os

from flask import Flask, session
from flask import Blueprint, render_template
from flask_login import LoginManager
from handlers import site
# from classes.UserAccount import UserAccount

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.register_blueprint(site)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
