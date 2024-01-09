import subprocess
from datetime import datetime
import os

extension = 'jpg'

def captureImage():
  print('Capturing image')
  now = datetime.now()
  dt_string = now.strftime("%Y-%d-%m/%H:%M:%S")
  filepath = '/home/pi/images/' + dt_string + '.' + extension
  # Create images directory if it doesn't already exist
  os.makedirs(os.path.dirname(filepath), exist_ok=True)
  # Capture image
  subprocess.run([
    'libcamera-still',
    '-n', # No preview
    '-o', filepath,
    '--vflip', '--hflip', # Transforms
    '--width', '2028', '--height', '1520' # Resolution
  ], check=True, text=True)
  print('Image captured, optimizing')
  subprocess.run(['cp', filepath, '/home/pi/images/latest.' + extension], check=True, text=True)
  print('Image optimized')