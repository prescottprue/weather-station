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
    cur.close()
  except mariadb.Error as e:
    print(f"Error: {e}")

def readWeather():
  # Get Cursor
  cur = conn.cursor()
  measurements = []
  cur.execute(f"SELECT ID,AMBIENT_TEMPERATURE,HUMIDITY,SNOW_DEPTH,CREATED FROM {tableName} ORDER BY ID DESC LIMIT 100")
  # Fill measurements array with objects
  for (id, temperature_f, humidity, snowDepth, created) in cur:
    measurements.append({ "id": id, "temp": temperature_f, "humidity": humidity, "snowDepth": snowDepth, "created": created })
  cur.close()
  return measurements
