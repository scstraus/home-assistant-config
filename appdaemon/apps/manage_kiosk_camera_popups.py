# for some reason, there's no human_off timer running when this happens
# 2021-07-31 17:19:08.972791 INFO manage_kiosk_camera_popups: sensor.left_on_property_person changed state from 1 to 2
# 2021-07-31 17:19:08.974650 INFO manage_kiosk_camera_popups: Checking if other trigger timers are running and restarting timers if humans detected on them
# 2021-07-31 17:19:09.112504 INFO manage_kiosk_camera_popups: Popup camera = False
# 2021-07-31 17:19:09.113066 INFO manage_kiosk_camera_popups: Popup already open. Not issuing another popup command
# 2021-07-31 17:19:09.139565 INFO manage_kiosk_camera_popups: self.POPUP_OPEN = True. Sending screen wakeup commands
# 2021-07-31 17:19:09.140090 INFO manage_kiosk_camera_popups: Keepalive step = 1
# so the popup never closes. Must be fixed.



import appdaemon.plugins.hass.hassapi as hass

# This appdaemon script pops up camera windows on the kiosk tablets in the house when humans are spotted outside. It tries not to open and close camera windows too often as it causes them to not stream correctly.

class ManageKioskCameraPopups(hass.Hass):

#########################################################################################################
#                                  GLOBAL VARIABLES FOR MANAGING CALLBACKS                              #
#########################################################################################################

  ACTIVE_CAMERA="none"
  POPUP_OPEN="False"
  KINDLE_KITCHEN_DEVICEID=""
  KINDLE_MASTER_CLOSET_DEVICEID=""
  FRONT_CAMERA="camera.front_stream"
  BACK_CAMERA="camera.back_stream"
  LEFT_CAMERA="camera.left_substream"
  RIGHT_CAMERA="camera.right_substream"
  KEEPALIVE_STEP=0
#########################################################################################################
#                            THESE ARE THE INITIALIZE AND LAUNCH FUNCTIONS                              #
#########################################################################################################

# Setup callbacks for things we are watching for
  def initialize(self):
    self.log("Manage Kiosk Camera Popups AppDaemon App Initialized")
    self.listen_state(self.handle_human_sensor_updates, "sensor.right_on_property_person")
    self.listen_state(self.handle_human_sensor_updates, "sensor.left_on_property_person")
    self.listen_state(self.handle_human_sensor_updates, "sensor.right_on_property_person")
    self.listen_state(self.handle_human_sensor_updates, "sensor.back_on_property_person")
    self.listen_state(self.handle_human_off_timer_end, "timer.front_human_off",new="idle")
    self.listen_state(self.handle_human_off_timer_end, "timer.left_human_off",new="idle")
    self.listen_state(self.handle_human_off_timer_end, "timer.right_human_off",new="idle")
    self.listen_state(self.handle_human_off_timer_end, "timer.back_human_off",new="idle")
    self.listen_state(self.close_popup,"timer.human_popup_close",new="idle")
    self.KINDLE_KITCHEN_DEVICEID=self.args["kindle_kitchen_deviceid"]
    self.KINDLE_MASTER_CLOSET_DEVICEID=self.args["kindle_master_closet_deviceid"]
#    self.log("kindle_kitchen_deviceid is %s", self.args["kindle_kitchen_deviceid"])
#    self.log("kindle_master_closet_deviceid is %s", self.args["kindle_master_closet_deviceid"])
#    self.log("kindle_kitchen_deviceid is {}".format(kwargs["kindle_kitchen_deviceid"]))
#    self.log("kindle_master_closet_deviceid is {}".format(kwargs["kindle_master_closet_deviceid"]))

