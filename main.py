import json

import logging
from google.appengine.runtime import DeadlineExceededError

import counter
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

def get_apps_count(app=None):
    return requesthandler.getAppCount(app)


@app.route('/errors/apps/chart', methods=['GET'])
def chart():
    apps = get_apps_count()
    labels = apps.keys()
    values = apps.values()
    return render_template('chart.html', values=values, labels=labels)





if __name__ == '__main__':
    app.run()
