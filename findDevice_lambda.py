from datetime import datetime
import os
import psycopg2
from botocore.vendored import requests
import json



def lambda_handler(event, context):
    con = None
    #https://stackoverflow.com/questions/3800551/select-first-row-in-each-group-by-group
    # querytext = ('''SELECT DISTINCT ON (device_id)
    #  datetime AS recenttime, ST_X(geom) as back_lon, ST_Y(geom) as back_lat, device_id
    #  FROM bus.device_test
    #  WHERE ST_Distance_Sphere(geom, ST_MakePoint({0},{1})) <= 3 * 1609.34
    #  AND datetime >= now()::timestamp - interval '15 minutes'
    #  ORDER  BY device_id, recenttime DESC
    #  LIMIT 20;'''.format(event['lon'], event['lat']))

    querytext = ('''SELECT DISTINCT ON (device_id)
     datetime AS recenttime, ST_X(geom) as back_lon, ST_Y(geom) as back_lat, device_id
     FROM   bus.device_test
     WHERE ST_Distance_Sphere(geom, ST_MakePoint({0},{1})) > 0.1 * 1609.34
     AND ST_Distance_Sphere(geom, ST_MakePoint({0},{1})) <= 10 * 1609.34
     AND datetime >= now()::timestamp - interval '10 days'
     ORDER  BY device_id, recenttime DESC
     LIMIT 5;'''.format(event['lon'], event['lat']))

    try:

        host = 'last_pass'
        database = 'last_pass'
        user = 'last_pass'
        password = 'last_pass'

        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cur = con.cursor()
        cur.execute(querytext)
        rows = cur.fetchall()
        con.commit()

        API_KEY = 'last_pass'
        final_response = {"buses":[]}
        for entry in rows:
            url = ('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&' +
              'origins=' + str(event['lat']) + ',' + str(event['lon']) + '&destinations=' +
               str(entry[2]) + ',' + str(entry[1]) + '&key=' + str(API_KEY))
            print(url)
            back_time = entry[0]
            back_lon = str(entry[1])
            back_lat = str(entry[2])
            back_device = entry[3]

            req = requests.get(url)
            time_result = req.json()['rows'][0]['elements'][0]['duration']['text']
            response =  {'back_loc': str(back_lat)+","+str(back_lon),
                         'bus_Time': str(back_time),
                         'expected_time': time_result,
                         'device': back_device}
            final_response['buses'].append(response)
        return final_response

    except psycopg2.DatabaseError as e:
        print('Error: {}'.format(e))
        con.rollback()
        raise
    else:
        print('done!')
    finally:
        print('completed at {}'.format(str(datetime.now())))
        if con:
            con.close()
