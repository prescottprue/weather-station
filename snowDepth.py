from gpiozero import DistanceSensor


maxDistance = 1.5
ultrasonic = DistanceSensor(echo=17, trigger=27, max_distance=maxDistance)

def getSnowDepth():
  # TODO: Subtract calibrated height instead of max
  snowDepth_m = maxDistance - ultrasonic.distance
  # Convert meters to inches
  snowDepth = snowDepth_m / .3048 % 1 * 12
  print('Snow depth is', snowDepth, 'in')

  return snowDepth

def outOfRange():
  print("Snow depth out of range")

ultrasonic.when_out_of_range = outOfRange