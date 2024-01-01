# Weather Station

DIY weather station and property monitoring (built for Raspberry Pi)

## Features
* Capturing of Temperature, Humidity, and Snow Depth - stored in MySQL instance
* Simple REST API for exposing captured values is great for exposing to tools like HomeAssistant (with docs about usage through VPN)
* Capture and API set up as two separate systemd services to run in the background on boot
* Github Actions Workflow for automatically publishing changes to weather station (leveraging [Tailscale's Github Action](https://github.com/tailscale/github-action) to dynamically create nodes marked as ephemeral)

## Hardware

1. AMD based Linux Debian machine such as Raspberry Pi
1. Temp/Humidity - DHT 11
1. Snow Depth - Ultrasonic sensor (HC-SR04)

## Setup

1. Flash linux machine planned for the weather-station (in my case Raspberry Pi) with a Debian version of linux (NOT Bookworm)
1. SSH into the Pi (i.e. `ssh pi@raspberrypi.local` unless you changed defaults)
1. Install dependencies inluding git, python, and maria db: `sudo apt-get install git build-essential python3 python3-pip libgpiod2 mariadb-server`
1. Clone repo `git clone https://github.com/prescottprue/weather-station`
1. Install python app dependencies: `pip3 install adafruit-blinka adafruit-circuitpython-dht gpiozero mariadb fastapi "uvicorn[standard]"`
1. Setup user with privileges, create `weather` database, and create `measurements` table:

    ```sql
    create user pi IDENTIFIED by 'mydbpass';
    CREATE DATABASE weather;
    grant all privileges on *.* to 'pi' with grant option;
    CREATE TABLE weather.measurements(
      id BIGINT NOT NULL AUTO_INCREMENT,
      remote_id BIGINT,
      ambient_temperature DECIMAL(6,2) NOT NULL,
      humidity DECIMAL(6,2) NOT NULL,
      snow_depth DECIMAL(6,2),
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY ( id )
    );
    ```
1. To test, run API using: `MARIADB_PASS=mydbpass pipenv run ./weather-station/main.py`
1. Setup and start services to run capture + API in background on boot:
    1. Write a file containing DB password you picked above (note `tee` is to prevent permission issues): `echo "MARIADB_PASS=mydbpass" | sudo tee -a /etc/environment >/dev/null`
    1. Copy service files into systemd folders: `sudo cp /home/pi/weather-station/services/weather-capture.service /etc/systemd/system/weather-capture.service && sudo cp /home/pi/weather-station/services/weather-api.service /etc/systemd/system/weather-api.service`
    1. Reload the daemon: `sudo systemctl daemon-reload`
    1. Enable services: `sudo systemctl enable weather-capture.service && sudo systemctl enable weather-api.service`
    1. Start services: `sudo systemctl start weather-capture.service && sudo systemctl start weather-api.service`

### Github Actions
To set up your weather-station code to update automatically when you push changes:

1. Fork this repo
1. Follow section below about setup of Tailscale
1. Add the following to Tailscale Access Controls:

    ```json
      "tagOwners": {
        "tag:ci": [],
      },
    ```
1. Add a Tailscale oAuth client with `tag:ci` - client id and secret which appear will be saved in next step
1. Set the following values within Github Actions Secrets (Settings tab of repo):
    ```
    TS_OAUTH_CLIENT_ID - Tailscale oauth client id
    TS_OAUTH_SECRET - Tailscale oauth secert
    MARIADB_PASS - password of mariadb user (set to env file)
    WEATHER_STATION_TAILNET_ADDRESS - address of weather-station machine on tailnet
    ```

## Home Assistant
Weather station data is exposed in a REST API - this makes it easy for tools like HomeAssistant to connect and pull data. **NOTE:** If you are running your weather station on a different network than you home assistant instance, you will need to setup Tailscale (super easy - see section below)

Use the File Editor to modify your `/homeassistant/configuration.yaml` file to add the following:

**NOTE**: `$LOCAL_IP` is the local IP address of the weather station machine (raspberry pi) - this can be found by running `ifconfig` within ssh. If you are running Tailscale VPN, this should instead be your device's tailnet URL or IP.

```yaml
rest:
  - resource: "http://$LOCAL_IP:8080/measurements"
    sensor:
      - name: "Station Temperature"
        unique_id: station-temperature
        value_template: "{{ value_json.0.ambient_temperature }}"
        unit_of_measurement: "°F"
        device_class: temperature

      - name: "Station Humidity"
        unique_id: station-humidity
        value_template: "{{ value_json.0.humidity }}"
        unit_of_measurement: "%"
        device_class: humidity

      - name: "Station Snow Depth"
        unique_id: station-snow-depth
        icon: mdi:snowflake
        value_template: "{{ value_json.0.snow_depth }}"
        unit_of_measurement: "in"
        device_class: distance
        
      - name: "Station Last Capture"
        unique_id: station-last-capture
        icon: mdi:clock
        value_template: "{{ as_datetime(value_json.0.created_at).astimezone() }}"
        device_class: timestamp

```

## Remote Network
If you plan to have your weather station on a different network (such as my situation which is a property which does not yet have internet planned to use 4G hat on PI) you can access weather-station data by setting up a VPN. I suggest Tailscale since it is so easy to set up 

Make sure you are SSHed into your weather-station then do the following:

1. Install tailscale: `curl -fsSL https://tailscale.com/install.sh | sh`
1. Start tailscale with ssh enabled `tailscale up --ssh`

## My Setup

I'm currently using a Raspberry Pi 4 since I plan to add a 4G Hat, but the goal is to keep most of the project generalized to any AMD platform running Linux

## Plans

1. Wind speed/direction
1. Rain Sensor
1. 4G modem for remote connectivity
1. Camera
1. Motion sensor
1. Publishing/sharing to weather authority
1. Support Bookworm OS version by using python virtual env
1. Pipenv or similar for dependency management

## References

* [Raspberry Pi Org Weather station project](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station) - main reference for organization and data storage. Doesn't include networking or extra sensors.
* [Raspberry Pi Org Distance Sensor project](https://projects.raspberrypi.org/en/projects/physical-computing/12)
* [DHT11 Interfacing with Raspberry Pi](https://www.electronicwings.com/raspberry-pi/dht11-interfacing-with-raspberry-pi)
* [Setup Python script as a service through systemctl](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267)