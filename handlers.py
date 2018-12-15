from flask import Blueprint, render_template, redirect, current_app, url_for
from flask import request, flash, session, abort


from classes.Announcement import *
from classes.Movie import *
from classes.Actor import *
from classes.Cast import *

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
    my_cast = Cast([Actor('Ali', 'Veli', 'Venom'),
                    Actor('Hasan', 'Mahmut', 'Second Vecom')])
    movie_list = [
        Movie('Ali', 'Lorem ipsum', 4, 100,
              'Mahmut Dogan', my_cast, "static/img/movies/bohemian_rapsody.jpg"),
        Movie('Ali', 'Lorem ipsum', 4, 100,
              'Mahmut Dogan', my_cast, "static/img/movies/bohemian_rapsody.jpg"),
        Movie('Ali', 'Lorem ipsum', 4, 100,
              'Mahmut Dogan', my_cast, "static/img/movies/bohemian_rapsody.jpg"),
        Movie('Ali', 'Lorem ipsum', 4, 100,
              'Mahmut Dogan', my_cast, "static/img/movies/bohemian_rapsody.jpg")
    ]

    return render_template('movie/index.html', movie_list=movie_list)


@site.route('/movies/<int:movie_id>', methods=['GET', 'POST'])
def movies_show(movie_id):
    # TODO: Change this with db by using movie_id
    my_cast = Cast([Actor('Ali', 'Veli', 'Venom'),
                    Actor('Hasan', 'Mahmut', 'Second Vecom')])
    movie = Movie('Ali', 'Lorem ipsum', 4, 100,
                  'Mahmut Dogan', my_cast, "static/img/movies/bohemian_rapsody.jpg")

    return render_template('movie/show.html', movie=movie)


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
	if request.method == 'GET':
		# If user is authenticated direct it to homepage
		#else
		return render_template('login/index.html')
	else:
		form = request.form
		print(form["email"])
		print(form["password"])
		# Send to the microservice.
		# Get the result
		return render_template('login/index.html') 
    


@site.route('/watch', methods=['GET', 'POST'])
def wath():
    return render_template('watch/index.html')


# @site.route('/movie')
# def movie():
#     # a = requests.get('http://053e8eac.ngrok.io/payment/create').content
#     # print('asdf')
#     return requests.get('http://053e8eac.ngrok.io/payment/create').content
