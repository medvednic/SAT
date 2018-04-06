# SAT

Twitter Sentiment Analysis Tool

##  Design

This tool consumes the Twitter Streaming API according to predifined keywords, determines the sentiment of incoming
tweets, and allows a user to view statistics regarding the sentiment of the collected tweets.

The application is built from 5 components:

1. Producer - subscribes to Twitter stream API and publishes incoming tweets to a message broker.
2. Consumer - recives tweets from the message broker and determines their sentiment using TextBlob, 
the tweets are saved in a DB after being processed.
3. Message broker - RabbitMQ.
4. DB - MongoDB.
5. SAT-API - simple flask REST-API which allows querying the DB.

## Prerequisites

Twitter API key and token as ```twiter-api-credentials.json``` file in ```config``` directory.
```javascript
{
  "consumer-key":{
    "key":"your-key",
    "secret":"your-secret"
  },
  "access-token":{
    "token":"your-access-token",
    "secret":"your-token-secret"
  }
}
```
Set keywords, hashtags and handles in ```config/person-config.json```. this will
determine which tweets will be pushed from the streaming API, the default is:
```javascript
{
  "keywords":[
    "Donald Trump",
    "Trump",
    "#potus",
    "@therealdonalntrump"
  ]
}
```

Since ther are two ways to deploy the app, the prerequisites depend on the deployment way of choice:
#### The convinient way - using Docker
  * Docker 18.*
  * Docker-Compose 1.20.*
    
#### Local deployement
  * Python 3
  * pip
  * MongoDB
  * RabbitMQ 

## Deployement
#### Using Docker
1. open a terminal in the project's directory
2. in the terminal enter: ```docker-compose up --build``` (```sudo``` maybe required)

The app image will be built and there should be three containers running:
* sat
* mongo
* rabbitmq

#### Local deployment
1. go to ```config/hosts.json``` and change ```"env":"docker"``` to ```"env":"local"``` 
(hosts differ bewteen Docker and local deployement)
2. open a terminal in the project's directory and run the following commands (```sudo``` maybe required for pip):
```
  pip install -r requirements.txt
  python -m textblob.download_corpora
  python producer.py
  python consumer.py
  python sat-api.py
```
## Usage

open your browser and enter the url ```http://localhost:5000/distribution```, you should get the a response
of the following structure, with tweet distribution by sentiment and date ranges (last hour, day, and week):

```javascript
{
  "from": "Fri, 06 Apr 2018 12:55:52 GMT",
  "to": "Fri, 06 Apr 2018 13:55:52 GMT",
  "tweet-distribution": [
    {
      "_id": "negative",
      "count": 2211
    },
    {
      "_id": "positive",
      "count": 2966
    },
    {
      "_id": "neutral",
      "count": 4062
    }, ...
  ]
}
```

you can also use ```http://localhost:5000/distribution/byspan?span=W``` to get data
of tweets in range of hour, day or week (H,D,W).

## Some points
* Front-end was left out, but should be quite trivial using a modern js framework.
* Python was chosen due to low development overhead
* For a bigger project
  * allow keyword configuration in runtime per user
  * fine tune message broker
  * DB authentication
