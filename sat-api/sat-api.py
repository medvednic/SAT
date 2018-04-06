import datetime

from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

collection = None


def group_by_sentiment(span):
    current_time_s = int(datetime.datetime.now().strftime('%s'))
    if span == 'H':
        diff = 3600
    elif span == 'D':
        diff = 3600 * 24
    elif span == 'W':
        diff = 3600 * 24 * 7
    else:
        return 'Bad request, please specify H/D/W in url params', 400
    max_date = datetime.datetime.fromtimestamp(current_time_s, None)
    time_lower_lim_s = current_time_s - diff
    min_date = datetime.datetime.fromtimestamp(time_lower_lim_s, None)
    pipeline = [
        {
            "$match":
                {
                    "created_at":
                        {"$gte": min_date, "$lte": max_date}
                }
        },
        {
            "$group":
                {
                    "_id": "$sentiment",
                    "count": {"$sum": 1}
                }
        }
    ]
    return list(collection.aggregate(pipeline))


@app.route("/distribution")
def tweet_distribution():
    span = str(request.args.get('span')).upper()
    results = group_by_sentiment(span)
    return jsonify(results), 200


if __name__ == '__main__':
    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client.sat_db
    collection = db.tweet_collection
    app.run()
