#!/bin/bash
nohup python producer.py &
nohup python consumer.py &
nohup python sat-api.py
