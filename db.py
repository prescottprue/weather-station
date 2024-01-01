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
    f"INSERT INTO {tableName} (ambient_temperature,humidity,snow_depth) VALUES (?, ?, ?)",
    (temperature_f, humidity, snowDepth))
    conn.commit() 
    print(f"Inserted new measurement: {cur.lastrowid}")
    cur.close()
  except mariadb.Error as e:
    print(f"Error: {e}")

def listMeasurements():
  cur = conn.cursor(dictionary=True) # So fetchall returns list of objects
  cur.execute(f"SELECT * FROM {tableName} ORDER BY ID DESC LIMIT 10")
  measurements = cur.fetchall()
  conn.commit()
  cur.close()
  return measurements