#########################################################################################################
#                                    THESE ARE THE CALLBACK FUNCTIONS                                   #
#########################################################################################################

  def handle_human_sensor_updates(self, entity, attribute, old, new, kwargs):
    self.log("%s changed state from %s to %s", entity, old, new)
    popup_camera="True"
    kindle_kitchen_deviceid = self.KINDLE_KITCHEN_DEVICEID
    kindle_master_closet_deviceid = self.KINDLE_MASTER_CLOSET_DEVICEID
    if (int(new) > 0): #changed from no human to human
      self.log("Checking if other trigger timers are running and restarting timers if humans detected on them")
      # Check if someone was detected recently on the other cameras, if so, decide not to switch to the new camera(entity)
      if ((self.get_state("timer.left_human_on")=="active") and entity != "sensor.left_on_property_person"):
        popup_camera="False"
        # restart timers for the other sides showing active humans other than the one that triggered this callback (entity)
        if (int(self.get_state("sensor.left_on_property_person"))>0):
          self.call_service("timer/start", entity_id = "timer.left_human_on")
      if ((self.get_state("timer.right_human_on")=="active") and entity != "sensor.right_on_property_person"):
        popup_camera="False"
        if (int(self.get_state("sensor.right_on_property_person"))>0):
          self.call_service("timer/start", entity_id = "timer.right_human_on")
      if ((self.get_state("timer.front_human_on")=="active") and entity != "sensor.front_on_property_person"):
        popup_camera="False"
        if (int(self.get_state("sensor.front_on_property_person"))>0):
          self.call_service("timer/start", entity_id = "timer.front_human_on")
      if ((self.get_state("timer.back_human_on")=="active") and entity != "sensor.back_on_property_person"):
        popup_camera="False"
        if (int(self.get_state("sensor.back_on_property_person"))>0):
          self.call_service("timer/start", entity_id = "timer.back_human_on")
      self.log("Popup camera = %s", popup_camera)
      if (popup_camera=="True" and (self.POPUP_OPEN=="False")):
        self.log("No other humans detected in last 3 seconds on other cameras. Popping up camera.")
        if entity == "sensor.right_on_property_person":
          self.open_popup("right")
          self.log("  Popping up right camera")
        elif entity == "sensor.left_on_property_person":
          self.open_popup("left")
          self.log("  Popping up left camera")
        elif entity == "sensor.back_on_property_person":
          self.open_popup("back")
          self.log("  Popping up back camera")
        elif entity == "sensor.front_on_property_person":
          self.open_popup("front")
          self.log("  Popping up front camera")
        self.log("  Restarting trigger timer for entity: %s", entity)
      elif self.POPUP_OPEN!="False":
        self.log("Popup already open. Not issuing another popup command")
      elif popup_camera!="True":
        self.log("Still a human or or timer running on current camera. Not issuing popup command", entity)
      if entity=="sensor.front_on_property_person":
        self.call_service("timer/start", entity_id = "timer.front_human_on")
      elif entity=="sensor.left_on_property_person":
        self.call_service("timer/start", entity_id = "timer.left_human_on")
      elif entity=="sensor.right_on_property_person":
        self.call_service("timer/start", entity_id = "timer.right_human_on")
      elif entity=="sensor.back_on_property_person":
        self.call_service("timer/start", entity_id = "timer.back_human_on")
    else: #changed from human to no human
      self.log("  Restarting human off timer for entity: %s", entity)
      if entity=="sensor.front_on_property_person":
        self.call_service("timer/start", entity_id = "timer.front_human_off")
      elif entity=="sensor.left_on_property_person":
        self.call_service("timer/start", entity_id = "timer.left_human_off")
      elif entity=="sensor.right_on_property_person":
        self.call_service("timer/start", entity_id = "timer.right_human_off")
      elif entity=="sensor.back_on_property_person":
        self.call_service("timer/start", entity_id = "timer.back_human_off")

  def handle_human_off_timer_end(self, entity, attribute, old, new, kwargs):
    self.log("Human off timer ended: %s", entity)
    #first check that no human is found or on_timer is on camera for off_timer which is ending. If there is a human, restart it's on_timer and exit function. If there's a timer running, exit function
    if (entity=="timer.front_human_off"):
      self.log("  Front human_off timer ended. Seeing if someone still on camera or timer")
      if (int(self.get_state("sensor.front_on_property_person"))>0):
        self.call_service("timer/start", entity_id = "timer.front_human_on")
        self.log("  Still someone on front camera. Restarting human_on timer and exiting function")
        return
      else:
        if (self.get_state("timer.front_human_on")=="active"):
          self.log("  Front human_on timer still running. Exiting function.")
          return
    elif (entity=="timer.left_human_off"):
      self.log("  Left human_off timer ended. Seeing if someone still on camera or timer")
      if (int(self.get_state("sensor.left_on_property_person"))>0):
        self.call_service("timer/start", entity_id = "timer.left_human_on")
        self.log("  Still someone on left camera. Restarting human_on timer and exiting function")
        return
      else:
        if (self.get_state("timer.left_human_on")=="active"):
          self.log("  Left human_on timer still running. Exiting function.")
          return
    elif (entity=="timer.right_human_off"):
      self.log("  Right human_off timer ended. Seeing if someone still on camera or timer")
      if (int(self.get_state("sensor.right_on_property_person"))>0):
        self.call_service("timer/start", entity_id = "timer.right_human_on")
        self.log("  Still someone on right camera. Restarting on human_on timer and exiting function")
        return
      else:
        if (self.get_state("timer.right_human_on")=="active"):
          self.log("  Right human_on timer still running. Exiting function.")
          return
    elif (entity=="timer.back_human_off"):
      self.log("  Back human_off timer ended. Seeing if someone still on camera or timer")
      if (int(self.get_state("sensor.back_on_property_person"))>0):
        self.call_service("timer/start", entity_id = "timer.back_human_on")
        self.log("  Still someone on back camera. Restarting human_on timer and exiting function")
        return
      else:
        if (self.get_state("timer.back_human_on")=="active"):
          self.log("  Back human_on timer still running. Exiting function.")
          return
    # look for humans on other cameras and if they are there, pop up that camera (shouldn't matter to check this camera too as we just showed that no one was there above)
    if (int(self.get_state("sensor.right_on_property_person"))>0):
      self.log("  Somone on Right Camera. Popping up popup.")
