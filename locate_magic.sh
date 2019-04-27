#!/bin/bash
platform=$1
token="982feb449d8a86"
if [ "$platform" = "osx" ]; then
                list=($(/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s |  egrep -o '([a-f0-9]{2}:){5}[a-f0-9]{2}'))
        elif [ "$platform" = "linux" ]; then
                interface=($(ifconfig | grep wlan | awk '{print $1}' | tr -d :))
                list=($(iwlist "$interface" scanning | grep Address | awk '{print $5}'))
        else
                echo "Invalid platform / OS selected.. Proceeding with IP address based location"
                list[0]=""
        fi

        if [[ ! $list ]]; then
                echo "Wifi is disabled or there are no WiFis nearby. Proceeding with IP address based location"
                list[0]=""
        fi

for i in "${list[@]}"
        do
           comm_wifi+="{\"bssid\": \"$i\"},"
        done

comm_wifi=$(sed "s/.$//g" <<< $comm_wifi)
curl_comm="{\"token\": \"$token\",\"wifi\": ["$comm_wifi"],\"address\": 1}"
#echo $curl_comm
curl --request POST --silent --url https://us1.unwiredlabs.com/v2/process.php --data "$curl_comm"
