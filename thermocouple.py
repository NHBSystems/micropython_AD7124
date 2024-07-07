from math import pow, exp

class Tc_Types:
  Type_K = 0 
  Type_J = 1 #Not yet implemented 
  Type_T = 2 #Not yet implemented 

  
class TC:
  def __init__(self):
    pass

  def volts_to_tempC(self, voltage, junctionTemp, type):
    offsetV = self.tempC_to_volts(junctionTemp, type)
    return self.volts_to_tempC_no_comp(voltage + offsetV, type)

  def volts_to_tempC_no_comp(self, voltage, type):
    coef_1 = [0, 2.5173462e1, -1.1662878, -1.0833638, -8.9773540e-1]
    coef_2 = [0, 2.508355e1, 7.860106e-2, -2.503131e-1, 8.315270e-2]
    coef_3 = [-1.318058e2, 4.830222e1, -1.646031, 5.464731e-2, -9.650715e-4]
    i = 5
    mVoltage = voltage * 1e3

    if voltage < 0:
      temperature = self.power_series(i, mVoltage, coef_1)
    elif voltage > 20.644:
      temperature = self.power_series(i, mVoltage, coef_3)
    else:
      temperature = self.power_series(i, mVoltage, coef_2)

    return temperature

  def tempC_to_volts(self, temperature, type):
    coef_1 = [0, 0.3945013e-1, 0.2362237e-4, -0.3285891e-6, -0.4990483e-8]
    coef_2 = [-0.17600414e-1, 0.38921205e-1, 0.1855877e-4, -0.9945759e-7, 0.31840946e-9]
    a_coef = [0.1185976, -0.1183432e-3, 0.1269686e3]
    i = 5

    a_power = a_coef[1] * pow((temperature - a_coef[2]), 2)
    a_results = a_coef[0] * exp(a_power)

    if temperature < 0:
      mVoltage = self.power_series(i, temperature, coef_2) + a_results
    else:
      mVoltage = self.power_series(i, temperature, coef_1)

    return mVoltage / 1e3

  def power_series(self, n, input, coef):
    sum = coef[0]
    for i in range(1, n):
      sum = sum + (pow(input, i) * coef[i])
    return sum