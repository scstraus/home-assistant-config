#########################################################
## Script to turn down the thermostat progressively in ##
## each room as the weather warms up so that we can    ## 
## "bank" some cold in the house to keep the house     ##
## cooler during warm days and save money on heat      ##
#########################################################

## Grab the weather parameters ##
LOW_TEMP = float((hass.states.get("sensor.dark_sky_overnight_low_temperature_0d")).state)
HIGH_TEMP = float((hass.states.get("sensor.dark_sky_daytime_high_temperature_0d")).state)
CLOUDY_DAY = ((hass.states.get("sensor.dark_sky_icon_0d")).state in ['partly-cloudy-day', 'rain', 'snow', 'sleet', 'wind', 'fog', 'cloudy'])
SUNNY_DAY = ((hass.states.get("sensor.dark_sky_icon_0d")).state in ['clear-day'])

## Set the services we need ##
TEMP_SET_SERVICE_DOMAIN = "evohome"
TEMP_SET_SERVICE_CALL = "set_zone_override"
SET_AUTO_SERVICE_DOMAIN = "evohome"
SET_AUTO_SERVICE_CALL = "clear_zone_override"

## Set the bounds of temps that can be set for rooms ##
MIN_TEMP = 5
MAX_TEMP = 25

# Profiles are temperatures of each room in this order (same as order defined in ROOM_ENTITIES:
# dining [0], entrance [1], garage [2], guest bedroom [3], living [4], master bath [5],	master bedroom [6], master closet [7], office [8], sebs room [9], sophie's room [10], laundry [11]
ROOM_ENTITIES= ["climate.dining_room", "climate.entrance", "climate.garage", "climate.guest_bedroom", "climate.living_room", "climate.master_bath", "climate.master_bedroom", "climate.master_closet", "climate.office_library", "climate.sebastian_s_room", "climate.sophie_s_room", "climate.laundry_room"]

# Temperature of 0 in profile means to skip that room ##
# Temperature of 100 in profile means to revert to auto schedule programmed into thermostat for cold weather ##
SKIP_TOKEN = 0
AUTO_TOKEN = 100

############################################################################################
## Maximum override time is 1 minute short of a day. Then we decide at the same time the  ##
## next day what override to apply/not apply, otherwise it just goes back to cold weather ##
## schedule, so we can't screw things up too much                                         ##
############################################################################################

OVERRIDE_MINUTES = 1439



## PROFILES DEFINED HERE ##



## Note value of skip token and auto token above for when we don't set temp or set it to auto mode ##

###########################################################################################
## Auto is for winter where full heating is needed, Profile A is for still cold weather  ##
## at night but somewhat warm during day where rooms won't warm up much during day and   ##           
## will cool down a lot during night, from there they are for warmer weather. Profile E  ##          
## is basically just turning the heat off in the whole house because the weather is warm ##          
## enough that it's not needed even at night for any rooms.                              ##
###########################################################################################

PROFILE_AUTO = [100,100,100,100,100,100,100,100,100,100,100,100]
PROFILE_A = [20,18,18,21,0,22,21,22,22,22,21,100]
PROFILE_B = [19,17,17,20,0,21,21,21,21,21,21,21]
PROFILE_C = [18,16,15,18,16,20,20,20,20,21,21,21]
PROFILE_D = [15,15,15,15,15,15,15,15,15,18,18,19]
PROFILE_E = [15,15,15,15,15,15,15,15,15,15,15,12]

###########################################################################################
## Some just for the living room, you probably won't need these, you can delete them and ##
## the logic at the bottom of the file for them                                          ##
###########################################################################################

LIVING_ROOM_18 = [0,0,0,0,18,0,0,0,0,0,0,0]
LIVING_ROOM_20 = [0,0,0,0,20,0,0,0,0,0,0,0]
LIVING_ROOM_AUTO = [0,0,0,0,100,0,0,0,0,0,0,0]

##########################################################################################
## List of entities of automations for other heat overrides that we may or may not want ##
## to be active depending on the chosen profile. These will be activated or deactivated ##
## according to the profile                                                             ##
##########################################################################################

AUTOMATION_ENTITIES = ["automation.working_from_home_today", "automation.working_from_home_now", "automation.turn_up_the_heat_in_sophie_s_room_if_she_s_home"]

## 1 is on, 0 is off

AUTOMATIONS_PROFILE_AUTO = [1,1,1]
AUTOMATIONS_PROFILE_A = [1,1,1]
AUTOMATIONS_PROFILE_B = [1,1,1]
AUTOMATIONS_PROFILE_C = [1,1,1]
AUTOMATIONS_PROFILE_D = [0,0,0]
AUTOMATIONS_PROFILE_E = [0,0,0]



###### Function definitions and startup. Proably don't need to change these ######



