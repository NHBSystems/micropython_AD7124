from machine import Pin, SPI
from time import sleep, sleep_ms, ticks_us, ticks_ms, ticks_diff
import neopixel
import gc

from micropython_AD7124 import NHB_AD7124
from micropython_AD7124.thermocouple import Tc_Types

filterSelectBits = 4 #Fast

cs = 4 #CS pin

spi = SPI(1,
          baudrate=4000000, 
          sck=Pin(10),
          mosi=Pin(7),
          miso=Pin(8),
          firstbit =SPI.MSB,
          polarity=1,
          phase=1)  # AD7124 uses SPI mode 3

adc = NHB_AD7124.Ad7124(cs,spi)


print("Trying to read ID register...")
ID = adc.get_ID()
print(f"ADC chip ID: {hex(ID)}")


# Configure the ADC in full power mode
adc.set_adc_control(NHB_AD7124.AD7124_OpMode_SingleConv,
                    NHB_AD7124.AD7124_FullPower,True)

# Configure Setup 0 for load cells:
# - Use the external reference tied to the excitation voltage (2.5V reg)
# - Set a gain of 128 for a bipolar measurement of +/- 19.53 mv
adc.setup[0].set_config(NHB_AD7124.AD7124_Ref_ExtRef1, NHB_AD7124.AD7124_Gain_128, True)

# Configure Setup 1 for using the internal temperature sensor
# - Use internal reference and a gain of 1
adc.setup[1].set_config(NHB_AD7124.AD7124_Ref_Internal, NHB_AD7124.AD7124_Gain_1, True) #IC Temp

# Set filter type and data rate select bits (defined above)
#  The combination of filter type and filter select bits affects the final
#  output data rate. The SINC3 filter seems to be the best general purpose
#  option. The filter select bits are a number between 1 and 2048. A smaller
#  number will give a faster conversion, but allow more noise. Refer to the
#  datasheet for details, it can get complicated.
adc.setup[0].set_filter(NHB_AD7124.AD7124_Filter_SINC3, filterSelectBits)
adc.setup[1].set_filter(NHB_AD7124.AD7124_Filter_SINC3, filterSelectBits)

# Set channel 0 to use pins AIN0(+)/AIN1(-)
adc.set_channel(0, 0, NHB_AD7124.AD7124_Input_AIN0, NHB_AD7124.AD7124_Input_AIN1, True)

# Set channel 1 to use the internal temperature sensor for the positive input
# and AVSS for the negative
adc.set_channel(1, 1, NHB_AD7124.AD7124_Input_TEMP, NHB_AD7124.AD7124_Input_AVSS, True) #IC Temp

print("Turning ExV on")
adc.setPWRSW(True)
sleep_ms(200)


print("Now try to get some readings...")


while True:
    
    reading = adc.read_fb(0, 2.5, 5.00)  # Read full brideg sensor (Chan, Ex V, Scaling)
    #reading = adc.read_volts(0)         # Or use this to just read the voltage
    print(f"Loadcell = {reading:.4f}", end=',')
    
    ic_temp = adc.read_ic_temp(1)       
    print(f" IC Temp = {ic_temp:.2f}")
    
    sleep_ms(100)  