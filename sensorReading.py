# Read data from all sensors and print
# Includes: BME680, TSL2561 Light Sensor

import bme680
import time
import os

# Some variables
REPEAT = 5
WAIT_PERIOD = 2

def main():
    count = 0
    bme = bme680.BME680(i2c_addr=0x77)

    #Initialize sensor
    bme.set_humidity_oversample(bme680.OS_2X)
    bme.set_pressure_oversample(bme680.OS_4X)
    bme.set_temperature_oversample(bme680.OS_8X)
    bme.set_filter(bme680.FILTER_SIZE_3)
    bme.set_gas_status(bme680.ENABLE_GAS_MEAS)

    # Main loop
    while (1):
		if bme.get_sensor_data():
			tempCelcius = float("{0:.2f}".format(bme.data.temperature))
			#Convert the above variable to fahrenheit
			temperature = float(tempCelcius*(9/5) + 32)
			pressure = float("{0:.2f}".format(bme.data.pressure))
			humidity = float("{0:.2f}".format(bme.data.humidity))
			gas = float("{0:.2f}".format(bme.data.gas_resistance))

			print("Temperature: " + str(temperature))
			print("Pressure:" + str(pressure))
			print("Humidity:" + str(humidity))
			print("Gas:" + str(gas) + '\n')
			
			count += 1
			
			time.sleep(WAIT_PERIOD)

# Run main
if __name__ == '__main__':
    main()
