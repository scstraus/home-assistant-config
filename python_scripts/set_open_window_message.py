#####################################################
# This script just makes a message to display on my #
# frontend for when there are windows open that are #
# making the house cold or hot                      #
#####################################################

###### Service Call Parameters #######

MESSAGE_TYPE = data.get("message_type")

###### Global Variables #######

WINDOW_ENTITIES= ["binary_sensor.back_door", "binary_sensor.sebastians_room_left_window", "binary_sensor.sophies_room_ceiling_window", "binary_sensor.ecolink_closet_left_window", "binary_sensor.laundry_room_window_zone_13", "binary_sensor.ecolink_garage_door","binary_sensor.windows_1st_floor_zone_2"]

###### Function definitions ######

def count_open_windows():
  num_open_windows = 0
  logger.debug("Counting open windows")
  for count in range(len(WINDOW_ENTITIES)):
    logger.debug("Working on window %s",count)
    logger.debug("Window entity name: %s", WINDOW_ENTITIES[count])
    window_entity=WINDOW_ENTITIES[count]
    if (hass.states.get(WINDOW_ENTITIES[count]).state) == "on":
      logger.debug("%s is open",WINDOW_ENTITIES[count])
      num_open_windows = num_open_windows + 1
  logger.debug("Total number of open windows: %s",num_open_windows)
  return num_open_windows

def make_open_windows_message(num_open_windows):
  counter = num_open_windows
  window_counter = 0
  first_floor_windows = 0
  message=""
  if ((hass.states.get("binary_sensor.laundry_room_window_zone_13").state) == "on") and (MESSAGE_TYPE == "hot"):
    counter = counter - 1
  if (hass.states.get("binary_sensor.back_door").state) == "on":
    message = "The open Back Door"
    counter = counter - 1
  if (hass.states.get("binary_sensor.ecolink_garage_door").state) == "on":
    if num_open_windows > counter:
      message = message + ", the open Garage Door"
    else:
      message = "The open Garage Door"
    counter = counter - 1
  if (hass.states.get("binary_sensor.windows_1st_floor_zone_2").state) == "on":
    if num_open_windows > counter:
      message = message + ", open windows on the First Floor"
    else:
      message = "Open windows on the First Floor"
    if num_open_windows > counter:
      message = message + " and in"
    counter = counter - 1
    first_floor_windows = 1
  else:
    if (num_open_windows > counter) and (first_floor_windows == 1):
      message = message + " and open windows in"
    elif num_open_windows > counter:
      message = message + ", and open windows in"
    else:
      message = message + "Open windows in"
  if (hass.states.get("binary_sensor.sebastians_room_left_window").state) == "on":
    message = message + " Sebastian's Room"
    counter = counter - 1
    window_counter = window_counter + 1
  if (hass.states.get("binary_sensor.sophies_room_ceiling_window").state) == "on":
    if counter == 1 and window_counter == 1:
      message = message + " and"
    if counter == 1 and window_counter > 1:
      message = message + ", and"
    if counter > 1 and ((window_counter-counter)>1):
      message = message + ","
    message = message + " Sophie's Room"
    counter = counter - 1
    window_counter = window_counter + 1
  if (hass.states.get("binary_sensor.ecolink_closet_left_window").state) == "on":
    if counter == 1 and window_counter == 1:
      message = message + " and"
    if counter == 1 and window_counter > 1:
      message = message + ", and"
    if counter > 1 and ((window_counter-counter)>1):
      message = message + ","
    message = message + " the Master Closet"
    counter = counter - 1
    window_counter = window_counter + 1  
  if ((hass.states.get("binary_sensor.laundry_room_window_zone_13").state) == "on") and (MESSAGE_TYPE != "hot"):
    if counter == 1 and window_counter == 1:
      message = message + " and"
    if counter == 1 and window_counter > 1:
      message = message + ", and"
    if counter > 1 and ((window_counter-counter)>1):
      message = message + ","
    message = message + " the Laundry Room"
    counter = counter - 1
    window_counter = window_counter + 1
  message = message + " are"
  if MESSAGE_TYPE == "hot":
    message = message + " making the house hot."
    hass.services.call("input_text", "set_value", {"entity_id" : "input_text.windows_making_house_hot", "value" : message}, False)
  elif MESSAGE_TYPE == "cold":
    message = message + " making the house cold."
    hass.services.call("input_text", "set_value", {"entity_id" : "input_text.windows_making_house_cold", "value" : message}, False)
  elif MESSAGE_TYPE == "aqi":
    message = message + " letting polluted air into the house."
    hass.services.call("input_text", "set_value", {"entity_id" : "input_text.windows_letting_pollution_in", "value" : message}, False)
  return message

###### Run the Functions ######
num_open_windows = count_open_windows()
if num_open_windows > 0:
  message=make_open_windows_message(num_open_windows)
logger.debug("The message is: %s",message)