## Function that's actually setting the temperatures ##
def set_to_profile(profile,profile_name,automations_profile,automations_profile_name):
  logger.debug("Setting to profile %s",profile)

  ## turn off automations that aren't needed for profile ##
  if automations_profile_name in ["AUTOMATIONS_PROFILE_AUTO", "AUTOMATIONS_PROFILE_A", "AUTOMATIONS_PROFILE_B", "AUTOMATIONS_PROFILE_C", "AUTOMATIONS_PROFILE_D", "AUTOMATIONS_PROFILE_E"]: 
    for count in range(len(automations_profile)):
      logger.debug("Working on automation item %s",count)
      logger.debug("Heat entity name: %s", AUTOMATION_ENTITIES[count])
      logger.debug("Set to: %s", automations_profile[count])
      if automations_profile[count]==0:
        hass.services.call("automation", "turn_off", {"entity_id" : AUTOMATION_ENTITIES[count]}, False)
      elif automations_profile[count]==1:
        hass.services.call("automation", "turn_on", {"entity_id" : AUTOMATION_ENTITIES[count]}, False)
  elif automations_profile_name=="NULL":
    logger.debug("Living Room Heating Procfile, not setting automations on/off")
  else:
    logger.debug("Bad value for automation profile name: %s",automations_profile)

  ## set temperature ##
  
  #  for count,setting in enumerate(profile):
  for count in range(len(profile)):
    logger.debug("Working on heat item %s",count)
    logger.debug("Heat entity name: %s", ROOM_ENTITIES[count])
    logger.debug("Set to: %s", profile[count])
    if profile_name in ["PROFILE_AUTO", "PROFILE_A", "PROFILE_B", "PROFILE_C", "PROFILE_D", "PROFILE_E"]: 
      hass.services.call("input_select", "select_option", {"entity_id" : "input_select.active_heating_profile", "option" : profile_name}, False)
    if profile_name in ["LIVING_ROOM_18", "LIVING_ROOM_20", "LIVING_ROOM_AUTO"]:  
      hass.services.call("input_select", "select_option", {"entity_id" : "input_select.active_heating_profile_living_room", "option" : profile_name}, False)    
    if profile[count]==SKIP_TOKEN:
      logger.debug("Not setting %s",ROOM_ENTITIES[count]) 
    elif profile[count]==AUTO_TOKEN:
      logger.debug("Setting %s to Auto", ROOM_ENTITIES[count])  
      hass.services.call(SET_AUTO_SERVICE_DOMAIN, SET_AUTO_SERVICE_CALL, {"entity_id" : ROOM_ENTITIES[count]}, False)
    elif profile[count] in range(MIN_TEMP, MAX_TEMP):
      logger.debug("Setting %s to %s for 1439 minutes", ROOM_ENTITIES[count], profile[count])
      hass.services.call(TEMP_SET_SERVICE_DOMAIN, TEMP_SET_SERVICE_CALL, {"entity_id" : ROOM_ENTITIES[count], "setpoint" : profile[count], "duration" : {"minutes":1439}}, False)
    else:
      logger.info("Invalid value (%s) for temperature for room %s. Must be in range %s-%s. Item #%s skipped.", setpoint, ROOM_ENTITIES[count], MAX_TEMP, MIN_TEMP, count)


## Just some debug info in case something doesn't work ##
def startup_log_dump():
  logger.info("Starting up climate profile python script")
  logger.info("Low temp: %s",LOW_TEMP)
  logger.info("High temp: %s",HIGH_TEMP)
  logger.info("Weather Description: %s", (
  (hass.states.get("sensor.dark_sky_icon_0d")).state))
  logger.info("Is cloudy: %s",CLOUDY_DAY)
  logger.info("Is sunny: %s",SUNNY_DAY)
     
startup_log_dump()

########################################################################
## These are the rules for which profile to use based on the weather, ##
## you can change these based on any rules you want or try to keep    ##
## them as a starting point to fine tune your temps. I just made them ## 
## based on how my house felt under different conditions, so they     ##
## work well for me, but YMMV                                         ##
########################################################################

## Some general rules for in case we don't match others ##
if LOW_TEMP > 14 and HIGH_TEMP > 25:
  logger.info("Low > 14 High > 25 - Choose Profile E")
  set_to_profile(PROFILE_E,"PROFILE_E",AUTOMATIONS_PROFILE_E,"AUTOMATIONS_PROFILE_E")
elif LOW_TEMP >= 12 and LOW_TEMP <= 14 and HIGH_TEMP > 23:
  logger.info("Low 12-14 High > 23 - Choose Profile D")
  set_to_profile(PROFILE_D,"PROFILE_D",AUTOMATIONS_PROFILE_D,"AUTOMATIONS_PROFILE_D")
elif LOW_TEMP >= 10 and LOW_TEMP <= 13 and HIGH_TEMP > 20:
  logger.info("Low 10-13 High <= 13 - Choose Profile C")
  set_to_profile(PROFILE_C,"PROFILE_C",AUTOMATIONS_PROFILE_C,"AUTOMATIONS_PROFILE_C")
