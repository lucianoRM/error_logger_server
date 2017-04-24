import json
import logging

import datetime
import time

from google.appengine.api.taskqueue import taskqueue
from google.appengine.runtime import DeadlineExceededError
import config.config

import counter
import errorline
import requesthandler
from errorline import ErrorLine
from flask import Flask, request, render_template

Flask.debug=True
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/errors', methods=['POST'])
def post_errors():
    try:
        requesthandler.storeFromJson(request.get_data())
        return "OK!", 200
    except KeyError as e:
        return "", 400
    except DeadlineExceededError as e:
        logging.warn(e)


@app.route('/test',methods=['POST'])
def test():
    jsonObject = json.loads(request.get_data())
    print jsonObject
    return "ok"

@app.route('/errors/tasks/ranking', methods=['POST','GET'])
def rank_errors():
    cursor = request.args.get('cursor')
    cursor, more = requesthandler.handlecron(cursor)
    if cursor and more:
        taskqueue.add(url=request.path, params={'cursor' : cursor})
    return "OK",200

@app.route('/errors/lines/ranking')
def get_top():
    date = request.args.get('date')
    (top, timeInterval) = requesthandler.getTop(date)
    print top
    labels = [key.split("-")[0] for key in top.keys()]
    values = top.values()
    toDate = datetime.datetime.utcfromtimestamp(timeInterval + config.config.top_reset_time())
    return render_template('ranking.html', values=values, labels=labels,
                           fromDate=datetime.datetime.utcfromtimestamp(timeInterval),
                           toDate=toDate, previous="?date=" + str(datetime.datetime.utcfromtimestamp(timeInterval - config.config.top_reset_time()).strftime('%Y%m%d%H%M%S')), next="?date=" + str(toDate.strftime('%Y%m%d%H%M%S')))

def get_apps_count(date,pagenumber):
    return requesthandler.getAppCount(date,pagenumber)


@app.route('/errors/apps/chart', methods=['GET'])
def chart():
    page = request.args.get('page')
    date = request.args.get('date')
    if not page:
        page = 0
    page = int(page)
    if page < 0:
        page = 0
    if not date:
        date = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    apps, page, timeInterval = get_apps_count(date,page)
    labels = [app.split("-")[0] for app in apps.keys()]
    values = apps.values()
    next = page+1
    previous = page-1
    if previous < 0:
        previous = 0
    date = datetime.datetime.utcfromtimestamp(timeInterval).strftime('%Y%m%d%H%M%S')
    toDate = datetime.datetime.utcfromtimestamp(timeInterval + config.config.chart_reset_time())
    return render_template('chart.html', values=values, labels=labels , page=page, next="?date=" + date + "&page=" + str(next), previous="?date=" + date + "&page=" + str(previous), date= datetime.datetime.strptime(date, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S'), toDate=toDate, previousDate="?date=" + str(datetime.datetime.utcfromtimestamp(timeInterval - config.config.chart_reset_time()).strftime('%Y%m%d%H%M%S')), nextDate="?date=" + str(toDate.strftime('%Y%m%d%H%M%S')))





if __name__ == '__main__':
    app.run()