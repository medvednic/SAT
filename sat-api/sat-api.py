from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
collection = None


@app.route("/")
def hello():
    duration = request.args.get('duration')
    if duration is 'H':
        pass
    elif duration is 'D':
        pass
    elif duration is 'W':
        pass
    else:
        return 'Bad request, please specify H/D/W in url params', 400
    pipeline = [
        {"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}
    ]
    results = (list(collection.aggregate(pipeline)))
    return jsonify(results), 200


if __name__ == '__main__':
    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client.sat_db
    collection = db.tweet_collection
    app.run()