##  Rules for cool sunny weather ##
elif SUNNY_DAY and LOW_TEMP <= 5 and HIGH_TEMP >= 13:
  logger.info("Sunny Low <=5 High >= 13 - Choose Profile A")
  set_to_profile(PROFILE_A,"PROFILE_A",AUTOMATIONS_PROFILE_A,"AUTOMATIONS_PROFILE_A")
elif SUNNY_DAY and LOW_TEMP > 5 and LOW_TEMP <= 10 and HIGH_TEMP >= 13 and HIGH_TEMP <= 20:
  logger.info("Sunny Low 5-10 High 13-20 - Choose Profile A")
  set_to_profile(PROFILE_A,"PROFILE_A",AUTOMATIONS_PROFILE_A,"AUTOMATIONS_PROFILE_A")
elif SUNNY_DAY and LOW_TEMP > 5 and LOW_TEMP <= 10 and HIGH_TEMP > 20:
  logger.info("Sunny Low 5-10 High > 20 - Choose Profile B")
  set_to_profile(PROFILE_B,"PROFILE_B",AUTOMATIONS_PROFILE_B,"AUTOMATIONS_PROFILE_B")
elif SUNNY_DAY and LOW_TEMP < 10 and HIGH_TEMP < 13:
  logger.info("Sunny Low < 10 High < 13 - Choose Profile Auto")
  set_to_profile(PROFILE_AUTO,"PROFILE_AUTO",AUTOMATIONS_PROFILE_AUTO,"AUTOMATIONS_PROFILE_AUTO")
## Riles for cool cloudy weather ##
elif CLOUDY_DAY and LOW_TEMP >= 7 and LOW_TEMP <= 10 and HIGH_TEMP >= 15 and HIGH_TEMP <= 20:
  logger.info("Cloudy Low 7-10 High 15-20 - Choose Profile A")
  set_to_profile(PROFILE_A,"PROFILE_A",AUTOMATIONS_PROFILE_A,"AUTOMATIONS_PROFILE_A")
elif CLOUDY_DAY and LOW_TEMP < 7 and HIGH_TEMP >= 15:
  logger.info("Cloudy Low < 7 High > 15 - Choose Profile A")
  set_to_profile(PROFILE_A,"PROFILE_A",AUTOMATIONS_PROFILE_A,"AUTOMATIONS_PROFILE_A")
elif CLOUDY_DAY and LOW_TEMP >= 7 and LOW_TEMP <= 10 and HIGH_TEMP > 20:
  logger.info("Cloudy Low 7-10 High > 20 - Choose Profile B")
  set_to_profile(PROFILE_B,"PROFILE_B",AUTOMATIONS_PROFILE_B,"AUTOMATIONS_PROFILE_B")
elif CLOUDY_DAY and LOW_TEMP < 7 and HIGH_TEMP < 15:
  logger.info("Cloudy Low < 7 High < 15 - Choose Profile Auto")
  set_to_profile(PROFILE_AUTO,"PROFILE_AUTO",AUTOMATIONS_PROFILE_AUTO,"AUTOMATIONS_PROFILE_AUTO")
## Now, in theory the above rules covered all cases, this one is just here in case I screwed up (which is likely) ##
else:
  set_to_profile(PROFILE_AUTO,"PROFILE_AUTO",AUTOMATIONS_PROFILE_AUTO,"AUTOMATIONS_PROFILE_AUTO")
  logger.error("Didn't match any rules")

#########################################################################################
## I like to turn down the living room based on different rules because it has lots of ##
## west facing windows and the temperature is very sensitive to the sun, you could get ##
## rid of the below if the rules above and normal profiles are enough                  ##
#########################################################################################

if LOW_TEMP >= 2 and LOW_TEMP <= 5 and HIGH_TEMP > 11:
  logger.info("Low 2-5 High > 11 - Choose Living Room 20")
  set_to_profile(LIVING_ROOM_20,"LIVING_ROOM_20",NULL,"NULL")
elif LOW_TEMP > 5 and LOW_TEMP < 10 and HIGH_TEMP > 13:
  logger.info("Low 5-10 High > 13 - Choose Living Room 18")
  set_to_profile(LIVING_ROOM_18,"LIVING_ROOM_18",NULL,"NULL")
elif LOW_TEMP < 2 and HIGH_TEMP > 11: 
  logger.info("Low < 2 High > 11 - Choose Living Room Auto")
  set_to_profile(LIVING_ROOM_AUTO,"LIVING_ROOM_AUTO",NULL,"NULL")
elif LOW_TEMP < 5 and HIGH_TEMP < 11:
  logger.info("Low <= 5 High <= 11 - Choose Living Room Auto")
  set_to_profile(LIVING_ROOM_AUTO,"LIVING_ROOM_AUTO",NULL,"NULL")

