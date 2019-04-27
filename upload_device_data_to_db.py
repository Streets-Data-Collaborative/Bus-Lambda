import argparse
import psycopg2
import json


def main():
    ###################################
    ### parse commandline arguments ###
    ###################################
    parser = argparse.ArgumentParser(description='parse arguments')
    parser.add_argument('--device_id', type=str, help='MAC id of the raspberry pi device')
    parser.add_argument('--timestamp', type=str, help='timestamp when the location info is sent')
    parser.add_argument('--location', type=str, help='json str containing lat and lon')
    args = vars(parser.parse_args())
    print args

    ###################################
    ###   get location information  ###
    ###################################
    location = json.loads(args['location'])
    lat = location['lat']
    lon = location['lon']
    print lat,lon

    ###################################
    ###      insert data to db      ###
    ###################################
    host = "refer lastpass"
    database = "refer lastpass"
    user = "refer lastpass"
    password = "refer lastpass"

    con = psycopg2.connect(host=host, database=database, user=user, password=password)
    cur = con.cursor()

    query = 'insert into bus.device (datetime, device_id, lat, lon) VALUES (%s, %s, %s, %s);'
    cur.execute(query, (args['timestamp'], args['device_id'], lat, lon))
    con.commit()

if __name__ == '__main__':
   main()
