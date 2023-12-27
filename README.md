# Weather Station

DIY weather station and property monitoring (built for Raspberry Pi)

## Hardware

1. AMD based Linux machine such as Raspberry Pi (specs to come later)
1. Temp/Humidity - DHT 11
1. Snow Depth - Ultrasonic sensor (HC-SR04)

## Getting Started

1. Flash a new Raspberry Pi with raspbian
1. SSH into the Pi (i.e. `ssh pi@raspberrypi.local` unless you changed defaults)
1. Clone repo `git clone https://github.com/prescottprue/weather-station`
1. Create a new `.env` file containing DB password: `echo "MARIADB_PASS=mydbpass" > /home/pi/weather-station/.env`
1. Install git, python, and pipenv `sudo apt-get install git build-essential python-dev pipenv libgpiod2`
1. Install Maria DB:
    ```bash
    sudo apt-get install -y mariadb-server libmariadb-dev-compat libmariadb-dev
    sudo pip3 install mariadb
    ```
1. Run `pipenv install`
1. Setup SQL Database with table
    ```
    sudo mysql
    ```

    ```sql
    create user pi IDENTIFIED by 'mydbpass';
    CREATE DATABASE weather
    grant all privileges on *.* to 'pi' with grant option;
    CREATE TABLE weather.WEATHER_MEASUREMENT(
      ID BIGINT NOT NULL AUTO_INCREMENT,
      REMOTE_ID BIGINT,
      AMBIENT_TEMPERATURE DECIMAL(6,2) NOT NULL,
      HUMIDITY DECIMAL(6,2) NOT NULL,
      SNOW_DEPTH DECIMAL(6,2),
      CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY ( ID )
    );
    ```
1. To test, run API using: `python3 ./weather-station/main.py`
1. Setup and start services to run capture + API in background on boot:
    1. Copy service files into systemd folders: `cp /home/pi/weather-station/capture.service /etc/systemd/system/capture.service`
    1. Reload the daemon: `sudo systemctl daemon-reload`
    1. Enable services: `sudo systemctl enable capture.service && sudo systemctl enable api.service`
    1. Start services: `sudo systemctl start capture.service && sudo systemctl start api.service`

## My Setup

I'm currently using a Raspberry Pi 2 B, but the goal is to keep this generalized to any AMD platform running Linux

## Plans

1. Wind speed/direction
1. Rain Sensor
1. 4G modem for remote connectivity
1. Ability to expose data to HomeAssistant running in a different location (possibly RealVNC and/or Tailscale)
1. Camera
1. Motion sensor

## References

* [Raspberry Pi Org Weather station project](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station) - main reference for organization and data storage. Doesn't include networking or extra sensors.
* [Raspberry Pi Org Distance Sensor project](https://projects.raspberrypi.org/en/projects/physical-computing/12)
* [DHT11 Interfacing with Raspberry Pi](https://www.electronicwings.com/raspberry-pi/dht11-interfacing-with-raspberry-pi)
* [Setup Python script as a service through systemctl](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267)