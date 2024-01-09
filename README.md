# Weather Station

DIY weather station and property monitoring (built for Raspberry Pi)

## Features
* Capturing of Temperature, Humidity, and Snow Depth - stored in MySQL instance
* Simple REST API for exposing captured values is great for exposing to tools like HomeAssistant (with docs about usage through VPN)
* Capture and API set up as two separate systemd services to run in the background on boot
* Github Actions Workflow for automatically publishing changes to weather station (leveraging [Tailscale's Github Action](https://github.com/tailscale/github-action) to dynamically create nodes marked as ephemeral)
* Support for 4G modem for remote connectivity

## Hardware

1. AMD based Linux Debian machine such as Raspberry Pi
1. Temp/Humidity - DHT 11
1. Snow Depth - Ultrasonic sensor (HC-SR04)
1. Raspberry Pi Camera - [Arducam IMX 477](https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/12MP-IMX477/)

### Not Required

1. [Sixfax 4G LTE Modem Hat](https://sixfab.com/product/raspberry-pi-4g-lte-modem-kit)

## Setup

1. Flash linux machine planned for the weather-station (in my case Raspberry Pi) with a Debian version of linux (NOT Bookworm)
1. SSH into the Pi (i.e. `ssh pi@raspberrypi.local` unless you changed defaults)
1. If you are using any hardware for remote connectivity such as the [Sixfab LTE hat](https://sixfab.com/product/raspberry-pi-4g-lte-modem-kit) - I've found it best to install this before any other dependencies. Follow setup instructions provided by manufacturer - otherwise skip this step.
1. Install dependencies including git, python, and maria db: `sudo apt-get install git build-essential python3 python3-pip libgpiod2 mariadb-server mariadb-client libmariadb-dev`
1. Clone repo `git clone https://github.com/prescottprue/weather-station`
1. Install python app dependencies: `pip3 install adafruit-blinka adafruit-circuitpython-dht gpiozero mariadb fastapi "uvicorn[standard]" python-dotenv`
1. Setup MySQL instance:
    1. Run `sudo mysql` all following steps will be sql commands
    1. Setup user with privileges:

        ```sql
        create user pi IDENTIFIED by 'mydbpass';
        grant all privileges on *.* to 'pi' with grant option;
        ````
    1. Create `weather` database and measurements table:

        ```sql
        CREATE DATABASE weather;
        CREATE TABLE weather.measurements(
          id BIGINT NOT NULL AUTO_INCREMENT,
          temp DECIMAL(6,2) NOT NULL,
          humidity DECIMAL(6,2) NOT NULL,
          snow_depth DECIMAL(6,2),
          created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY ( id )
        );
        ```
    1. Hit `ctrl + c` to exit mysql
1. To test API, run: `MARIADB_PASS=mydbpass python3 ./weather-station/main.py` then visit `http://raspberrypi.local:8080` (or whatever the local name or local ip address of your Pi)
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
    {
      // Define the tags which can be applied to devices and by which users.
      "tagOwners": {
        "tag:ci":   [],
        "tag:prod": [],
      },
      // Define users and devices that can use Tailscale SSH.
      "ssh": [
        // Allow all users to SSH into their own devices in check mode.
        // Comment this section out if you want to define specific restrictions.
        {
          "action": "check",
          "src":    ["autogroup:member"],
          "dst":    ["autogroup:self"],
          "users":  ["autogroup:nonroot", "root"],
        },
        // Allow all users and machines with tag:ci to ssh into machines with tag:prod (tag:ci used for machines which deploy from Github Actions)
        {
          "action": "accept",
          "src":    ["autogroup:member", "tag:ci"],
          "dst":    ["tag:prod"],
          "users":  ["autogroup:nonroot", "root", "pi"],
        },
      ],
    }
    ```

1. Add a Tailscale oAuth client with `tag:ci` - client id and secret which appear will be saved in next step
1. Set the following values within Github Actions Secrets (Settings tab of repo):

    ```
    TS_OAUTH_CLIENT_ID - Tailscale oauth client id
    TS_OAUTH_SECRET - Tailscale oauth secert
    WEATHER_STATION_TAILNET_ADDRESS - address of weather-station machine on tailnet
    ```


## Remote Network
If you plan to have your weather station on a different network (such as my situation which is a property which does not yet have internet planned to use 4G hat on PI) you can access weather-station data by setting up a VPN. I suggest Tailscale since it is so easy to set up 

Make sure you are SSHed into your weather-station then do the following:

1. Install tailscale: `curl -fsSL https://tailscale.com/install.sh | sh`
1. Start tailscale with ssh enabled `sudo tailscale up --ssh --advertise-tags tag:prod`
1. Approve machine in tailscale if needed and add the tag `prod`

## Home Assistant
Weather station data is exposed in a REST API - this makes it easy for tools like HomeAssistant to connect and pull data. 

Use the File Editor to modify your `/homeassistant/configuration.yaml` file to add the following:

**NOTE**: `$LOCAL_IP` is the local IP address of the weather station machine (raspberry pi) - this can be found by running `ifconfig` within ssh. If you are running Tailscale VPN, this should instead be your device's tailnet URL or IP.

```yaml
rest:
  # Replace $LOCAL_IP with local IP address of weather-station machine - if using Tailscale, this is Tailnet DNS entry or IP
  - resource: "http://$LOCAL_IP:8080/latest"
    sensor:
      - name: "Station Temperature"
        unique_id: station-temperature
        value_template: "{{ value_json.temp }}"
        unit_of_measurement: "°F"
        device_class: temperature

      - name: "Station Humidity"
        unique_id: station-humidity
        value_template: "{{ value_json.humidity }}"
        unit_of_measurement: "%"
        device_class: humidity

      - name: "Station Snow Depth"
        unique_id: station-snow-depth
        icon: mdi:snowflake
        value_template: "{{ value_json.snow_depth }}"
        unit_of_measurement: "in"
        device_class: distance
        
      - name: "Station Last Capture"
        unique_id: station-last-capture
        icon: mdi:clock
        value_template: "{{ as_datetime(value_json.created).astimezone() }}"
        device_class: timestamp
```

### Remote Home Assistant

If you are running your weather station on a different network than you home assistant instance, you will need to setup Tailscale on your weather-station machine (super easy - see [Remote Network section](#remote-network) above) as well as install [@tsujamin's Home Assistant Tailscale addon](https://github.com/tsujamin/hass-addons) (Tailscale addon in store did allow rest connection to access Tailnet).

1. Go to Add On Store
1. Click "Add Repository"
1. Add `https://github.com/tsujamin/hass-addons` repo url
1. Add "Tailscale" addon from under the `tsujamin's Add-ons` section
1. Create a new auth key in Tailscale UI
1. Set auth key from Tailscale UI in configuration panel of Tailscale addon and disable `userspace_networking` (this is important!)
1. Save configuration then start Tailscale addon (and make sure `Start on boot` is enabled)


## My Setup

I'm currently using a Raspberry Pi 4 since I plan to add a 4G Hat, but the goal is to keep most of the project generalized to any AMD platform running Linux

## Plans

1. Wind speed/direction
1. Rain Sensor
1. Camera
1. Motion sensor
1. Publishing/sharing to weather authority
1. Support Bookworm OS version by using python virtual env
1. Pipenv or similar for dependency management

## Why

### Capture on a cycle instead of on API call?

* Continue to capture data to machine's memory even if it is offline allowing for later review
* Data pulling can be optimized for network conditions (not necessarily all captures will go over the network)

## References

* [Raspberry Pi Org Weather station project](https://projects.raspberrypi.org/en/projects/build-your-own-weather-station) - main reference for organization and data storage. Doesn't include networking or extra sensors.
* [Raspberry Pi Org Distance Sensor project](https://projects.raspberrypi.org/en/projects/physical-computing/12)
* [DHT11 Interfacing with Raspberry Pi](https://www.electronicwings.com/raspberry-pi/dht11-interfacing-with-raspberry-pi)
* [Setup Python script as a service through systemctl](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267)
* [@tsujamin's Home Assistant Tailscale addon](https://github.com/tsujamin/hass-addons)
