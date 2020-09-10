#####################################################
# This script just makes a message to display on my #
# frontend for when there are windows open that are #
# making the house cold or hot                      #
#####################################################


###### Global Variables #######

WINDOW_ENTITIES= ["binary_sensor.back_door", "binary_sensor.sebastians_room_left_window", "binary_sensor.sophies_room_ceiling_window", "binary_sensor.ecolink_closet_left_window", "binary_sensor.laundry_room_window_zone_13", "binary_sensor.ecolink_garage_door"]

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
  message=""
  if (hass.states.get("binary_sensor.back_door").state) == "on":
    message="The open back door"
    counter = counter - 1
  if (hass.states.get("binary_sensor.ecolink_garage_door").state) == "on":
    if num_open_windows > counter:
      message = message + ", the open garage door"
    else:
      message = "The open garage door"
    counter = counter - 1
  if num_open_windows > counter:
    message = message + ", and open windows in"
  else:
    message = message + "Open windows in"
  if (hass.states.get("binary_sensor.sebastians_room_left_window").state) == "on":
    message = message + " Sebastian's Room"
    counter = counter - 1
    window_counter = window_counter + 1
  if (hass.states.get("binary_sensor.sophies_room_ceiling_window").state) == "on":
    if counter == 1 and window_counter > 0:
      message = message + ", and"
    elif window_counter > 0:
      message = message + ", "
    message = message + " Sophie's Room"
    counter = counter - 1
    window_counter = window_counter + 1
  if (hass.states.get("binary_sensor.ecolink_closet_left_window").state) == "on":
    if counter == 1 and window_counter > 0:
      message = message + ", and the"
    elif window_counter > 0:
      message = message + ", "
    message = message + " Master Closet"
    counter = counter - 1
    window_counter = window_counter + 1  
  if (hass.states.get("binary_sensor.laundry_room_window_zone_13").state) == "on":
    if counter == 1 and window_counter > 0:
      message = message + ", and the"
    elif window_counter > 0:
      message = message + ", "
    message = message + " Laundry Room"
    counter = counter - 1
    window_counter = window_counter + 1  
  message = message + " are making the house cold."
  return message

###### Run the Functions ######

message=make_open_windows_message(count_open_windows())
logger.debug("The message is: %s",message)

