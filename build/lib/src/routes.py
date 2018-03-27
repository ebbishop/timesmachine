import os
from flask import Flask, send_from_directory, render_template

APP = Flask(__name__, static_folder='../app/dist')

@APP.route('/', methods=['GET'])
def index():
  return send_from_directory(APP.static_folder, 'index.html')

@APP.route('/static/<filename>', methods=['GET'])
def send_static(filename):
  print(os.path.join(APP.static_folder, 'dist'))
  return send_from_directory(os.path.join(APP.static_folder, 'dist'), filename)
# def get_articles():
        # 'api-key': '93ac857a87c0496497514e971c96cf10',
#   https://api.nytimes.com/svc/search/v2/articlesearch.json
