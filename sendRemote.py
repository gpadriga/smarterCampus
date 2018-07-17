# Read data from all sensors and sends
# Includes: BME680, TSL2561 Light Sensor, USB microphone

import MySQLdb
import bme680
from tsl2561 import TSL2561
import time
import os
import numpy
import pyaudio
import analyse
from uuid import getnode as get_mac

# Some variables
WAIT_PERIOD = 60
HOST = "155.246.80.48"
PORT = 3306
USER = "gpadriga"
PASSWORD = "summer18"
DB = "readings"


def main():
    mac_addr = open('/sys/class/net/wlan0/address').readline()

    bme = bme680.BME680(i2c_addr=0x77)

    # Initialize db
    con = MySQLdb.Connection(host=HOST, port=PORT,
                             user=USER, passwd=PASSWORD, db=DB)
    c = con.cursor()
    # c.execute(CREATE TABLE IF NOT EXISTS data (temp FLOAT, pres FLOAT, hum FLOAT, gas FLOAT, lux INT, dbs FLOAT))

    # Initialize sensor
    bme.set_humidity_oversample(bme680.OS_2X)
    bme.set_pressure_oversample(bme680.OS_4X)
    bme.set_temperature_oversample(bme680.OS_8X)
    bme.set_filter(bme680.FILTER_SIZE_3)
    bme.set_gas_status(bme680.ENABLE_GAS_MEAS)

    # Initialize USB mic
    #pyaud = pyaudio.PyAudio()
    # stream = pyaud.open(
    #	format = pyaudio.paInt16,
    #channels = 1,
    #rate = 32000,
    #input_device_index = 2,
    #input = True
    # )

    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print("Readings began " + now)
    print("Press ctrl+c to end readings and close connection.")

    # Main loop
    while (True):
        try:
            # Record time
            now = time.strftime('%Y-%m-%d %H:%M:%S')

            # Read from BME
            bme.get_sensor_data()
            tempCelcius = float("{0:.2f}".format(bme.data.temperature))

            # Convert the above variable to fahrenheit
            temperature = float(tempCelcius*(9/5) + 32)
            pressure = float("{0:.2f}".format(bme.data.pressure))
            humidity = float("{0:.2f}".format(bme.data.humidity))
            gas = float("{0:.2f}".format(bme.data.gas_resistance))

            # Read from lux sensor
            tsl = TSL2561(debug=True)
            luxVal = tsl.lux()

            # Read from USB mic
            #rawsamps = stream.read(2048, exception_on_overflow=False)
            #samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
            #decib = analyse.loudness(samps) + 60

            values = (mac_addr, temperature, pressure,
                      humidity, gas, luxVal, now)
            add_val = ("INSERT INTO data "
                       "(mac, temp, pres, hum, gas, lux, dt)"
                       "VALUES (%s, %s, %s, %s, %s, %s, %s)")
            c.execute(add_val, values)
            con.commit()

            time.sleep(WAIT_PERIOD)

        except KeyboardInterrupt:
            con.close()
            break


# Run main
if __name__ == '__main__':
    main()
