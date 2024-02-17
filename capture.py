import time
from tempAndHumidity import getInternalTempAndHumidity, getExternalTempAndHumidity, dhtDevice
from snowDepth import getSnowDepth
from camera import captureImage
from db import writeMeasurement, conn

while True:
  try:
    internal_temperature_f, internal_humidity = getInternalTempAndHumidity()
    temperature_f, humidity = getExternalTempAndHumidity()
    snowDepth = getSnowDepth()
    writeMeasurement(temperature_f, humidity, internal_temperature_f, internal_humidity, snowDepth)
    captureImage()
  except RuntimeError as error:
    # Errors happen fairly often, DHT's are hard to read, just keep going
    print(error.args[0])
    time.sleep(2.0)
    continue
  except Exception as error:
    dhtDevice.exit()
    conn.close()
    raise error

  # Capture every 5 mins
  time.sleep(300.0)