# https://4x4x9a7f5a.execute-api.us-east-1.amazonaws.com/beta/time?route=A&lon=-73.8887422822949&lat=40.6452239097308

import argparse
import psycopg2
import json
from datetime import datetime
from sys import argv

def main(argv):
    print(argv)
    ### parse commandline arguments ###
    ###################################
    parser = argparse.ArgumentParser(description='parse arguments')
    parser.add_argument('--device_id', type=str, help='MAC id of the raspberry pi device')
    parser.add_argument('--timestamp', type=str, help='timestamp when the location info is sent')
    parser.add_argument('--location', type=str, help='json str containing lat and lon')
    args = vars(parser.parse_args())

    ###################################
    ###   get location information  ###
    ###################################
    location = json.loads(args['location'])
    lat = location["lat"]
    lon = location["lon"]
    print(lat,lon)

    ###################################
    ###      Convert Timestamp      ###
    ###################################

    timestamp = int(args['timestamp'])
    date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    ###################################
    ###      insert data to db      ###
    ###################################
    host = "refer lastpass"
    database = "refer lastpass"
    user = "refer lastpass"
    password = "refer lastpass"

    con = psycopg2.connect(host=host, database=database, user=user, password=password)
    cur = con.cursor()

    query = 'insert into bus.device_test (datetime, device_id, lat, lon) VALUES (%s, %s, %s, %s);'
    cur.execute(query, (date, args['device_id'], lat, lon))
    con.commit()

if __name__ == '__main__':
   if len(argv) == 7:
       main(argv)
   else:
       print('Incorrect number of Arguments')
