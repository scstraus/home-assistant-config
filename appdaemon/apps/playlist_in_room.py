import appdaemon.plugins.hass.hassapi as hass

# This appdaemon script plays music in a selection of rooms on iTunes and AirPlay devices based on an Amazon Alexa instruction (or service call)
# It was created primarily to handle shitty things that iTunes does like not turning on the speaker or playlist properly, so this retries till it works.

class PlaylistInRoom(hass.Hass):


#########################################################################################################
#                                  GLOBAL VARIABLES FOR MANAGING CALLBACKS                              #
#########################################################################################################

  SPEAKER_REQUEST_COUNT = 0
  SPEAKER_RESPONSE_COUNT = 0
  ALEXA_ENTITY = ""
  PLAYLIST = ""
  ITUNES_BEING_ASSHOLE_PROTECTION = 0
  ITUNES_BEING_ASSHOLE_ENGAGED = 0
  ITUNES_VOLUME_CHANGE_HAPPENED = 0
  TIME_TO_PLAY_PLAYLIST = 0
  REQUESTED_PLAY = 0
  ITUNES_BEING_ASSHOLE_CHECK_SECS = 12
  NO_VOLUME_CHANGE_FALLBACK_CHECK_SECS = 14

#########################################################################################################
#              THINGS WHICH CAN BE USER DEFINED THAT I SHOULD MOVE TO THE CONFIG FILE                   #
#########################################################################################################

  ITUNES_VOLUME = 0.5
  ITUNES_ENTITY = "media_player.itunes"

  AIRPLAY_ENTITIES = ["media_player.apple_tv_airtunes_speaker", "media_player.back_yard_airtunes_speaker", "media_player.bathroom_1st_floor_airtunes_speaker", "media_player.computer_airtunes_speaker", "media_player.gym_airtunes_speaker", "media_player.kitchen_airtunes_speaker", "media_player.laundry_room_airtunes_speaker", "media_player.library_airtunes_speaker", "media_player.living_room_airtunes_speaker", "media_player.master_bath_airtunes_speaker", "media_player.office_airtunes_speaker", "media_player.sebastian_s_room_airtunes_speaker", "media_player.sophie_s_room_airtunes_speaker"]
  AIRPLAY_ENTITY_VOLUMES = {"media_player.apple_tv_airtunes_speaker": 0.5, "media_player.back_yard_airtunes_speaker": 0.5, "media_player.bathroom_1st_floor_airtunes_speaker": 0.5, "media_player.computer_airtunes_speaker": 0.5, "media_player.gym_airtunes_speaker": 0.5, "media_player.kitchen_airtunes_speaker": 0.35, "media_player.laundry_room_airtunes_speaker": 0.5, "media_player.library_airtunes_speaker": 0.5, "media_player.living_room_airtunes_speaker": 0.25, "media_player.master_bath_airtunes_speaker": 0.7, "media_player.office_airtunes_speaker": 0.5, "media_player.sebastian_s_room_airtunes_speaker": 0.5, "media_player.sophie_s_room_airtunes_speaker": 0.5}
# Element 0 in each column is the alexa or service call, next elements are the speakers that it needs to activate to play music
  ALEXA_TO_AIRPLAY_MAPPING =[["media_player.alexa_kitchen","media_player.living_room_airtunes_speaker","media_player.kitchen_airtunes_speaker"],
  ["media_player.alexa_living_room","media_player.living_room_airtunes_speaker","media_player.kitchen_airtunes_speaker"],
  ["media_player.alexa_master_bath","media_player.master_bath_airtunes_speaker"],
  ["media_player.kichen_bar_kindle_fire","media_player.living_room_airtunes_speaker","media_player.kitchen_airtunes_speaker"],
  ["media_player.office_alexa","media_player.office_airtunes_speaker"],  
  ["media_player.sophies_room_echo_dot","media_player.sophie_s_room_airtunes_speaker"],
  ["media_player.master_closet_kindle","media_player.office_airtunes_speaker"],
  ["christmas","media_player.living_room_airtunes_speaker","media_player.kitchen_airtunes_speaker","media_player.bathroom_1st_floor_airtunes_speaker"]]

#########################################################################################################
#                            THESE ARE THE INITIALIZE AND LAUNCH FUNCTIONS                              #
#########################################################################################################

# Setup callbacks for things we are watching for
  def initialize(self):
    self.log("Playlist In Room AppDaemon App Initialized")
    self.listen_event(self.alexa_launch_itunes_playlist, "ALEXA_LAUNCH_ITUNES_PLAYLIST")
    self.listen_state(self.speaker_on, "media_player", new = "on")
    self.listen_state(self.speaker_off, "media_player", new = "off")
    self.listen_state(self.itunes_volume_change, "media_player.itunes", attribute = "volume_level")
    self.listen_state(self.itunes_started_playing, "media_player.itunes", new = "playing")
    self.listen_state(self.itunes_stopped_playing, "media_player.itunes", new = "paused")    

