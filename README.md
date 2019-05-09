# Bus-Lambda
Low-cost, real time tracking of buses.

## Why


![ Growing up in India, Varun would often find himself in these situations ](https://wricitieshub.org/sites/default/files/image4.jpg)

Growing up in India, [Varun](https://uploads.knightlab.com/storymapjs/158f477ab79c7702de8c33b817ddae41/varun-resume/index.html) would often find himself in these situations. In a country where public resources are either constrained or misallocated, simply knowing how far the next bus is could play a small part in improving the overall tranist experience and mitigate the overcrowding of buses that could lead to life-threating situations. 

Access to real-time transit information has been linked to  [overall satisfaction with transit service](http://trrjournalonline.trb.org/doi/abs/10.3141/2082-13), [increases in ridership](http://www.sciencedirect.com/science/article/pii/S0968090X12000022), and  [substantial increases in farebox revenue](http://www.sciencedirect.com/science/article/pii/S0968090X15000297). 

If cities could simply increase practical availability to transit information, they could achieve outcomes similar to increases in transit service itself. 

Encouragingly, this missing layer of coordination between providers and users amounts to a conceptually simple piece of technology.

Less encouragingly, the legacy technology in this space can be exorbitantly expensive. NYC’s bus-tracking GPS system has been quoted at many thousands of $dollars per bus. After a protracted 3 year deployment process, Melbourne, a moderately-sized city, was forced to  [suspend rollout](https://www.streetsdatacollaborative.org/technical-overview/[https://www.itnews.com.au/news/melbourne-takes-second-stab-at-gps-bus-tracking-381093) of it’s original bus-tracking system in 2013 at only 30% coverage due to unreasonable operating costs. While all cities and citizens could benefit from a real-time transit information system in principle, this is not an option for all cities in practice. As forward-looking municipalities, we have to find a new approach.

Simple microcomputers with internet access enable wifi-positioning at the accuracy of a few meters at costs orders of magnitude cheaper than legacy GPS systems.

## What

This project combines the following to realize a low-cost kit to instrument any bus in an urban area across the world: 
- A $10 Raspberry Pi Zero W
- A $30 wireless hotspot with the cheapest data plan
- Wifi Positioning system using locationmagic.org
- A postgres database hosted on Amazon Web Services (AWS)
- AWS Lambda functions to trigger requests from client application
- A simple Javascript front end that requests where the nearest buses are.

![ A $10 Raspberry Pi Zero is a fully-functional wifi-equipped computer capable of retrieving its location. ](https://static1.squarespace.com/static/59948729a803bbad877d588e/t/5997b872f14aa1178c60949c/1503115399348/raspberry-pi-zero-w-wireless-256x256.png?format=1500w)

A $10 Raspberry Pi Zero is a fully-functional wifi-equipped computer capable of retrieving its location.

![ A recent ride on a New York City bus using the Raspberry Pi device and Wifi-positioning to retrieve the bus's location. A citywide system can be built to develop real time bus schedule infrastructure at the fraction of what it costs today. ](https://static1.squarespace.com/static/59948729a803bbad877d588e/t/5997b8bdf14aa1178c609703/1503115491956/bustime.jpg?format=1500w)

A recent ride on a New York City bus using the $10 Raspberry Pi device and Wifi-positioning to retrieve the bus's location. A citywide system can be built to develop real time bus schedule infrastructure at the fraction of what it costs today.

## Who
- Varun Adibhatla
- David Marulli
- Lingyi Zhang
- Xia Wang
- Vishwajeet Shelar
- Please create an [issue](https://github.com/vr00n/Bus-Lambda/issues) if you would like to contribute to this project.


## How
- **Device**: A simple, reliable, and weather resistant hardware that connects to the Internet, request its location from locationmagic.org, and sends its location `DEVICE_LOCATION` every "n" seconds to a cloud-hosted postgres database.
- **Backend**: A `postgres database` with appropriate tables to receive real-time device data along with static bus stop and route data. A simple query should allow for the display of the required information to to be displayed on a static frontend page.
- **Frontend**: A static single page application that can run on any smartphone. The page would request the user's current location and upon receiving it, send the `CLIENT_LOCATION` as a payload to an API endpoint.
- **Endpoint**: An API endpoint that receives the `CLIENT_LOCATION` and returns top-n `DEVICE_LOCATIONs` closest to it at `TIME t` via a simple postgres spatial query. At the moment, we use AWS Lambda functions connected to an API Gateway to achieve this.

## What

### locate_magic.sh (Device)
This script will run on a Raspberry Pi and obtain its location by pinging WIFI routers around it and sending it to an external service called Location Magic maintained by Unwired Labs. 
Usage:
- Obtain a token from locationmagic.org
- if OSX `./locate_magic.sh osx` should return your current location.
- if linux `./locate_magic.sh linux` should return your current location.

### findDevice_lambda.py (Backend)
This is a script that runs on Amazon Web Services. It uses the [Google Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/start) to compute the distance between the client and the nearest bus.


### client-location-page.html (Front End)
This static page is hosted on http://vr00n.github.io/Bus-Lambda and requests your current location. The intention is to send your current location to an API endpoint that returns the top-n nearest buses.

Usage: 
- In the same directory as the html file `python -m SimpleHTTPServer 8888` will create a local webserver
- Open a new browser window and type `http://localhost:8888/`.
- Click on `client-location-page.html`
- The page should ask you to `Allow for Location`. Please allow.
- The page should then return your current location.


### Further Reading


-   [Real-Time Transit Data Is Good for People and Cities. What’s Holding This Technology Back?  **World Resources Institute, February 2016**](http://www.wri.org/blog/2016/02/real-time-transit-data-good-people-and-cities-whats-holding-technology-back).
-   [The Impact Of Real-Time Information On Bus Ridership In New York City. Brakewood et. al. **ScienceDirect. 2017.**](http://www.sciencedirect.com/science/article/pii/S0968090X15000297.)
-   [Ridership Effects Of Real-Time Bus Information System: A Case Study In The City Of Chicago.  **Tang et. al. Sciencedirect 2017.**](http://www.sciencedirect.com/science/article/pii/S0968090X12000022.)
-   [Examination Of Traveler Responses To Real-Time Information About Bus Arrivals Using Panel Data |  **Transportation Research Record: Journal Of The Transportation Research Board". 2017.**](http://trrjournalonline.trb.org/doi/abs/10.3141/2082-13.)

