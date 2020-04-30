#--------------------------------------------------------------------------------------------------
# Call multiple services on multiple entities in an automation template
# currently does not support additional payload such as color information or brightness
#--------------------------------------------------------------------------------------------------

"""
Data format: service1|entityA|entityB|entityC,
            service2|entityX|entityY|entityZ

Example Usage: 
    - service: python_script.python_script_call_service_on_multiple_entities
      data_template:
        operations: >
          {% set topic = states.sensor.sensor_presence_tom.state %}
          {% if topic == 'Fort' %}
            media_player.media_stop|media_player.spotify,
            light.turn_off|group.all_lights|group.all_switches
          {% elif topic == 'Gerade angekommen' %}          
            scene.turn_on|scene.comfortable|test,
            homeassistant.turn_on|group.office
            scene.turn_on|scene.comfortable
          {% else %}
          {% endif %}
"""


operations = data.get('operations')
if not operations:
    logger.debug("Error, wrong data format or empty.")
else:
    logger.debug("tasks {0} end".format(operations))  
    tasks = operations.replace("\n","").replace(" ","").split(",")
    
    for task in tasks:
      logger.warning("tasks {0}".format(tasks))
      data = task.split("|")
      operation = data[0].split(".")
      service = operation[0]
      action = operation[1]
      if hass.services.has_service(service,action):
        for entity in data[1:]:
          if hass.states.get(entity) is not None:
            logger.debug("Calling {0}.{1} on Entity {2}".format(service,action,entity))
            hass.services.call(service, action, {"entity_id" : entity}, False)
          else:
            logger.warning("Could not find entity \"{0}\"".format(entity))
      else:
        logger.warning("Error: Service \"{0}\" not found".format(service))
