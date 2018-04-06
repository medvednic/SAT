#!/bin/bash
sudo pip install -r requirements.txt
python -m textblob.download_corpora
python sentiment-analysis/producer.py &
python sentiment-analysis/consumer.py &
python sat-api/sat-api.py &
