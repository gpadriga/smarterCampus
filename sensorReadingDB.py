# Read data from all sensors and print
# Includes: BME680, TSL2561 Light Sensor, USB microphone

import sqlite3
import bme680
from tsl2561 import TSL2561
import time
import os
import numpy
import pyaudio
import analyse

# Some variables
REPEAT = 5
WAIT_PERIOD = 2

def main():
    count = 0
    bme = bme680.BME680(i2c_addr=0x77)

    # Initialize db
    con = sqlite3.connect('data.db')
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data(temp FLOAT, pres FLOAT, hum FLOAT, gas FLOAT, lux INTEGER, db FLOAT)''')

    #Initialize sensor
    bme.set_humidity_oversample(bme680.OS_2X)
    bme.set_pressure_oversample(bme680.OS_4X)
    bme.set_temperature_oversample(bme680.OS_8X)
    bme.set_filter(bme680.FILTER_SIZE_3)
    bme.set_gas_status(bme680.ENABLE_GAS_MEAS)
    
    # Initialize USB mic
    pyaud = pyaudio.PyAudio()
    stream = pyaud.open(
	format = pyaudio.paInt16,
	channels = 1,
	rate = 32000,
	input_device_index = 2,
	input = True)

    # Main loop
    while (count < REPEAT):
	    # Read from BME
	    bme.get_sensor_data()
	    tempCelcius = float("{0:.2f}".format(bme.data.temperature))
	    #Convert the above variable to fahrenheit
	    temperature = float(tempCelcius*(9/5) + 32)
	    pressure = float("{0:.2f}".format(bme.data.pressure))
	    humidity = float("{0:.2f}".format(bme.data.humidity))
	    gas = float("{0:.2f}".format(bme.data.gas_resistance))
			
	    # Read from lux sensor
	    tsl = TSL2561(debug=True)
	    luxVal = tsl.lux()
	    
	    # Read from USB mic
            rawsamps = stream.read(2048, exception_on_overflow=False)
            samps = numpy.fromstring(rawsamps, dtype=numpy.int16)
            dB = analyse.loudness(samps)
	
	    print("      BME680")
	    print("Temperature: {}".format(temperature))
	    print("Pressure: {}".format(pressure))
	    print("Humidity: {}".format(humidity))
	    print("Gas: {}".format(gas))
	    print('\n')
	    print("     TSL2561")
            print("Lux: {}".format(luxVal))
            print('\n')
            print("     USB Mic")
            print ("------------------------")
            print ("Sound in dB: {}".format(dB)) 
            
	    values = (temperature, pressure, humidity, gas, luxVal, dB)
            c.execute("INSERT INTO data VALUES(?, ?, ?, ?, ?, ?)", values)
	    count += 1
			
	    time.sleep(WAIT_PERIOD)
    con.commit()
    con.close()
# Run main
if __name__ == '__main__':
    main()
