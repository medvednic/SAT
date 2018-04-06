import datetime

from flask import Flask, jsonify, request

from services import get_db_collection

"""
API - flask app, allows performing HTTP requests to get tweets distribution by sentiment over spans of time (H/D/W).
the app is connected to the same DB which the consumer writes into. 
"""

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

    # perform aggregation query on tweets in date range (group by sentiment)
    results = list(collection.aggregate(pipeline))

    response_body = {
            "from": min_date,
            "to": max_date,
            "tweet-distribution": results
    }
    return response_body


# get tweet sentiment distribution for specific time span (h/d/w)
@app.route("/distribution/byspan")
def tweet_distribution_by_span():
    span = str(request.args.get('span')).upper()
    results = group_by_sentiment(span)
    return jsonify(results), 200


# get tweet sentiment distribution for all time spans (h/d/w)
@app.route("/distribution")
def tweet_distribution_all():
    results = list(map(lambda s: group_by_sentiment(s), ['H', 'D', 'W']))
    return jsonify(results), 200


if __name__ == '__main__':
    collection = get_db_collection('localhost', 27017, 'sat_db', 'tweet_collection')
    app.run()
