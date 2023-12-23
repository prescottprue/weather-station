import time
import mariadb
from tempAndHumidity import getTempAndHumidity, dhtDevice
from snowDepth import getSnowDepth

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="pi",
        password="my54cr4t",
        host="localhost",
        port=3306,
        database="weather"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


while True:
  try:
    temperature_f, humidity = getTempAndHumidity()
    snowDepth = getSnowDepth()
    cur.execute(
    "INSERT INTO weather (AMBIENT_TEMPERATURE,HUMIDITY) VALUES (?, ?)"
    (temperature_f, humidity))
    print("after insert")
  except RuntimeError as error:
      # Errors happen fairly often, DHT's are hard to read, just keep going
      print(error.args[0])
      time.sleep(2.0)
      continue
  except Exception as error:
      dhtDevice.exit()
      raise error

  time.sleep(2.0)