from picamera import PiCamera
from time import sleep


camera = PiCamera()
camera.rotation = 180

def capturePicture():
  print('Capturing image')
  camera.capture('/home/pi/latest.jpg')
  print('Image captured')