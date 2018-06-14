# Read data from all sensors and print
# Includes: BME680, TSL2561 Light Sensor

import bme680
from tsl2561 import TSL2561
import time
import os

# Some variables
WAIT_PERIOD = 2

def main():
    bme = bme680.BME680(i2c_addr=0x77)

    #Initialize sensor
    bme.set_humidity_oversample(b
                                me680.OS_2X)
    bme.set_pressure_oversample(bme680.OS_4X)
    bme.set_temperature_oversample(bme680.OS_8X)
    bme.set_filter(bme680.FILTER_SIZE_3)
    bme.set_gas_status(bme680.ENABLE_GAS_MEAS)

    # Main loop
    while (1):
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
        
        print("      BME680")
        print("Temperature: {}".format(temperature))
        print("Pressure: {}".format(pressure))
        print("Humidity: {}".format(humidity))
        print("Gas: {}".format(gas))
        print('\n')
        print("     TSL2561")
        print("Lux: {}".format(luxVal))
        print ("------------------------")
			
        time.sleep(WAIT_PERIOD)

# Run main
if __name__ == '__main__':
    main()
