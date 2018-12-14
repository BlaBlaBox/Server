from flask import Blueprint, render_template , redirect , current_app,url_for
from flask import request,flash,session,abort

site = Blueprint('site', __name__)

@site.route("/")
def hello():
    return "Hello World!"


@site.route("/movie")
def movie():
    return "Hello Movie!"