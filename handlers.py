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
    if request.method == 'GET':
        # TODO: Change this with microservice:
        announcement_list = [
            Announcement('Ali', 'BOyle BOyle oldu'),
            Announcement('Mahmut', 'Bak bu da var'),
            Announcement('Xdeeeee', 'Hayde gidelum hayde hayde ')
        ]

        return render_template('home/index.html', announcement_list=announcement_list)


@site.route('/search', methods=['POST'])
def search_movie():
    return redirect(url_for('site.movies_index', movie_name=request.form['search']))


@site.route('/movies', methods=['GET', 'POST'])
def movies_index():
    # Take the search value parameter
    search_value = request.args.get('movie_name')
    search_value = search_value if search_value != None else ''

    # TODO: Change this with microservice with the search params
    my_cast = Cast([Actor('Ali', 'Veli', 'Venom'),
                    Actor('Hasan', 'Mahmut', 'Second Vecom')])
    movie_list = [
        Movie('Ali', 'Lorem ipsum', 1, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg"),
        Movie('Ali', 'Lorem ipsum', 3, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg"),
        Movie('Ali', 'Lorem ipsum', 5, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg"),
        Movie('Ali', 'Lorem ipsum', 2.5, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg")
    ]

    return render_template('movie/index.html', movie_list=movie_list)


@site.route('/movies/<int:movie_id>', methods=['GET', 'POST'])
def movies_show(movie_id):
    # TODO: Change this with db by using movie_id
    my_cast = Cast([Actor('Ali', 'Veli', 'Venom'),
                    Actor('Hasan', 'Mahmut', 'Second Vecom')])
    movie = Movie('Ali', 'Lorem ipsum', 4, 100,
                  'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg")

    return render_template('movie/show.html', movie=movie)


@site.route('/movies/<int:movie_id>/update', methods=['GET', 'POST'])
def movies_update(movie_id):
    print(movie_id)
    return render_template('movie/update.html')


@site.route('/aboutus', methods=['GET'])
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
    if request.method == 'GET':
        return render_template('payment/index.html', form=None)
    else:
        form = request.form
        form.data = {}
        form.errors = {}
        print(form["cardholder"])
        print(form["expiration-month"])
        print(form["expiration-year"])
        print(form["cardnumber"])
        print(form["cvc"])
        # TODO: Send them to the microservice
        # If return is not 200
        # then form.errors['notcompleted'] = 'We couldn\'t registred you as user please change your info or try again.'
        form.errors['notcompleted'] = 'Payment is not accepted. Please try different card.'
        return render_template('payment/index.html', form=form)
        # ELSE If successfull go to the home page with login user
        return redirect(url_for('site.movies'))


@site.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register/index.html', form=None)
    else:
        form = request.form
        form.data = {}
        form.errors = {}
        print(form["name"])
        print(form["surname"])
        print(form["username"])
        print(form["email"])
        print(form["password"])
        print(form["birthdate"])
        print(form["gender"])
        # TODO: Send them to the microservice
        # If return is not 200
        # then form.errors['notcompleted'] = 'We couldn\'t registred you as user please change your info or try again.'
        form.errors['notcompleted'] = 'We couldn\'t registred you as user please change your info or try again.'
        return render_template('register/index.html', form=form)
        # ELSE If successfull go to the home page with login user
        return redirect(url_for('site.home'))


@site.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # If user is authenticated direct it to homepage
        # else
        return render_template('login/index.html', form=None)
    else:
        form = request.form
        print(form["email"])
        print(form["password"])
        # Send to the microservice.
        # Get the result
        # IF it is not 200
        form.errors['notcompleted'] = 'Login is not successful. Please try again.'
        return render_template('register/index.html', form=form)

        # ELSE If successfull go to the home page with login user
        return redirect(url_for('site.home'))


@site.route('/watch', methods=['GET', 'POST'])
def watch():
    return render_template('watch/index.html')


@site.route('/search', methods=['GET', 'POST'])
def search():
    return redirect(url_for('site.movies_index'))


@site.route('/publish', methods=['POST'])
def publish():
    return redirect(url_for('site.admin'))


@site.route('/movies/add', methods=['POST'])
def add_movie():
    return redirect(url_for('site.admin'))

# @site.route('/movie')
# def movie():
#     # a = requests.get('http://053e8eac.ngrok.io/payment/create').content
#     # print('asdf')
#     return requests.get('http://053e8eac.ngrok.io/payment/create').content
