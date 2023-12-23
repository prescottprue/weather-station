from gpiozero import DistanceSensor

ultrasonic = DistanceSensor(echo=17, trigger=27, max_distance=1.5)


def getSnowDepth():
  # TODO: Subtract calibrated height
  print(ultrasonic.distance)
  snowDepth = ultrasonic.distance
  return snowDepth

def outOfRange():
  print("Snow depth out of range")

ultrasonic.when_out_of_range = outOfRange