#!/usr/bin/python
import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from oauth2client import client
from config import youtube_config
import requests
import flask

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.

# Examples!
# https://developers.google.com/youtube/v3/code_samples/python#create_a_playlist
DEVELOPER_KEY = youtube_config["developerKey"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


youtube_flow = client.flow_from_clientsecrets(
    youtube_config['secretPath'],
    scope='https://www.googleapis.com/auth/youtube',
    redirect_uri='http://127.0.0.1:5000/oauth2callback')


def get_credentials_from_session():
    credentials = client.OAuth2Credentials.from_json(flask.session['youtube_credentials'])
    return credentials


def get_auth_youtube_obj():
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    http=get_credentials_from_session().authorize(httplib2.Http()))
    return youtube


def get_token(code):
    credentials = youtube_flow.step2_exchange(code)
    print('creds:')
    print(credentials.to_json())
    flask.session['youtube_credentials'] = credentials.to_json()


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
        q=options["q"],
        part="id,snippet",
        maxResults=options["max_results"]
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    return videos