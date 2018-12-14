from flask import Blueprint, render_template , redirect , current_app,url_for
from flask import request,flash,session,abort

import requests
site = Blueprint('site', __name__)



@site.route("/movie")
def movie():
    # a = requests.get('http://053e8eac.ngrok.io/payment/create').content
    # print('asdf')
    return requests.get('http://053e8eac.ngrok.io/payment/create').content