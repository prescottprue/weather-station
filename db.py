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

def writeMeasurement(temperature_f, humidity, internal_temperature_f, internal_humidity, snowDepth):
  try:
    # Get Cursor
    cur = conn.cursor()
    cur.execute(
    f"INSERT INTO {tableName} (temp,humidity,internal_temperature_f,internal_humidity,snow_depth) VALUES (?, ?, ?)",
    (temperature_f, humidity, internal_temp, internal_humidity, snowDepth))
    conn.commit() 
    print(f"Inserted new measurement: {cur.lastrowid}")
    cur.close()
  except mariadb.Error as e:
    print(f"Error: {e}")

def listMeasurements():
  cur = conn.cursor(dictionary=True) # So fetchall returns list of objects
  cur.execute(f"SELECT * FROM {tableName} ORDER BY ID DESC LIMIT 10;")
  measurements = cur.fetchall()
  cur.close()
  conn.commit()
  return measurements

def getLatestMeasurement():
  cur = conn.cursor(dictionary=True) # So fetchone returns objects
  cur.execute(f"SELECT * FROM {tableName} ORDER BY ID DESC LIMIT 1;")
  latest = cur.fetchone()
  cur.close()
  conn.commit()
  return latest
