import json

import logging
from google.appengine.runtime import DeadlineExceededError

import counter
import pages
import requesthandler
from errorline import ErrorLine
from flask import Flask, request, render_template

Flask.debug=True
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test')
def test():
    e = ErrorLine(lineString="Hola!")
    e.put()
    counter.increment(str(e.key.id()))
    return "Done"

@app.route('/errors', methods=['POST'])
def errors():
 return post_errors()

def post_errors():
    try:
        requesthandler.storeFromJson(request.get_data())
        return "OK!"
    except KeyError as e:
        return "",400
    except DeadlineExceededError as e:
        logging.warn(e)

@app.route('/errors/apps' , methods=['GET'])
def error_apps():
    return json.dumps(get_apps_count())

def get_apps_count(pagenumber=0):
    return requesthandler.getAppCount(pagenumber)


@app.route('/errors/apps/chart', methods=['GET'])
def chart():
    page = request.args.get('page')
    if not page:
        page = 0
    page = int(page)
    if page < 0:
        page = 0
    apps, page = get_apps_count(page)
    labels = apps.keys()
    values = apps.values()
    next = page+1
    previous = page-1
    if previous < 0:
        previous = 0
    return render_template('chart.html', values=values, labels=labels , page=page, next="?page=" + str(next), previous="?page=" + str(previous))





if __name__ == '__main__':
    app.run()