#      self.open_popup("camera.right_substream")
      self.open_popup("right")
      self.call_service("timer/start", entity_id = "timer.right_human_on")
      self.POPUP_OPEN="True"
    elif (int(self.get_state("sensor.left_on_property_person"))>0):
      self.log("  Somone on Left Camera. Popping up popup.")
#      self.open_popup("camera.left_substream") 
      self.open_popup("left")  
      self.call_service("timer/start", entity_id = "timer.left_human_on")
      self.POPUP_OPEN="True"
    elif (int(self.get_state("sensor.back_on_property_person"))>0):
      self.log("  Somone on Back Camera. Popping up popup.")
#      self.open_popup("camera.back_substream")   
      self.open_popup("back")
      self.call_service("timer/start", entity_id = "timer.back_human_on")
      self.POPUP_OPEN="True"
    elif (int(self.get_state("sensor.front_on_property_person"))>0):
      self.log("  Somone on Front Camera. Popping up popup.")
#      self.open_popup("camera.front_substream")
      self.open_popup("front")
      self.call_service("timer/start", entity_id = "timer.front_human_on") 
      self.POPUP_OPEN="True"
    elif (self.get_state("timer.right_human_on")=="active"):
      self.log("  Right human_on timer still running. Popping up popup.")
#      self.open_popup("camera.right_substream")
      self.open_popup("right") 
    elif (self.get_state("timer.left_human_on")=="active"):
      self.log("  Left human_on timer still running. Popping up popup.")
#      self.open_popup("camera.left_substream")
      self.open_popup("left") 
    elif (self.get_state("timer.front_human_on")=="active"):
      self.log("  Front human_on timer still running. Popping up popup.")
#      self.open_popup("camera.front_substream")   
      self.open_popup("front") 
    elif (self.get_state("timer.back_human_on")=="active"):
      self.log("  Back human_on timer still running. Popping up popup.")
#      self.open_popup("camera.back_substream")
      self.open_popup("back") 
    else:
      self.log("  There are no humans on or recently on any of the cameras. Now seeing if any more human_off timers are still running. If not, we will start the close_popup timer" )
      if (self.get_state("timer.right_human_off")=="active"):
        self.log("  Right human_off timer still running. Not starting close popup timer yet.")
        return
      elif (self.get_state("timer.left_human_off")=="active"):
        self.log("  Left human_off timer still running. Not starting close popup timer yet.")
        return    
      elif (self.get_state("timer.front_human_off")=="active"):
        self.log("  Front human_off timer still running. Not starting close popup timer yet.")
        return    
      elif (self.get_state("timer.back_human_off")=="active"):
        self.log("  Back human_off timer still running. Not starting close popup timer yet.")
        return
      else:
        self.log("  All timers are done and there's no people anywhere, so starting the close_popup timer")
        self.call_service("timer/start", entity_id = "timer.human_popup_close")

  def open_popup(self, camera):
    self.log("Popping up %s camera now",camera)
    if camera == "front":
      self.call_service("browser_mod/more_info", entity_id = self.FRONT_CAMERA, deviceID = self.KINDLE_KITCHEN_DEVICEID )
      self.call_service("browser_mod/more_info", entity_id = self.FRONT_CAMERA, deviceID = self.KINDLE_MASTER_CLOSET_DEVICEID )
      self.call_service("timer/start", entity_id = "timer.front_human_on")
#      self.call_service("browser_mod/navigate", navigation_path = "/lovelace/13", deviceID = self.KINDLE_KITCHEN_DEVICEID )
#      self.call_service("browser_mod/navigate", navigation_path = "/lovelace/13", deviceID = self.KINDLE_MASTER_CLOSET_DEVICEID )
    elif camera == "back":
      self.call_service("browser_mod/more_info", entity_id = self.BACK_CAMERA, deviceID = self.KINDLE_KITCHEN_DEVICEID )
      self.call_service("browser_mod/more_info", entity_id = self.BACK_CAMERA, deviceID = self.KINDLE_MASTER_CLOSET_DEVICEID )
      self.call_service("timer/start", entity_id = "timer.back_human_on")
