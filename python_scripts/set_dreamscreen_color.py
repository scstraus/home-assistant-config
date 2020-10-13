#####################################################
# Set Dreamscreen color using RGB from HSV input    #
#####################################################

###### Service Call Parameters #######

H = int(data.get("h"))
S = (float(data.get("s")))/100
V = (float(data.get("v")))/100

###### Global Variables #######

DREAMSCREEN_ENTITY_ID="dreamscreen.living_room_tv"

###### Function definitions ######

def hsv_to_rgb(h, s, v):
  if s == 0.0: v = v*255; return (v, v, v)
  i = int(h*6.) 
  f = (h*6.)-i
  p = int(255*(v*(1.-s)))
  q = int(255*(v*(1.-s*f)))
  t = int(255*(v*(1.-s*(1.-f))))
  v = v*255
  i = i%6
  if i == 0: return (v, t, p)
  if i == 1: return (q, v, p)
  if i == 2: return (p, v, t)
  if i == 3: return (p, q, v)
  if i == 4: return (t, p, v)
  if i == 5: return (v, p, q)

###### Main ######
logger.debug("Calling hsv_to_rgb with H=: %s, S= %s, V=%s",H,S,V) 
rgb = hsv_to_rgb((float(H)/360.),S,V)
#logger.debug("R=: %x, G= %x, B=%x",rgb[0],rgb[1],rgb[2]) 
rhex=hex(int(rgb[0]))
ghex=hex(int(rgb[1]))
bhex=hex(int(rgb[2]))
rgbhex = ("#"+rhex[2:].zfill(2)+ghex[2:].zfill(2)+bhex[2:].zfill(2))
logger.debug("RGB hex color is: %s",rgbhex) 
hass.services.call("dreamscreen", "set_ambient_color", {"entity_id" : "dreamscreen.living_room_tv", "color" : rgbhex}, False)
