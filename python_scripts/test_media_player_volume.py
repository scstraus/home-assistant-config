hass.services.call("media_player", "volume_set", {"entity_id" : "media_player.forked_daapd_output_kitchen", "volume_level" : "0.25" }, False)
hass.services.call("media_player", "volume_set", {"entity_id" : "media_player.forked_daapd_output_living_room", "volume_level" : "0.35" }, False)
hass.services.call("media_player", "volume_set", {"entity_id" : "media_player.forked_daapd_server", "volume_level" : "0.90"}, False)

#hass.services.call("media_player", "select_source", {"entity_id" : "media_player.forked_daapd_server", "source" : "Best Jazz"}, False)
#hass.services.call("media_player", "media_play", {"entity_id" : "media_player.forked_daapd_server"}, False)
