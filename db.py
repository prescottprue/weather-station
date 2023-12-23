import mariadb
import os
import sys
import atexit

# Connect to MariaDB Platform
try:
  conn = mariadb.connect(
    user="pi",
    password=os.environ.get('MARIADB_PASS'),
    host="localhost",
    port=3306,
    database="weather"
  )

except mariadb.Error as e:
  print(f"Error connecting to MariaDB Platform: {e}")
  sys.exit(1)

# Close database connection on exit
atexit.register(conn.close)

def writeWeather(temperature_f, humidity):
  try:
    # Get Cursor
    cur = conn.cursor()
    cur.execute(
    "INSERT INTO WEATHER_MEASUREMENT (AMBIENT_TEMPERATURE,HUMIDITY) VALUES (?, ?)",
    (temperature_f, humidity))
    conn.commit() 
    print(f"Last Inserted ID: {cur.lastrowid}")
  except mariadb.Error as e:
    print(f"Error: {e}")
