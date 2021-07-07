#####################################################
# This script just makes a message to display on my #
# frontend for when there are windows open that are #
# making the house cold or hot                      #
#####################################################

###### Service Call Parameters #######

MESSAGE_TYPE = data.get("message_type")

###### Global Variables #######

WINDOW_ENTITIES= ["binary_sensor.back_door", "binary_sensor.sebastians_room_left_window", "binary_sensor.sophies_room_ceiling_window", "binary_sensor.ecolink_closet_left_window", "binary_sensor.laundry_room_window_zone_13", "binary_sensor.ecolink_garage_door","binary_sensor.windows_1st_floor_zone_2","binary_sensor.master_bedroom_window","binary_sensor.office_door","binary_sensor.library_door"]

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
  door_counter = 0 
  window_counter = 0
  first_floor_windows = 0
  problem_conditions = 0
  first_open_window = 0
  message=""
  logger.debug("Making Open Window Message")
  logger.debug("Doing Laundry Room Counter. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  if ((hass.states.get("binary_sensor.laundry_room_window_zone_13").state) == "on") and (MESSAGE_TYPE == "hot"):
    counter = counter - 1
  logger.debug("Doing Back Door. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  if (hass.states.get("binary_sensor.back_door").state) == "on":
    message = "The open Back Door"
    counter = counter - 1
    door_counter = door_counter + 1
  logger.debug("Doing Garage Door. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  if (hass.states.get("binary_sensor.ecolink_garage_door").state) == "on":
    if num_open_windows > counter:
      message = message + ", the open Garage Door"
    else:
      message = "The open Garage Door"
    counter = counter - 1
    door_counter = door_counter + 1
  logger.debug("Doing First Floor Windows. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  if (hass.states.get("binary_sensor.windows_1st_floor_zone_2").state) == "on":
    # Both the back door and garage door are open and windows on the first floor are the last thing left
    if (num_open_windows > (counter+1)) and (counter == 1):
      message = message + ", and open windows on the First Floor"
    # We did one thing already and windows on the first floor are last thing left
    elif (num_open_windows > counter) and (counter == 1):
      message = message + " and open windows on the First Floor"
    elif (num_open_windows > counter) and (counter > 1):
      message = message + ", open windows on the First Floor"
    else:
      message = "Open windows on the First Floor"
    counter = counter - 1
    first_floor_windows = 1

## num open windows > (counter + 1) means we did multiple things already
## num open windows > counter means we did at least one thing already
## num_open_windows <= (counter+1) means we did one or less thing already 
## first_floor_windows means they are open
## counter == 1 means this is the last one
## counter == 2 means there is one more coming
## counter > 0 means there is this one or more coming
## counter > 1 means there is this one plus one or more coming
## counter > 2 means there is this one plus 2 or more coming

  logger.debug("Doing Connecting Words. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  # At least one open door and open first floor windows, any amount more windows open
  if (num_open_windows > (counter+1) ) and (first_floor_windows == 1) and (counter > 1):
    message = message + ", and open windows in"
    first_open_window = 1
  # First floor windows are open and 2 or more more windows are open
  elif (first_floor_windows == 1) and (counter >= 2):
    message = message + ", in"
    first_open_window = 1
  # No door open, only open first floor windows, and other window(s) open
  elif (num_open_windows <= (counter+1)) and (first_floor_windows == 1) and (counter >= 1):
    message = message + " and in"
  # no open door or open first floor windows but some open window
  elif (counter > 0):
    message = message + "Open windows in"
  logger.debug("Doing Sebastian's Room. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  if (hass.states.get("binary_sensor.sebastians_room_left_window").state) == "on":
    message = message + " Sebastian's Room"
    counter = counter - 1
    window_counter = window_counter + 1
  logger.debug("Doing Master Bedroom. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  if (hass.states.get("binary_sensor.master_bedroom_window").state) == "on":
    if counter == 1 and window_counter == 1:
      message = message + " and"
    if counter == 1 and window_counter > 1:
      message = message + ", and"
    if counter > 1 and ((window_counter-counter)<1) and (first_open_window<1):
      message = message + ","
    first_open_window=0
    message = message + " the Master Bedroom"
    counter = counter - 1
    window_counter = window_counter + 1
  logger.debug("Doing Office. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  if (hass.states.get("binary_sensor.office_door").state) == "on":
    if counter == 1 and window_counter == 1:
      message = message + " and"
    if counter == 1 and window_counter > 1:
      message = message + ", and"
    if counter > 1 and ((window_counter-counter)<1) and (first_open_window<1):
      message = message + ","
    first_open_window=0
    message = message + " the Office"
    counter = counter - 1
    window_counter = window_counter + 1
  logger.debug("Doing Library. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  if (hass.states.get("binary_sensor.library_door").state) == "on":
    if counter == 1 and window_counter == 1:
      message = message + " and"
    if counter == 1 and window_counter > 1:
      message = message + ", and"
    if counter > 1 and ((window_counter-counter)<1) and (first_open_window<1):
      message = message + ","
    first_open_window=0
    message = message + " the Library"
    counter = counter - 1
    window_counter = window_counter + 1
  logger.debug("Doing Sophies Room. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  if (hass.states.get("binary_sensor.sophies_room_ceiling_window").state) == "on":
    if counter == 1 and window_counter == 1:
      message = message + " and"
    if counter == 1 and window_counter > 1:
      message = message + ", and"
    if counter > 1 and ((window_counter-counter)<1) and (first_open_window<1):
      message = message + ","
    first_open_window=0
    message = message + " Sophie's Room"
    counter = counter - 1
    window_counter = window_counter + 1
  logger.debug("Doing Closet. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  if (hass.states.get("binary_sensor.ecolink_closet_left_window").state) == "on":
    if counter == 1 and window_counter == 1:
      message = message + " and"
    if counter == 1 and window_counter > 1:
      message = message + ", and"
    if counter > 1 and ((window_counter-counter)<1) and (first_open_window<1):
      message = message + ","
    first_open_window=0
    message = message + " the Master Closet"
    counter = counter - 1
    window_counter = window_counter + 1  
  logger.debug("Doing Laundry Room. counter==%s, num_open_windows==%s, door_counter==%s, window_counter==%s,first_floor_windows==%s",  counter, num_open_windows, door_counter, window_counter, first_floor_windows)
  if ((hass.states.get("binary_sensor.laundry_room_window_zone_13").state) == "on") and (MESSAGE_TYPE != "hot"):
    if counter == 1 and window_counter == 1:
      message = message + " and"
    if counter == 1 and window_counter > 1:
      message = message + ", and"
    if counter > 1 and ((window_counter-counter)<1) and (first_open_window<1):
      message = message + ","
    first_open_window=0
    message = message + " the Laundry Room"
    counter = counter - 1
    window_counter = window_counter + 1
  if ((door_counter == 1) and (window_counter == 0) and (first_floor_windows == 0)):
    message = message + " is"
  else:
    message = message + " are"
  logger.debug("binary_sensor.open_window_making_house_hot: %s",(hass.states.get("binary_sensor.open_window_making_house_hot").state))
  if (hass.states.get("binary_sensor.open_window_making_house_hot").state) == "on":
#  if hass.states.is_state("binary_sensor.open_window_making_house_hot","on"):
    logger.debug("Adding house hot message")
    message = message + " making the house hot"
    problem_conditions = 1
    
  logger.debug("binary_sensor.open_window_making_house_cold: %s",(hass.states.get("binary_sensor.open_window_making_house_cold").state))
  if (hass.states.get("binary_sensor.open_window_making_house_cold").state) == "on":
#  if hass.states.is_state("binary_sensor.open_window_making_house_cold","on"):
    logger.debug("Adding house cold message")
    message = message + " making the house cold"
    problem_conditions = 1
  logger.debug("binary_sensor.open_window_letting_pollution_in: %s",(hass.states.get("binary_sensor.open_window_letting_pollution_in").state))
  if (hass.states.get("binary_sensor.open_window_letting_pollution_in").state) == "on":
    logger.debug("Adding pollution message")
#  if hass.states.is_state("binary_sensor.open_window_letting_pollution_in","on"):
    if problem_conditions > 0:
      message = message + " and letting polluted air in"
    else:
      message = message + " letting polluted air into the house" 
  message = message + "."
  logger.debug("Calling input text set value with message: %s",message)
  hass.services.call("input_text", "set_value", {"entity_id" : "input_text.windows_making_problem", "value" : message}, False)
  return message
#  if MESSAGE_TYPE == "hot":
#    message = message + " making the house hot."
#    hass.services.call("input_text", "set_value", {"entity_id" : "input_text.windows_making_house_hot", "value" : message}, False)
#  elif MESSAGE_TYPE == "cold":
#    message = message + " making the house cold."
#    hass.services.call("input_text", "set_value", {"entity_id" : "input_text.windows_making_house_cold", "value" : message}, False)
#  elif MESSAGE_TYPE == "aqi":
#    message = message + " letting polluted air into the house."
#    hass.services.call("input_text", "set_value", {"entity_id" : "input_text.windows_letting_pollution_in", "value" : message}, False)


###### Run the Functions ######
num_open_windows = count_open_windows()
if num_open_windows > 0:
  message=make_open_windows_message(num_open_windows)
  logger.debug("The message is: %s",message)
else: 
  logger.debug("Message not set")
