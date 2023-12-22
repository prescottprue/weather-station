import board
import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=True)

def getTempAndHumidity():
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