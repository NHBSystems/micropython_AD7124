# micropython_AD7124
MicroPython library for using the Analog Devices AD7124-4, 24 bit ADC

The AD7124-4 is a 4 channel, 24 bit, differential ADC (it can also be configured for up to 7 single ended channels). This library is a port of the [NHB_AD7124 Arduino library](https://github.com/NHBSystems/NHB_AD7124) to Micropython. The library is currently written in all Python and is a bit of a memory hog as it is, but it gets the job done. I am new to MicroPython, so I'm sure there is plenty of room for improvement and optimization.  

Like the original Arduino library, this was originally written for use 
with the [NHB AD7124 Analog Sensor FeatherWing](https://www.tindie.com/products/24680/), but there is no reason it couldn't be used with a raw chip in your own design.

So far I have only tested this library on an ESP32-C3, but it 
really should work with any architectures that has a working SPI
implementation. 