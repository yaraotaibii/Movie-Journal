
from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from movies_database import Genres, Base, Movies, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Movie Journal"

engine = create_engine('sqlite:///movieswithusers.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    genreslist = session.query(Genres).all()
    latestmovies = session.query(Movies).order_by(
        Movies.id.desc()).limit(4).all()
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state, genreslist=genreslist,
                           latestmovies=latestmovies)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code, now compatible with Python3
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response - Python3 compatible
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += """ " style = "width: 300px; height: 300px;border-radius: 150px;
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> """
    flash("you are now logged in as %s" % login_session['username'])
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/logout')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON APIs for Genres and Movies information


@app.route('/home/genre/JSON')
def GenresJSON():
    genreslist = session.query(Genres).all()
    return jsonify(genreslist=[i.serialize for i in genreslist])


@app.route('/home/genre/<int:genreid>/JSON')
def GenrePageJSON(genreid):
    genreslist = session.query(Genres).filter_by(id=genreid).one()
    movielist = session.query(Movies).filter_by(genre_id=genreid).all()
    return jsonify(movielist=[i.serialize for i in movielist])


@app.route('/home/genre/<int:genreid>/movie/<int:movieid>/JSON')
def MoviePageJSON(genreid, movieid):
    genreslist = session.query(Genres).filter_by(id=genreid).one()
    movie = session.query(Movies).filter_by(id=movieid).one()
    return jsonify(movie=movie.serialize)

# Show homepage


@app.route('/')
@app.route('/home/')
def HomePage():
    genreslist = session.query(Genres).all()
    latestmovies = session.query(Movies).order_by(
        Movies.id.desc()).limit(4).all()
    if 'username' not in login_session:
        return render_template('home(public).html', genreslist=genreslist,
                               latestmovies=latestmovies)
    else:
        return render_template('home.html', genreslist=genreslist,
                               latestmovies=latestmovies)

# Show movies in each genre


@app.route('/home/genre/<int:genreid>/')
def GenrePage(genreid):
    genreslist = session.query(Genres).all()
    latestmovies = session.query(Movies).order_by(
        Movies.id.desc()).limit(4).all()
    genres = session.query(Genres).filter_by(id=genreid).one()
    movielist = session.query(Movies).filter_by(genre_id=genres.id).all()
    if 'username' not in login_session:
        return render_template('genre(public).html', movielist=movielist,
                               gname=genres.name, genres=genres,
                               genre_id=genres.id, genreslist=genreslist,
                               latestmovies=latestmovies)
    else:
        return render_template('genre.html', movielist=movielist,
                               gname=genres.name, genres=genres,
                               genre_id=genres.id, genreslist=genreslist,
                               latestmovies=latestmovies)

# Show movie information


@app.route('/home/genre/<int:genreid>/movie/<int:movieid>/')
def MoviePage(genreid, movieid):
    genreslist = session.query(Genres).all()
    latestmovies = session.query(Movies).order_by(
        Movies.id.desc()).limit(4).all()
    genre = session.query(Genres).filter_by(id=genreid).one()
    movie = session.query(Movies).filter_by(id=movieid).one()
    user = session.query(User).filter_by(id=movie.user_id).one()
    creator = getUserInfo(movie.user_id)
    if 'username' not in login_session:
        return render_template('movie(public).html', name=movie.name,
                               poster=movie.poster, date=movie.release_date,
                               synopsis=movie.synopsis, genreslist=genreslist,
                               genre=genre, movie=movie, gname=genre.name,
                               latestmovies=latestmovies, username=user.name)
    else:
        return render_template('movie.html', name=movie.name,
                               poster=movie.poster, date=movie.release_date,
                               synopsis=movie.synopsis, genreslist=genreslist,
                               genre=genre, movie=movie, gname=genre.name,
                               latestmovies=latestmovies, username=user.name)


# add movie

@app.route('/home/genre/<int:genreid>/new/', methods=['GET', 'POST'])
def NewMoviePage(genreid):
    latestmovies = session.query(Movies).order_by(
        Movies.id.desc()).limit(4).all()
    genre = session.query(Genres).filter_by(id=genreid).one()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newMovie = Movies(
            name=request.form['name'],
            synopsis=request.form['synopsis'],
            release_date=request.form['release_date'],
            poster=request.form['poster'],
            user_id=login_session['user_id'], genre_id=genreid)
        session.add(newMovie)
        session.commit()
        return redirect(url_for('GenrePage', genreid=genreid,
                                latestmovies=latestmovies))
    else:
        return render_template('newMovie.html', id=genreid, gname=genre.name,
                               latestmovies=latestmovies)

# edit movie


@app.route('/home/genre/<int:genreid>/movie/<int:movieid>/edit/',
           methods=['GET', 'POST'])
def EditMoviePage(genreid, movieid):
    latestmovies = session.query(Movies).order_by(
        Movies.id.desc()).limit(4).all()
    EditedMovie = session.query(Movies).filter_by(id=movieid).one()
    if 'username' not in login_session:
        return redirect('/login')
    if EditedMovie.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not " +
                "authorized to edit this movie. But you are welcome to " +
                "add your own!');} </script><body onload='myFunction()''>")
    if request.method == 'POST':
        if request.form['name']:
            EditedMovie.name = request.form['name']
            session.add(EditedMovie)
            session.commit()
        if request.form['release_date']:
            EditedMovie.release_date = request.form['release_date']
            session.add(EditedMovie)
            session.commit()
        if request.form['synopsis']:
            EditedMovie.synopsis = request.form['synopsis']
            session.add(EditedMovie)
            session.commit()
        if request.form['poster']:
            EditedMovie.poster = request.form['poster']
            session.add(EditedMovie)
            session.commit()
        return redirect(url_for('GenrePage', genreid=genreid,
                                latestmovies=latestmovies))
    else:
        return render_template('editMovie.html', movie=EditedMovie,
                               genreid=genreid, movieid=movieid,
                               latestmovies=latestmovies)


# delete movie
@app.route('/home/genre/<int:genreid>/movie/<int:movieid>/delete/',
           methods=['GET', 'POST'])
def DeleteMoviePage(genreid, movieid):
    latestmovies = session.query(Movies).order_by(
        Movies.id.desc()).limit(4).all()
    MovieToDelete = session.query(Movies).filter_by(id=movieid).one()
    if 'username' not in login_session:
        return redirect('/login')
    if MovieToDelete.user_id != login_session['user_id']:
        return ("<script>function myFunction() {alert('You are not " +
                "authorized to delete this movie. But you are welcome to " +
                "add your own!');} </script><body onload='myFunction()''>")
    if request.method == 'POST':
        session.delete(MovieToDelete)
        session.commit()
        return redirect(url_for('GenrePage', genreid=genreid,
                                latestmovies=latestmovies))
    else:
        return render_template('deleteMovie.html', movie=MovieToDelete,
                               genreid=genreid, movieid=movieid,
                               latestmovies=latestmovies)


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
