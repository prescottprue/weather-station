from picamera import PiCamera
from time import sleep


camera = PiCamera()
camera.rotation = 180

camera.capture('/home/pi/python-test.png')

def capturePicture():
  camera.capture('/home/pi/latest.png')