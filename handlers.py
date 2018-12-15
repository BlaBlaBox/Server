from flask import Blueprint, render_template, redirect, current_app, url_for
from flask import request, flash, session, abort


from classes.Announcement import *
from classes.Movie import *

import requests
site = Blueprint('site', __name__)


@site.route('/', methods=['GET', 'POST'])
def home():
    # TODO: Change this with database
    announcement_list = [
        Announcement('Ali', 'Hasan'),
        Announcement('Mahmut', 'Hasan'),
        Announcement('Xdeeeee', 'Hasan')
    ]

    return render_template('home/index.html', announcement_list=announcement_list)


@site.route('/movies', methods=['GET', 'POST'])
def movies_index():
    # TODO: Change this with database
    movie_list = [
        Movie("Ali", 4, 100, "static/img/movies/bohemian_rapsody.jpg"),
        Movie("Hasan", 3.5, 200, "static/img/movies/bohemian_rapsody.jpg"),
        Movie("Ayse", 2, 300, "static/img/movies/bohemian_rapsody.jpg"),
        Movie("Gizem", 5, 500, "static/img/movies/bohemian_rapsody.jpg")
    ]

    return render_template('movie/index.html', movie_list=movie_list)


@site.route('/movies/<int:movie_id>', methods=['GET', 'POST'])
def movies_show(movie_id):
    print(movie_id)
    return render_template('movie/show.html')


@site.route('/movies/<int:movie_id>/update', methods=['GET', 'POST'])
def movies_update(movie_id):
    print(movie_id)
    return render_template('movie/update.html')


@site.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    return render_template('aboutus/index.html')


@site.route('/admin', methods=['GET', 'POST'])
def admin():
    return render_template('admin/index.html')


@site.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('cart/index.html')


@site.route('/library', methods=['GET', 'POST'])
def library():
    return render_template('library/index.html')


@site.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment/index.html')


@site.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register/index.html')


@site.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login/index.html')


@site.route('/watch', methods=['GET', 'POST'])
def wath():
    return render_template('watch/index.html')


# @site.route('/movie')
# def movie():
#     # a = requests.get('http://053e8eac.ngrok.io/payment/create').content
#     # print('asdf')
#     return requests.get('http://053e8eac.ngrok.io/payment/create').content
