import argparse
import psycopg2
import json
from datetime import datetime

def main():
    ###################################
    ### parse commandline arguments ###
    ###################################
    parser = argparse.ArgumentParser(description='parse arguments')
    parser.add_argument('--device_id', type=str, help='MAC id of the raspberry pi device')
    parser.add_argument('--timestamp', type=str, help='timestamp when the location info is sent')
    parser.add_argument('--location', type=str, help='json str containing lat and lon')
    args = vars(parser.parse_args())
    print(args)

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
    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print(date)

    ###################################
    ###      insert data to db      ###
    ###################################
    host = "buslambda2.c8idj0wb3ddk.us-east-1.rds.amazonaws.com"
    database = "buslambda"
    user = "argomaster"
    password = "xAb513GKHpyf92F6"


    con = psycopg2.connect(host=host, database=database, user=user, password=password)
    cur = con.cursor()

    query = '''insert into bus.device_test (datetime, device_id, lat, lon) VALUES (%s, %s, %s, %s);'''
    cur.execute(query, (str(date), args['device_id'], lat, lon))
    cur.execute('''update bus.device_test set geom=st_SetSrid(st_MakePoint(cast(lon as float), cast(lat as float)), 4326);''')

    con.commit()



if __name__ == '__main__':
   main()
