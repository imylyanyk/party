from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import pyrebase
from googleapiclient.errors import HttpError
import auth
from config import firebase_config, youtube_config
# How to !
# https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

import youtube_helpers as yt
import json

app = Flask(__name__)
app.register_blueprint(auth.app)

firebase = pyrebase.initialize_app(firebase_config)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/name/<name>')
def index_name(name):
    cur_party = 1
    songs = firebase.database().child('parties/0/songs').get()
    songs = songs.val()
    auth_url = "https://accounts.google.com/o/oauth2/auth?\
client_id={0}&\
scope=https//www.googleapis.com/auth/youtube&\
redirect_uri=http//127.0.0.1:5000/oauth2callback&\
response_type=code&\
access_type=offline".format(youtube_config["clientId"])
    return render_template("index.html", name=name, songs=songs, auth_url=auth_url)


@app.route('/oauth2callback')
def handle_auth(data):
    return str(request.args)


@app.route('/add')
def add_song():
    return render_template("add.html")


@app.route('/ajax_search')
def ajax_search():
    q = request.args['q']
    res = []
    try:
        res = yt.youtube_search({"q": q, "max_results": 5})
    except HttpError as e:
        print("An HTTP error occurred:\n", e.resp.status, e.content)
    return json.dumps(res)


if __name__ == '__main__':
    app.run(debug=True, use_debugger=True)