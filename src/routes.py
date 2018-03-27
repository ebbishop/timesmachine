import os
from flask import Flask, send_from_directory, request, make_response
import ujson as json
import requests

APP = Flask(__name__, static_folder='../app/dist')

@APP.route('/', methods=['GET'])
def index():
  return send_from_directory(APP.static_folder, 'index.html')

@APP.route('/static/<type>/<filename>', methods=['GET'])
def send_static(type, filename):
  print(os.path.join(APP.static_folder, 'dist'))
  return send_from_directory(os.path.join(APP.static_folder, 'static', type), filename)

@APP.route('/get_articles', methods=['GET'])
def get_articles():
  params = dict(request.args)
  params['api-key'] = os.environ.get('TIMES_API_KEY')
  data = requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json', params=params).text
  return APP.response_class(
    response=data,
    status=200,
    mimetype="application/json")
