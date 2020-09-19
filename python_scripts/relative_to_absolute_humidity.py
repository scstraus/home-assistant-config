###########################################################
# A quick script to convert relative to absolute humidity #
###########################################################

###### Service Call Parameters #######

RELATIVE_HUMIDITY_SENSOR = data.get("relative_humidity_sensor")
AIR_PRESSURE_SENSOR = data.get("relative_humidity_sensor")
TEMPERATURE_SENSOR = data.get("temperature_sensor")
#INPUT_NUMBER_TO_SET = data.get("input_number_to_set")
VARIABLE_TO_SET = data.get("variable_to_set")

###### Global Variables #######

RH=(hass.states.get(RELATIVE_HUMIDITY_SENSOR).state)
T=(hass.states.get(TEMPERATURE_SENSOR).state)
P=100*(hass.states.get(AIR_PRESSURE_SENSOR).state)


###### Do Calculation and Return Value ######

es = 611.2*exp(17.67*(T-273.15)/(T-29.65))
rvs = 0.622*es/(P - es)
rv = RH/100. * rvs
qv = rv/(1 + rv)
rho = P/(RH * T)
AH = qv*rho

#hass.services.call("input_number", "set_value", {"entity_id" : INPUT_NUMBER_TO_SET, "value" : AH}, False)
hass.services.call("variable", "set_variable", {"variable" : VARIABLE_TO_SET, "value" : AH}, False)