import mariadb
import os
import sys
import atexit

tableName="measurements"

# Connect to MariaDB Platform
try:
  conn = mariadb.connect(
    user="pi",
    password=os.environ.get('MARIADB_PASS'),
    host="0.0.0.0",
    port=3306,
    database="weather"
  )

except mariadb.Error as e:
  print(f"Error connecting to MariaDB Platform: {e}")
  sys.exit(1)

# Close database connection on exit
atexit.register(conn.close)

def writeMeasurement(temperature_f, humidity, snowDepth):
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

def listMeasurements():
  cur = conn.cursor(dictionary=True) # So fetchall returns list of objects
  cur.execute(f"SELECT ID,AMBIENT_TEMPERATURE,HUMIDITY,SNOW_DEPTH,CREATED FROM {tableName} ORDER BY ID DESC LIMIT 100")
  measurements = cur.fetchall()
  cur.close()
  return measurements
