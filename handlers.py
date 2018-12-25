import os
import json
import requests
from flask import Blueprint, render_template, redirect, current_app, url_for, request, send_from_directory, abort
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename

from classes.Announcement import Announcement
from classes.Movie import Movie
from classes.Actor import Actor
from classes.Cast import Cast
from classes.CartElement import CartElement
from classes.User import UserObj

from api_links import AUTH, MOVIE, PAYMENT, ANNCMT

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'x-m4v'])

site = Blueprint('site', __name__)


@site.route('/loaderio-e4da898c282715093e8e832a29feefd8/', methods=['GET', 'POST'])
def load_test():
    return send_from_directory('./', 'load_test.txt')


@site.route('/', methods=['GET', 'POST'])
def home():

    announcement_list = []
    rv_anno = requests.get(ANNCMT + "announcement/get")
    rv_json = json.loads(rv_anno.content)

    for ann_json in rv_json['announcement_list']:
        announcement_list.append(Announcement(**ann_json))

    if not announcement_list:
        announcement_list = None

    return render_template('home/index.html', announcement_list=announcement_list)


@site.route('/search', methods=['POST'])
def search_movie():
    return redirect(url_for('site.movies_index', movie_name=request.form['search']))


@site.route('/movie/<int:movie_id>/<int:price>/rent', methods=['POST'])
def movie_rent(movie_id, price):
    rent_json = {
        'movie_id': str(movie_id),
        'price': str(price),
        'duration': '7'
    }
    print(rent_json)

    rv = requests.post(PAYMENT + "cart/item/create/" + str(current_user.id), json=rent_json)
    print(rv.content)

    return redirect(url_for('site.movies_index'))


@site.route('/movie/<int:movie_id>/<int:price>/buy', methods=['POST'])
def movie_buy(movie_id, price):

    buy_json = {
        'movie_id': str(movie_id),
        'price': str(price),
        'duration': '0'
    }

    print(buy_json)
    rv = requests.post(PAYMENT + "cart/item/create/" + str(current_user.id), json=buy_json)
    print(rv.content)
    return redirect(url_for('site.movies_index'))


def take_movie_from_json(movie):
    return [movie['movie_id'], movie['movie_title'], movie['release_year'], movie['added_at'], movie['duration'], movie['rating']/2, movie['information'], movie['cover_url'], movie['video_url'], movie['rent_price'], movie['purchase_price']]


@site.route('/movies', methods=['GET', 'POST'])
def movies_index():
    # Take the search value parameter
    search_value = request.args.get('movie_name')
    search_value = search_value if search_value is not None else ''

    rv_movies = requests.get(MOVIE + "movie/get")

    if rv_movies.status_code != 200:
        return render_template('movie/index.html', movie_list=None)
    rv_json = rv_movies.json()
    movies = rv_json['movies']
    movie_list = []

    for movie in movies:
        my_cast = []

        cast_rv = requests.get(MOVIE + "movie/get/" + str(movie['movie_id']) + "/cast")
        cast_json = cast_rv.json()

        if cast_rv.status_code == 200:
            for actor in cast_json['cast']:
                my_cast.append(Actor(actor['name']))

            movie_list.append(Movie(*take_movie_from_json(movie), my_cast))

    movie_list = [movie for movie in movie_list if search_value.lower() in movie.title.lower()]
    return render_template('movie/index.html', movie_list=movie_list)


@site.route('/movies/<int:movie_id>', methods=['GET', 'POST'])
def movies_show(movie_id):

    # TODO: Change this with db by using movie_id

    movie_info_request = requests.get(MOVIE + 'movie/get/' + str(movie_id))
    movie_info = movie_info_request.json()
    movie = movie_info['movie']

    actor_list = []

    cast_rv = requests.get(MOVIE + "movie/get/" + str(movie_id) + "/cast")
    cast_json = cast_rv.json()

    if cast_rv.status_code == 200:
        for actor in cast_json['cast']:
            actor_list.append(Actor(actor['name']))

        print(actor_list)
        movie = Movie(*take_movie_from_json(movie), Cast(actor_list))


        return render_template('movie/show.html', movie=movie)
    return redirect(url_for('site.home'))


@site.route('/movies/<int:movie_id>/update', methods=['GET', 'POST'])
def movies_update(movie_id):
    print(movie_id)
    return render_template('movie/update.html')


@site.route('/movie/<int:movie_id>/watch', methods=['GET', 'POST'])
def movie_watch(movie_id):
    # Get current movie infos
    # CHECK IF USER CAN REALLY WATCH THE MOVIE FROM DATABASE
    if not current_user.is_authenticated:
        return redirect(url_for('site.home'))
    response = requests.get(PAYMENT + "payment/rent/get/"+str(current_user.id))
    if response.status_code != 200:
        return redirect(url_for('site.library'))
    res_json = json.loads(response.content)
    flag = False
    for movie in res_json['movies_list']:
        if movie['movie_id'] == str(movie_id):
            flag = True

    if not flag:
        return redirect(url_for('site.library'))

    movie_info_request = requests.get(MOVIE + 'movie/get/' + str(movie_id))
    print(movie_info_request)
    movie_info = movie_info_request.json()
    movie_info = movie_info['movie']
    my_movie = Movie(*take_movie_from_json(movie_info), None)

    return render_template('watch/index.html', movie=my_movie)


