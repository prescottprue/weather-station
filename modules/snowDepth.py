from gpiozero import DistanceSensor

ultrasonic = DistanceSensor(echo=17, trigger=27)

def getSnowDepth():
  # TODO: Subtract calibrated height
  print(ultrasonic.distance)