# start the playlist launch sequence when we get the event ALEXA_LAUNCH_ITUNES_PLAYLIST
  def alexa_launch_itunes_playlist(self, event, data, kwargs):
    self.ALEXA_ENTITY=data["alexa_entity"] 
    self.PLAYLIST=data["playlist"] 
    self.log("********************************************************************")
    self.log("Launching playlist %s for %s",self.PLAYLIST,self.ALEXA_ENTITY)
    self.log("********************************************************************")
    self.SPEAKER_REQUEST_COUNT = 0
    self.SPEAKER_RESPONSE_COUNT = 0
    self.TIME_TO_PLAY_PLAYLIST = 0
    self.ITUNES_VOLUME_CHANGE_HAPPENED = 0

    #Setting iTunes volume
    self.log("Setting iTunes volume to 50%")
    self.call_service("media_player/volume_set", entity_id = "media_player.itunes", volume_level=self.ITUNES_VOLUME) 
    #Turning on speakers
    for count in range(len(self.ALEXA_TO_AIRPLAY_MAPPING)):
      if self.ALEXA_TO_AIRPLAY_MAPPING[count][0]==self.ALEXA_ENTITY: # we found the right row for alexa
        self.log("Checking speakers to turn on, #%s: %s", count , self.ALEXA_TO_AIRPLAY_MAPPING[count][0])
        for count2 in range(1,len(self.ALEXA_TO_AIRPLAY_MAPPING[count])):
          state=self.get_state(self.ALEXA_TO_AIRPLAY_MAPPING[count][count2])
          if (state=="off"):
            self.call_service("media_player/turn_on", entity_id = self.ALEXA_TO_AIRPLAY_MAPPING[count][count2])
            self.SPEAKER_REQUEST_COUNT+=1
            self.log("Turning on speaker #%s: %s", count2, self.ALEXA_TO_AIRPLAY_MAPPING[count][count2])
          else: 
            self.log("Speaker #%s: %s is already on, leaving it alone", count2, self.ALEXA_TO_AIRPLAY_MAPPING[count][count2])

        #Turning off speakers
        for count3 in range(len(self.AIRPLAY_ENTITIES)):
          self.log("Checking speakers to turn off, #%s: %s",count3,self.AIRPLAY_ENTITIES[count3])
          if (self.AIRPLAY_ENTITIES[count3] in self.ALEXA_TO_AIRPLAY_MAPPING[count]):
            self.log("Skipping. Speaker should be on for room.")
          else:
            state=self.get_state(self.AIRPLAY_ENTITIES[count3])
            if (state=="on"):
              self.log("Entity on, turning off")
              self.set_state(self.AIRPLAY_ENTITIES[count3], state="off")
              self.SPEAKER_REQUEST_COUNT+=1
              self.call_service("media_player/turn_off", entity_id = self.AIRPLAY_ENTITIES[count3])
            else:
              self.log("Entity already off")
    if self.SPEAKER_REQUEST_COUNT==0:
    # All our speakers already turned off or on, so let's launch the playlist
    # Setting volumes
      self.log("All speakers already in correct state. Let's set volumes and launch playlist.")
      self.set_speaker_volumes()      
      # Playing playlist
      self.TIME_TO_PLAY_PLAYLIST = 1
      self.log("Now we play the playlist.")
      # Backup in case we don't get a volume changed event.
      self.run_in(self.no_volume_change_fallback, self.NO_VOLUME_CHANGE_FALLBACK_CHECK_SECS)             


