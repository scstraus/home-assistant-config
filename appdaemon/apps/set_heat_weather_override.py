import hassapi as hass

class SetHeatWeatherOverride(hass.Hass):

  def initialize(self):
#    self.run_daily(self.main)
    self.run_minutely(self.main)

  def set_to_profile(profile):
    ROOM_ENTITIES= ["climate.dining_room","climate.entrance","climate.garage","climate.guest_bedroom","climate.living_room","climate.master_bath","climate.master_bedroom","climate.master_closet","climate.office_library","climate.sebastian_s_room","climate.sophie_s_room","climate.laundry_room"]
  #  for count,setting in enumerate(profile):
    for count in range(len(profile)):
      self.log("Working on item %s",count)
      self.log("Entity name: %s", ROOM_ENTITIES[count])
      self.log("Set to: %s", PROFILE_A[count])
      if type(profile[count])=='int':
        self.log("Setting %s to %s",ROOM_ENTITIES[count],setting)
        self.call_service(evohome/set_zone_override, entity_id = ROOM_ENTITIES[count], setpoint=setting)
        hass.services.call(DOMAIN, SERVICE_SET, {"entity_id" : ROOM_ENTITIES[count],"setpoint" : setting, "duration" : {"minutes":1459}}, False)
      elif profile[count]=='X':
        self.log("Not setting %s",ROOM_ENTITIES[count]) 
      else:
        self.log("Setting %s to Auto",ROOM_ENTITIES[count])  

  def main(self):
    self.turn_on(self.args["off_scene"])
    # Profiles are temperatures of each room in this order:
    # dining [0], entrance [1], garage [2], guest bedroom [3], living [4], master bath [5],	master bedroom [6], master closet [7], office [8], sebs room [9], sophie's room [10], laundry [11]
    DOMAIN = "evohome"
    SERVICE_SET = "set_zone_override"
    PROFILE_A = [20,18,18,21,'X',22,21,22,22,22,21,'A']
    self.log("Starting up climate profile python script")
    set_to_profile(PROFILE_A)



