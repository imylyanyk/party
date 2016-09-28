from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import pyrebase
from googleapiclient.errors import HttpError
import auth
from config import firebase_config, youtube_config
from youtube_helpers import youtube_flow, get_token, get_auth_youtube_obj
# How to !
# https://www.digitalocean.com/community/tutorials/how-to-structure-large-flask-applications

import youtube_helpers as yt
import json

app = Flask(__name__)
app.register_blueprint(auth.app)

firebase = pyrebase.initialize_app(firebase_config)


@app.route('/')
def hello_world():
    auth_url = youtube_flow.step1_get_authorize_url()
    return render_template("index.html", youtube_auth=auth_url)


@app.route('/name/<name>')
def index_name(name):
    cur_party = 1
    songs = firebase.database().child('parties/0/songs').get()
    songs = songs.val()
    return render_template("name.html", name=name, songs=songs)


@app.route('/dashboard')
def dashboard():
    yt = get_auth_youtube_obj()
    data = yt.channels().list(part='snippet', mine=True).execute()
    name = data['items'][0]['snippet']['title']
    print(name)
    return render_template('dashboard.html', name = name)


@app.route('/oauth2callback')
def handle_auth():
    get_token(request.args.get('code'))
    return redirect(url_for('dashboard'))


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
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.run(debug=True, use_debugger=True)