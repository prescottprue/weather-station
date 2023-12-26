import mariadb
import os
import sys
import atexit

tableName="WEATHER_MEASUREMENT"

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

def writeWeather(temperature_f, humidity, snowDepth):
  try:
    # Get Cursor
    cur = conn.cursor()
    cur.execute(
    f"INSERT INTO {tableName} (AMBIENT_TEMPERATURE,HUMIDITY,SNOW_DEPTH) VALUES (?, ?, ?)",
    (temperature_f, humidity, snowDepth))
    conn.commit() 
    print(f"Last Inserted ID: {cur.lastrowid}")
  except mariadb.Error as e:
    print(f"Error: {e}")

def readWeather():
  # Get Cursor
  cur = conn.cursor()
  cur.execute(f"SELECT * FROM weather.{tableName} ORDER BY CREATED")
  return cur
