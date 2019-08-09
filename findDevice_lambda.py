from datetime import datetime
import os
import psycopg2
from botocore.vendored import requests
import json



def lambda_handler(event, context):
    con = None
    # querytext = ('''SELECT datetime AS recenttime, ST_X(geom) as back_lon, ST_Y(geom) as back_lat, device_id
    #     FROM bus.device_test
    #     WHERE ST_Distance_Sphere(geom, ST_MakePoint({0},{1})) <= 3 * 1609.34 
    #     AND datetime >= now()::timestamp - interval '15 minutes'
    #     ORDER BY recenttime DESC
    #     LIMIT 20;'''.format(event['lon'], event['lat']))

    querytext = ('''SELECT datetime AS recenttime, ST_X(geom) as back_lon, ST_Y(geom) as back_lat, device_id 
        FROM bus.device_test
        WHERE ST_Distance_Sphere(geom, ST_MakePoint({0},{1})) <= 3 * 1609.34 
        AND datetime >= now()::timestamp - interval '10 days'
        ORDER BY recenttime DESC
        LIMIT 5;'''.format(event['lon'], event['lat']))
    
    # querytext = ('''SELECT datetime AS recenttime,
    # ST_X(ST_ClosestPoint(geom, ST_GeomFromText('Point({0} {1})', 4326))) AS pointLon, 
    # ST_Y(ST_ClosestPoint(geom, ST_GeomFromText('Point({0} {1})', 4326))) AS pointLat, 
    # device_id
    # FROM bus.device_test 
    # ORDER BY recenttime DESC 
    # LIMIT 1;'''.format(event['lon'], event['lat']))

    # print('Time of user query: {}'.format(str(datetime.now())))
    # print(event)

    try:
        
        host = "last_pass"
        database = "last_pass"
        user = "last_pass"
        password = "last_pass"

        con = psycopg2.connect(host=host, database=database, user=user, password=password)
        cur = con.cursor()
        cur.execute(querytext)
        rows = cur.fetchall()
        con.commit()
        # print(rows)
        # back_time = rows[0][0]
        # back_lon = str(rows[0][1])
        # back_lat = str(rows[0][2])
        # back_device = rows[0][3]
        # print(back_lat, back_lon)
        # print(back_time)
        # print(datetime.now().date())
        # print("This location information was in database " + str(datetime.now()-back_time) + " before.")

        # API_KEY = 'AIzaSyDDD_l2yX8BhAQPlfQ5JY0-xNTlNcUvrT8' #'AIzaSyCxwq4vjIeGPeXpWdWoKWhf2AZ_jmfwfJo'
        # url = ('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&' +
        #       'origins=' + str(event['lat']) + ',' + str(event['lon']) + '&destinations=' +
        #        str(back_lat) + ',' + str(back_lon) + '&key=' + str(API_KEY))

        # req = requests.get(url)
        # time_result = req.json()['rows'][0]['elements'][0]['duration']['text']
        # return {'back_loc': str(back_lat)+","+str(back_lon),'bus_Time': str(back_time),'expected_time': time_result, 'device': back_device}
        #return event
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