@site.route('/movies/update', methods=['POST'])
def movies_update_router():
    if not current_user.is_admin:
        return redirect(url_for('site.home'))
    return redirect(url_for('site.movies_update', movie_id=request.form['movie_selection']))


@site.route('/movies/delete', methods=['POST'])
def movies_delete():
    if not current_user.is_admin:
        return abort(401)

    movie_id = request.form['movie_selection']
    movie_json = {"movie_id": movie_id}
    requests.post(MOVIE+"movie/delete", json=movie_json)

    return redirect(url_for('site.admin'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@site.route('/movies/add', methods=['POST'])
def add_movie():
    video = request.files["video_path"]
    imdb_id = request.form['imdb_id']
    purchase_price = request.form['purchase']
    rent_price = request.form['rent']
    video_path = ""

    if video and allowed_file(video.filename):
        filename = secure_filename(video.filename)
        video_path = "/vid/movies/"
        video_path = current_app.config['UPLOAD_FOLDER'] + video_path + filename
        absolute_path = os.path.abspath("./" + video_path)
        print("video_path=", video_path)
        print("absolute=", absolute_path)
        video.save(absolute_path)

    movie_json = {"movie_id":imdb_id, "rent":rent_price, "purchase":purchase_price, "video_url":video_path}
    requests.post(MOVIE + "movie/add", json=movie_json)

    return redirect(url_for('site.admin'))


@site.route('/aboutus', methods=['GET'])
def aboutus():
    return render_template('aboutus/index.html')


@site.route('/admin', methods=['GET', 'POST'])
def admin():
    if not current_user.is_admin:
        return redirect(url_for('site.home'))
    # MOVIE_LIST should got changed with classes. Becuase update form should be filled with default values
    rv_movies = requests.get(MOVIE + "movie/get")
    print(rv_movies.status_code)

    if rv_movies.status_code != 200 and rv_movies.status_code != 204:
        return abort(404)

    movie_list = []
    if rv_movies.status_code == 200:
        rv_json = rv_movies.json()
        movies = rv_json['movies']

        if movies:
            for movie in movies:
                movie_list.append((movie['movie_title'], movie['movie_id']))


    # Find all users
    user_list = []
    rv_users = requests.get(AUTH + "user/get")
    rv_json = json.loads(rv_users.content)
    for user_json in rv_json['users']:
        user_list.append(
            (user_json['username'] + ' / ' + user_json['email'], user_json['user_id']))

    return render_template('admin/index.html', user_list=user_list, movie_list=movie_list)


@site.route('/cart', methods=['GET', 'POST'])
def cart():
    if not current_user.is_authenticated:
        return redirect(url_for('site.home'))

    response = requests.get(PAYMENT + "cart/get/"+str(current_user.id))
    if response.status_code != 200:
        return redirect(url_for('site.cart'))
    res_json = json.loads(response.content)

    cart_list = []
    for item in res_json['item_list']:
        # Send to the movie database get movies add them to cart element
        movie_id = item['movie_id']
        print(item)

        movie_info_request = requests.get(MOVIE + 'movie/get/' + str(movie_id))
        movie_info = movie_info_request.json()
        movie = movie_info['movie']

        actor_list = []
        cast_rv = requests.get(MOVIE + "movie/get/" + str(movie_id) + "/cast")
        cast_json = cast_rv.json()

        if cast_rv.status_code == 200:
            for actor in cast_json['cast']:
                actor_list.append(Actor(actor['name']))

        print(actor_list)
        movie = Movie(*take_movie_from_json(movie), Cast(actor_list))

        cart_list.append(CartElement(movie, item['duration'], int(float(item['price']))))

    return render_template('cart/index.html', cart_list=cart_list)


@site.route('/library', methods=['GET', 'POST'])
def library():
    if not current_user.is_authenticated:
        return redirect(url_for('site.home'))

    response = requests.get(PAYMENT + "payment/rent/get/"+str(current_user.id))
    if response.status_code != 200:
        return redirect(url_for('site.home'))

    res_json = json.loads(response.content)
    print(res_json)

    owned_movie_id_list = []
    my_movie_list = []
    for movie in res_json['movies_list']:
        owned_movie_id_list.append(movie['movie_id'])

    print(owned_movie_id_list)
    for movie_id in owned_movie_id_list:
        my_cast = []
        print(MOVIE + 'movie/get/' + str(movie_id))
        movie_info_request = requests.get(MOVIE + 'movie/get/' + str(movie_id))
        print(movie_info_request)
        movie_info = movie_info_request.json()
        movie_info = movie_info['movie']

        cast_rv = requests.get(MOVIE + "movie/get/" + str(movie_info['movie_id']) + "/cast")
        cast_json = cast_rv.json()
        print(cast_json)
        if cast_rv.status_code == 200:
            for actor in cast_json['cast']:
                my_cast.append(Actor(actor['name']))

            my_movie_list.append(Movie(*take_movie_from_json(movie_info), my_cast))


    return render_template('library/index.html', movie_list=my_movie_list)


@site.route('/announcement/add', methods=['POST'])
def add_announcement():
    if not current_user.is_admin:
        return redirect(url_for('site.home'))
    # TODO: Send these to db
    form = request.form

    ann_json = {
        'title': form['title'],
        'text': form['text'],
        'image_link': form['image'],
        'movie_link': form['movie']
    }
    print(ann_json)
    requests.post(ANNCMT + "announcement/create", json=ann_json)

    return redirect(url_for('site.admin'))

@site.route('/payment/', methods=['GET', 'POST'])
def payment():
    if not current_user.is_authenticated:
        return redirect(url_for('site.home'))
    if request.method == 'GET':
        response = requests.get(PAYMENT + "cart/get/"+str(current_user.id))
        if response.status_code != 200:
            return redirect(url_for('site.cart'))
        res_json = json.loads(response.content)

        cart_list = []
        for item in res_json['item_list']:
            # Send to the movie database get movies add them to cart element
            movie_id = item['movie_id']
            print(item)

            movie_info_request = requests.get(MOVIE + 'movie/get/' + str(movie_id))
            movie_info = movie_info_request.json()
            movie = movie_info['movie']

            actor_list = []
            cast_rv = requests.get(MOVIE + "movie/get/" + str(movie_id) + "/cast")
            cast_json = cast_rv.json()

            if cast_rv.status_code == 200:
                for actor in cast_json['cast']:
                    actor_list.append(Actor(actor['name']))

            print(actor_list)
            movie = Movie(*take_movie_from_json(movie), Cast(actor_list))

            cart_list.append(CartElement(movie, item['duration'], int(float(item['price']))))

        return render_template('payment/index.html', form=None, cart_list=cart_list)
    else:
        form = request.form
        form.data = {}
        form.errors = {}

        print(form['cardholder'])
        print(form['expiration-month'])
        print(form['expiration-year'])
        print(form['cardnumber'])
        print(form['cvc'])
        print(form['price'])

        pay_json = {
            'holder': form["cardholder"],
            'expiration': form["expiration-month"] + form["expiration-year"],
            'number': form["cardnumber"],
            'cvc': form['cvc'],
            'cost': form['price']
        }

        rv = requests.post(PAYMENT + 'payment/pay/' + str(current_user.id), json=pay_json)

        if rv.status_code != 200:
            form.errors['notcompleted'] = 'Payment is not accepted. Please try different card.'
            return render_template('payment/index.html', form=form, cart_list=cart_list)
        else:
            return redirect(url_for('site.movies_index'))


@site.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('site.home'))

        return render_template('register/index.html', form=None)
    else:
        form = request.form
        form.data = {}
        form.errors = {}

        register_json = {
            'name': form["name"],
            'surname': form["surname"],
            'gender': form["gender"],
            'dob': form['birthdate'],
            'username': form['username'],
            'password': form['password'],
            'email': form['email']
        }

        rv_register = requests.post(AUTH + "user/register", json=register_json)


        if rv_register.status_code != 200:
            form.errors['notcompleted'] = 'We couldn\'t registred you as user please change your info or try again.'
            return render_template('register/index.html', form=form)

        return redirect(url_for('site.home'))


@site.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))


