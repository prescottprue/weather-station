# Weather Station

DIY weather station and property monitoring (built for Raspberry Pi)

## Hardware

1. AMD based Linux machine such as Raspberry Pi (specs to come later)
1. Temp/Humidity - DHT 11
1. Snow Depth - Ultrasonic sensor (HC-SR04)

## My Setup

I'm currently using a Raspberry Pi 2 B, but the goal is to keep this generalized to any AMD platform running Linux

## Plans
1. Wind speed/direction
1. Rain Sensor
1. Local storage of data coming from sensors
1. 4G modem for remote connectivity
1. Ability to expose data to HomeAssistant running in a different location (most likely Tailscale)

## References
* [Raspberry Pi Org Weather station project](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station) - main reference for organization and data storage. Doesn't include networking or extra sensors.
* [Raspberry Pi Org Distance Sensor project](https://projects.raspberrypi.org/en/projects/physical-computing/12)