#########################################################################################################
#                                   THESE ARE THE CALLBACK FUNCTIONS                                    #
#########################################################################################################

  def speaker_on(self, entity, attribute, old, new, kwargs):
    self.log("%s turned on", entity)
    self.set_speaker_volumes_and_prepare_play(entity)    

  def speaker_off(self, entity, attribute, old, new, kwargs):
    self.log("%s turned off", entity)
    self.set_speaker_volumes_and_prepare_play(entity)

  def itunes_volume_change(self, entity, attribute, old, new, kwargs):
    self.log("iTunes volume changed.")
    if self.TIME_TO_PLAY_PLAYLIST==1:
      self.play_playlist()
      self.ITUNES_VOLUME_CHANGE_HAPPENED = 1

  def itunes_started_playing(self, entity, attribute, old, new, kwargs):
    self.log("iTunes started playing.")
    if self.REQUESTED_PLAY == 1:
      self.ITUNES_BEING_ASSHOLE_PROTECTION == 1
      self.run_in(self.disable_itunes_being_asshole_protection, self.ITUNES_BEING_ASSHOLE_CHECK_SECS)
    
  def itunes_stopped_playing(self, entity, attribute, old, new, kwargs):
    self.log("iTunes stopped playing.")
    if self.ITUNES_BEING_ASSHOLE_PROTECTION > 0:
      self.log("****** ITUNES BEING ASSHOLE PROTECTION(TM) ENGAGED!!! ******")
      self.log("Setting iTunes to play %s playlist again, goddamnit", self.PLAYLIST)
      self.call_service("media_player/media_play", entity_id = self.ITUNES_ENTITY)
      self.ITUNES_BEING_ASSHOLE_ENGAGED += 1
      self.run_in(self.disable_itunes_being_asshole_protection, self.ITUNES_BEING_ASSHOLE_CHECK_SECS)

  def disable_itunes_being_asshole_protection(self, kwargs):
    if self.ITUNES_BEING_ASSHOLE_ENGAGED > 0:
      #not time to turn off the asshole protection yet.
      self.ITUNES_BEING_ASSHOLE_ENGAGED -= 1
      self.log("Callback for ITUNES BEING ASSHOLE PROTECTION(TM) Disable Made, but there's still more assholling possible, so holding off.")
    else:
      self.ITUNES_BEING_ASSHOLE_PROTECTION = 0
      self.log("Looks like iTunes won't be an asshole this time. Enjoy your music!")

  def no_volume_change_fallback(self, kwargs):
    self.log("Double checking that the iTunes volume change event happened in case we need to launch playlist without it.")
    if self.ITUNES_VOLUME_CHANGE_HAPPENED == 0:
      self.log ("Whoops, no volume change event. Will attempt to launch playlist now anyway.")
      if self.TIME_TO_PLAY_PLAYLIST==1:
        self.play_playlist()
      else: 
        self.log ("For some reason, it's not time to play the playlist after all. Skipping.")
    else:
      self.log ("Volume change happened, no fallback needed.")

#########################################################################################################
#                                THESE ARE THE NON-CALLBACK FUNCTIONS                                   #
#########################################################################################################

  def set_speaker_volumes_and_prepare_play(self, entity):
    # This is watching to see if we have all our speakers in the correct states before turning on the variables which tell the callbacks to play the playlist
    if entity in self.AIRPLAY_ENTITIES:
      if self.SPEAKER_REQUEST_COUNT>self.SPEAKER_RESPONSE_COUNT: 
        if self.SPEAKER_REQUEST_COUNT==(self.SPEAKER_RESPONSE_COUNT+1):
          # All our speakers turned off or on, so let's launch the playlist
          # Setting volumes
          self.log("All %s/%s speakers have now changed state. Setting volumes and starting playlist.",(self.SPEAKER_RESPONSE_COUNT+1),self.SPEAKER_REQUEST_COUNT)
          self.set_speaker_volumes()
          # Telling the next callback to play the playlist
          self.TIME_TO_PLAY_PLAYLIST = 1
          self.log("Now we play the playlist.")
          self.SPEAKER_REQUEST_COUNT = 0
          self.SPEAKER_RESPONSE_COUNT = 0
        elif self.SPEAKER_REQUEST_COUNT != 0: 
          self.SPEAKER_RESPONSE_COUNT +=1
          self.log("Speaker response count now %s out of %s requests", self.SPEAKER_RESPONSE_COUNT,self.SPEAKER_REQUEST_COUNT )

  def set_speaker_volumes(self):
    for count in range(len(self.ALEXA_TO_AIRPLAY_MAPPING)):
      if self.ALEXA_TO_AIRPLAY_MAPPING[count][0]==self.ALEXA_ENTITY:
        self.log("Working on speakers volumes #%s: %s", count , self.ALEXA_TO_AIRPLAY_MAPPING[count][0])
        for count2 in range(1,len(self.ALEXA_TO_AIRPLAY_MAPPING[count])):
          self.log("Setting #%s/%s (%s) to Volume: %s",count2,len(self.ALEXA_TO_AIRPLAY_MAPPING[count])-1, self.ALEXA_TO_AIRPLAY_MAPPING[count][count2], self.AIRPLAY_ENTITY_VOLUMES.get(self.ALEXA_TO_AIRPLAY_MAPPING[count][count2]))
          self.call_service("media_player/volume_set", entity_id = self.ALEXA_TO_AIRPLAY_MAPPING[count][count2], volume_level=self.AIRPLAY_ENTITY_VOLUMES.get(self.ALEXA_TO_AIRPLAY_MAPPING[count][count2]))

  def play_playlist(self):
    self.log("Setting iTunes to play %s playlist now", self.PLAYLIST)
    self.call_service("media_player/play_media", entity_id = self.ITUNES_ENTITY, media_content_id=self.PLAYLIST, media_content_type="playlist")
    self.TIME_TO_PLAY_PLAYLIST = 0
    self.REQUESTED_PLAY = 1