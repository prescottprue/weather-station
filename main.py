import time
import database
from tempAndHumidity import getTempAndHumidity, dhtDevice
from snowDepth import getSnowDepth

db = database.weather_database()

while True:
  try:
    temperature_f, humidity = getTempAndHumidity()
    snowDepth = getSnowDepth()
    db.insert(snowDepth, temperature_f, humidity)
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