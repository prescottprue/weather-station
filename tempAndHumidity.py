import board
import adafruit_dht
import busio
import adafruit_sht31d

# Internal Temp/Humidity sensor (DHT11)
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)

# External Temp/Humidity sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)

def getInternalTempAndHumidity():
  # Print the values to the serial port
  temperature_c = dhtDevice.temperature
  temperature_f = temperature_c * (9 / 5) + 32
  humidity = dhtDevice.humidity
  print(
      "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
          temperature_f, temperature_c, humidity
      )
  )
  return temperature_f, humidity

def getExternalTempAndHumidity():
  # Print the values to the serial port
  print("\nTemperature: %0.1f C" % sensor.temperature)
  print("Humidity: %0.1f %%" % sensor.relative_humidity)
  humidity = sensor.relative_humidity
  temperature_f = sensor.temperature * (9 / 5) + 32
  return temperature_f, sensor.relative_humidity