@site.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('site.home'))
        return render_template('login/index.html', form=None)
    else:
        form = request.form
        form.data = {}
        form.errors = {}

        login_json = {
            'uname_mail': form["email"],
            'password': form["password"]
        }
        rv_login = requests.post(AUTH + "user/login", json=login_json)
        res_json = json.loads(rv_login.content)

        if rv_login.status_code != 200:
            form.errors['notcompleted'] = 'Login is not successful. Please try again.'
            return render_template('register/index.html', form=form)

        user = UserObj(**res_json["user"])
        login_user(user)

        # Create cart
        print(PAYMENT + "cart/create/" + str(user.id))
        requests.post(PAYMENT + "cart/create/" + str(user.id))

        return redirect(url_for('site.home'))


@site.route('/search', methods=['GET', 'POST'])
def search():
    return redirect(url_for('site.movies_index'))


@site.route('/user/suspend', methods=['POST'])
def suspend_user():
    if not current_user.is_admin:
        return redirect(url_for('site.home'))
    # TODO: Send this user_id to the db
    user_id = request.form.get('user_selection')
    print(user_id)

    return redirect(url_for('site.admin'))

@site.route('/loaderio-808d59fcf551d479ee8f1bbdfd670c4f/', methods=['GET','POST'])
def send_loader():
    return current_app.send_static_file('loader/loaderio-808d59fcf551d479ee8f1bbdfd670c4f.txt')
