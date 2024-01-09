from gpiozero import DistanceSensor

ultrasonic = DistanceSensor(echo=23, trigger=24)
# sensor resolution .005m (.5cm)
calibrated_zero = 0.720

def getSnowDepth():
  # TODO: Subtract calibrated height instead of max
  # Convert meters to inches
  depth_m = round(calibrated_zero - ultrasonic.distance, 3)
  if depth_m < 0.005:
    snowDepth = 0
  else:
    snowDepth = (depth_m * 39.37) - 0.41
  print('Distance', ultrasonic.distance)
  print('Snow depth is', snowDepth, 'in')

  return snowDepth

def getSensorDepth():
  return ultrasonic.distance

def outOfRange():
  print("Snow depth out of range")

ultrasonic.when_out_of_range = outOfRange