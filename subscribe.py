#Basic imports
import sys
import math
import random
import os
import time
import datetime
import redis
import string
import csv


# gets a valid message

def get_message():
    while True:
        temp = pubsub.get_message()
        if (temp is not None):
            return temp

def read_message():

    timestamp = get_message()
    if (timestamp['channel'] == 'timestamp'):
        timestamp = timestamp['data']
        print timestamp
        temperature = get_message()['data']
        print temperature
        pressure = get_message()['data']
        print pressure
        humidity = get_message()['data']
        print humidity

        return timestamp, temperature, pressure, humidity


# file paths
directory_name = "/var/www/html/data/MOL-lab/"

# connect to the Rasperry Pi Redis server
r = redis.StrictRedis(host='192.168.1.65', port=6379, db=0)

# open up a pubsub instance
pubsub = r.pubsub(ignore_subscribe_messages=True)

pubsub.subscribe('timestamp')
pubsub.subscribe('temperature')
pubsub.subscribe('pressure')
pubsub.subscribe('humidity')


# main loop

while True:

# make sure we get the messages in the right order
    

        timestamp, temperature, pressure, humidity = read_message()

        if(timestamp != None):
            # open file for writing
            file_name = (time.strftime("%Y-%m-%d")) + ".csv"
            
            if not os.path.exists(directory_name):
                    os.makedirs(directory_name)

            file_path = directory_name + file_name

            data_file = open(file_path, "ab")
            file_writer = csv.writer(data_file)
            file_writer.writerow([timestamp, temperature, pressure, humidity]) 
            data_file.close()
