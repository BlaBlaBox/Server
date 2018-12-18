import json
import requests
import os
from flask import Blueprint, render_template, redirect, current_app, url_for
from flask import request, flash, session, abort
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.utils import secure_filename

from classes.Announcement import *
from classes.Movie import *
from classes.Actor import *
from classes.Cast import *
from classes.CartElement import *
from classes.User import UserObj

from api_links import AUTH, MOVIE, PAYMENT, ANNCMT

ALLOWED_EXTENSIONS = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'x-m4v'])


site = Blueprint('site', __name__)


@site.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':

        announcement_list = []
        rv = requests.get(ANNCMT + "announcement/get")
        print(rv)
        rv_json = json.loads(rv.content)

        print(rv_json)
        Announcement
        for ann_json in rv_json['announcement_list']:
            announcement_list.append(Announcement(**ann_json))

        return render_template('home/index.html', announcement_list=announcement_list)


@site.route('/search', methods=['POST'])
def search_movie():
    return redirect(url_for('site.movies_index', movie_name=request.form['search']))


@site.route('/movies', methods=['GET', 'POST'])
def movies_index():
    # Take the search value parameter
    search_value = request.args.get('movie_name')
    search_value = search_value if search_value is not None else ''

    # TODO: Change this with microservice with the search params
    my_cast = Cast([Actor('Ali', 'Veli', 'Venom'),
                    Actor('Hasan', 'Mahmut', 'Second Vecom')])
    movie_list = [
        Movie(0, 'Ali', 'Lorem ipsum', 1, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4"),
        Movie(2, 'Ali', 'Lorem ipsum', 3, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4"),
        Movie(3, 'Ali', 'Lorem ipsum', 5, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4"),
        Movie(4, 'Ali', 'Lorem ipsum', 2.5, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4")
    ]

    return render_template('movie/index.html', movie_list=movie_list)


@site.route('/movies/<int:movie_id>', methods=['GET', 'POST'])
def movies_show(movie_id):
    # TODO: Change this with db by using movie_id
    my_cast = Cast([Actor('Ali', 'Veli', 'Venom'),
                    Actor('Hasan', 'Mahmut', 'Second Vecom')])
    movie = Movie(1, 'Ali', 'Lorem ipsum', 4, 100,
                  'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4")

    return render_template('movie/show.html', movie=movie)


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

    # GET MOVIE WITH MOVIE ID
    my_cast = Cast([Actor('Ali', 'Veli', 'Venom'),
                    Actor('Hasan', 'Mahmut', 'Second Vecom')])
    movie = Movie(1, 'Ali', 'Lorem ipsum', 4, 100,
                  'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rhapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4")

    return render_template('watch/index.html', movie=movie)


@site.route('/movies/update', methods=['POST'])
def movies_update_router():
    if not current_user.is_admin:
        return redirect(url_for('site.home'))
    return redirect(url_for('site.movies_update', movie_id=request.form['movie_selection']))


@site.route('/movies/delete', methods=['POST'])
def movies_delete():
    if not current_user.is_admin:
        return redirect(url_for('site.home'))
    # TODO: Delete movie
    print(request.form['movie_selection'])

    return redirect(url_for('site.admin'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@site.route('/movies/add', methods=['POST'])
def add_movie():
    image = request.files["image_path"]
    video = request.files["video_path"]
    imdb_id = request.form['imdb_id']
    purchase_price = request.form['purchase']
    rent_price = request.form['rent']
    image_path = ""
    video_path = ""

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        imagepath = "/img/movies/"
        imagepath = current_app.config['UPLOAD_FOLDER'] + imagepath + filename
        absolute_path = os.path.abspath("./" + imagepath)
        image.save(absolute_path)
        print("img_path=", imagepath)
        print("absolute=", absolute_path)
        image_path = imagepath

    if video and allowed_file(video.filename):
        filename = secure_filename(video.filename)
        videopath = "/vid/movies/"
        videopath = current_app.config['UPLOAD_FOLDER'] + videopath + filename
        absolute_path = os.path.abspath("./" + videopath)
        print("video_path=", video_path)
        print("absolute=", absolute_path)
        video.save(absolute_path)
        video_path = videopath

    print(video_path)
    # TODO create movie send to the microservice to add
    return redirect(url_for('site.admin'))


@site.route('/aboutus', methods=['GET'])
def aboutus():
    return render_template('aboutus/index.html')


@site.route('/admin', methods=['GET', 'POST'])
def admin():
    if not current_user.is_admin:
        return redirect(url_for('site.home'))
    # TODO: Change this with microservice and change this tuple list anout movie
    # MOVIE_LIST should got changed with classes. Becuase update form should be filled with default values
    movie_list = [('ali', 1), ('ata', 2), ('bak', 3),
                  ('irem', 4), ('okula', 5), ('git', 6)]
    # Find all users
    user_list = []
    rv = requests.get(AUTH + "user/get")
    rv_json = json.loads(rv.content)
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
    for item in res_json['item_list']:
        # Send to the movie database get movies add them to cart element
        print(item)
    # TODO: Connect these with db
    my_cast = Cast([Actor('Ali', 'Veli', 'Venom'),
                    Actor('Hasan', 'Mahmut', 'Second Vecom')])

    movie = Movie(1, 'Ali', 'Lorem ipsum', 4, 100,
                  'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4")
    movie_two = Movie(1, 'Ali', 'Lorem ipsum', 4, 100,
                      'Mahmut HASANANANANANAN', my_cast, "/static/img/movies/bohemian_rapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4")
    cart_list = [CartElemnt(movie, -1, 100), CartElemnt(movie_two, 7, 500),
                 CartElemnt(movie_two, 7, 400), CartElemnt(movie_two, 7, 300)]
    return render_template('cart/index.html', cart_list=cart_list)


@site.route('/library', methods=['GET', 'POST'])
def library():
    if not current_user.is_authenticated:
        return redirect(url_for('site.home'))

    response = requests.get(PAYMENT + "payment/rent/get/"+str(current_user.id))
    if response.status_code != 200:
        return redirect(url_for('site.library'))
    res_json = json.loads(response.content)
    for movie in res_json['movies_list']:
        # TODO : SEND TO MOVIE DATABASE TO GET MOVIE INFO
        #    movie['movie_id']
        print(movie)

    # TODO: Change this with microservice with the search params
    my_cast = Cast([Actor('Ali', 'Veli', 'Venom'),
                    Actor('Hasan', 'Mahmut', 'Second Vecom')])
    movie_list = [
        Movie(0, 'Ali', 'Lorem ipsum', 1, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4"),
        Movie(1, 'Ali', 'Lorem ipsum', 3, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4"),
        Movie(2, 'Ali', 'Lorem ipsum', 5, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4"),
        Movie(3, 'Ali', 'Lorem ipsum', 2.5, 100,
              'Mahmut Dogan', my_cast, "/static/img/movies/bohemian_rapsody.jpg", "/static/vid/movies/bohemian_rhapsody.mp4")
    ]

    return render_template('library/index.html', movie_list=movie_list, form=None)


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
    rv = requests.post(ANNCMT + "announcement/create", json=ann_json)
    # res_json = json.loads(rv.content)

    #     if rv.status_code != 200:
    #         form.errors['notcompleted'] = 'Login is not successful. Please try again.'
    #         return render_template('register/index.html', form=form)
    #     else:
    #     #    print(json.loads(res_json.content))
    #         user = UserObj(**res_json["user"])
    #         login_user(user)
    #         return redirect(url_for('site.home'))

    # print()
    # print()
    # print(form['image'])
    # print(form['movie'])
    return redirect(url_for('site.admin'))


@site.route('/payment', methods=['GET', 'POST'])
def payment():
    if not current_user.is_authenticated:
        return redirect(url_for('site.home'))
    if request.method == 'GET':
        return render_template('payment/index.html', form=None)
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

        # CHANGE this endpoint
        endpoint = 'http://dfcf2d0f.ngrok.io/payment/pay/'+current_user.id
        rv = requests.post(endpoint, json=pay_json)

        if rv != 200:
            form.errors['notcompleted'] = 'Payment is not accepted. Please try different card.'
            return render_template('payment/index.html', form=form)
        else:
            return redirect(url_for('site.movies'))


@site.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('site.home'))
        else:
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

        print(register_json)
        rv = requests.post(AUTH + "user/register", json=register_json)

        print(json.loads(rv.content))
        print(rv.status_code)
        print(rv.content)

        if rv.status_code != 200:
            form.errors['notcompleted'] = 'We couldn\'t registred you as user please change your info or try again.'
            return render_template('register/index.html', form=form)
        else:
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
        else:
            return render_template('login/index.html', form=None)
    else:
        form = request.form
        form.data = {}
        form.errors = {}

        login_json = {
            'uname_mail': form["email"],
            'password': form["password"]
        }
        rv = requests.post(AUTH + "user/login", json=login_json)
        res_json = json.loads(rv.content)

        print(json.loads(rv.content))
        print(rv.status_code)
        print(rv.content)

        if rv.status_code != 200:
            form.errors['notcompleted'] = 'Login is not successful. Please try again.'
            return render_template('register/index.html', form=form)
        else:
            # print(json.loads(res_json.content))
            user = UserObj(**res_json["user"])
            login_user(user)
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
# @site.route('/movie')
# def movie():
#     # a = requests.get('http://053e8eac.ngrok.io/payment/create').content
#     # print('asdf')
#     return requests.get('http://053e8eac.ngrok.io/payment/create').content
