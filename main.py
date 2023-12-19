import time
from modules.tempAndHumidity import getTempAndHumidity, dhtDevice
from modules.snowDepth import getSnowDepth

while True:
  try:
    getTempAndHumidity()
    getSnowDepth()
  except RuntimeError as error:
      # Errors happen fairly often, DHT's are hard to read, just keep going
      print(error.args[0])
      time.sleep(2.0)
      continue
  except Exception as error:
      dhtDevice.exit()
      raise error
  
  time.sleep(2.0)