#      self.call_service("browser_mod/navigate", navigation_path = "/lovelace/14", deviceID = self.KINDLE_KITCHEN_DEVICEID )
#      self.call_service("browser_mod/navigate", navigation_path = "/lovelace/14", deviceID = self.KINDLE_MASTER_CLOSET_DEVICEID )
    if camera == "left":
      self.call_service("browser_mod/more_info", entity_id = self.LEFT_CAMERA, deviceID = self.KINDLE_KITCHEN_DEVICEID )
      self.call_service("browser_mod/more_info", entity_id = self.LEFT_CAMERA, deviceID = self.KINDLE_MASTER_CLOSET_DEVICEID )
      self.call_service("timer/start", entity_id = "timer.left_human_on")
#      self.call_service("browser_mod/navigate", navigation_path = "/lovelace/15", deviceID = self.KINDLE_KITCHEN_DEVICEID )
#      self.call_service("browser_mod/navigate", navigation_path = "/lovelace/15", deviceID = self.KINDLE_MASTER_CLOSET_DEVICEID )
    elif camera == "right":
      self.call_service("browser_mod/more_info", entity_id = self.RIGHT_CAMERA, deviceID = self.KINDLE_KITCHEN_DEVICEID )
      self.call_service("browser_mod/more_info", entity_id = self.RIGHT_CAMERA, deviceID = self.KINDLE_MASTER_CLOSET_DEVICEID )
      self.call_service("timer/start", entity_id = "timer.right_human_on")

#      self.call_service("browser_mod/navigate", navigation_path = "/lovelace/16", deviceID = self.KINDLE_KITCHEN_DEVICEID )
#      self.call_service("browser_mod/navigate", navigation_path = "/lovelace/16", deviceID = self.KINDLE_MASTER_CLOSET_DEVICEID )

    # self.call_service("browser_mod/more_info", entity_id = entity, deviceID = self.KINDLE_KITCHEN_DEVICEID )
    # self.call_service("browser_mod/more_info", entity_id = entity, deviceID = self.KINDLE_MASTER_CLOSET_DEVICEID )
    self.ACTIVE_CAMERA=camera
    self.POPUP_OPEN="True"
    self.run_in(self.keep_screen_on, 0)

  def close_popup(self, entity, attribute, old, new, kwargs):
    if (self.POPUP_OPEN!="False"):
      self.log("Close popup timer is finished. self.POPUP_OPEN = %s. Closing the popup.",self.POPUP_OPEN)
      self.call_service("browser_mod/close_popup")
#      self.call_service("browser_mod/navigate", navigation_path = "/lovelace/1", deviceID = self.KINDLE_KITCHEN_DEVICEID )
#      self.call_service("browser_mod/navigate", navigation_path = "/lovelace/1", deviceID = self.KINDLE_MASTER_CLOSET_DEVICEID )
      self.POPUP_OPEN="False"
    else: 
      self
      self.log("Close popup timer is finished. self.POPUP_OPEN = %s. Doing nothing.",self.POPUP_OPEN)

  def keep_screen_on(self, kwargs):
    if self.POPUP_OPEN!="False":
      self.log("self.POPUP_OPEN = %s. Sending screen wakeup commands",self.POPUP_OPEN)
      self.KEEPALIVE_STEP=self.KEEPALIVE_STEP+1
      self.log("Keepalive step = %s",self.KEEPALIVE_STEP)
      if self.KEEPALIVE_STEP==1:
        self.call_service("shell_command/screensaver_stop_kindle_fire_kitchen")
        self.run_in(self.keep_screen_on, 1)
      if self.KEEPALIVE_STEP==2:
        self.call_service("shell_command/screensaver_stop_kindle_fire_closet")
        self.run_in(self.keep_screen_on, 1)
      if self.KEEPALIVE_STEP==3:
        self.call_service("shell_command/screen_on_kindle_fire_kitchen")
        self.run_in(self.keep_screen_on, 1)
      if self.KEEPALIVE_STEP==4:        
        self.call_service("shell_command/screen_on_kindle_fire_closet")
        self.KEEPALIVE_STEP=0
        self.run_in(self.keep_screen_on, 2)
      if self.KEEPALIVE_STEP>4:
        self.KEEPALIVE_STEP=0
    else:
      self.log("self.POPUP_OPEN = %s. Not sending screen wakeup commands", self.POPUP_OPEN)
      self.KEEPALIVE_STEP=0

