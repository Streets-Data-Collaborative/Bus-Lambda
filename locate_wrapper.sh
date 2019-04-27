#!/bin/bash
while :
do
	location=`./locate_magic.sh "osx"`
	timestamp=`date +%s`
	macid=`ifconfig en1 | grep ether | awk '{print $2}'`

	echo $macid,$timestamp,$location
	curl -s 'https://docs.google.com/forms/d/1AnW5Oj71X2CC6hyrAYb7v805JIDnCKj23xav6Okh5KY/formResponse' --data "entry.512945646=$macid" --data "entry.1966681112=$location" >>/dev/null
	#python upload_device_data_to_db.py --device-id $macid --timestamp $timestamp --location '$location'
	sleep 30
done
