#####################################################
# Set Dreamscreen color using RGB from HSV input    #
#####################################################

###### Service Call Parameters #######

H = data.get("h")
S = data.get("s")
V = data.get("v")

###### Global Variables #######

DREAMSCREEN_ENTITY_ID="dreamscreen.living_room_tv"

###### Function definitions ######


def hsv_to_rgb(h, s, v):
    i = math.floor(h*6)
    f = h*6 - i
    p = v * (1-s)
    q = v * (1-f*s)
    t = v * (1-(1-f)*s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i%6)]

    return r, g, b

#def hsv_to_rgb(h, s, v):
#    shape = h.shape
#    i = int_(h*6.)
#    f = h*6.-i
#
#    q = f
#    t = 1.-f
#    i = ravel(i)
#    f = ravel(f)
#    i%=6
#
#    t = ravel(t)
#    q = ravel(q)
#
#    clist = (1-s*vstack([zeros_like(f),ones_like(f),q,t]))*v
#
#    #0:v 1:p 2:q 3:t
#    order = array([[0,3,1],[2,0,1],[1,0,3],[1,2,0],[3,1,0],[0,1,2]])
#    rgb = clist[order[i], arange(prod(shape))[:,None]]
#
#    return rgb.reshape(shape+(3,))

#def hsv_to_rgb(h, s, v):
#    if s == 0.0: v*=255; return (v, v, v)
#    i = int(h*6.) # XXX assume int() truncates!
#    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
#    if i == 0: return (v, t, p)
#    if i == 1: return (q, v, p)
#    if i == 2: return (p, v, t)
#    if i == 3: return (p, q, v)
#    if i == 4: return (t, p, v)
#    if i == 5: return (v, p, q)

#def hsv_to_rgb(h, s, v):
#    if s == 0.0: return (v, v, v)
#    i = int(h*6.) # XXX assume int() truncates!
#    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
#    if i == 0: return (v, t, p)
#    if i == 1: return (q, v, p)
#    if i == 2: return (p, v, t)
#    if i == 3: return (p, q, v)
#    if i == 4: return (t, p, v)
#    if i == 5: return (v, p, q)


#def hsv_to_rgb(h, s, v):
#    h = float(h)
#    s = float(s)
#    v = float(v)
#    h60 = h / 60.0
#    h60f = math.floor(h60)
#    hi = int(h60f) % 6
#    f = h60 - h60f
#    p = v * (1 - s)
#    q = v * (1 - f * s)
#    t = v * (1 - (1 - f) * s)
#    r, g, b = 0, 0, 0
#    if hi == 0: r, g, b = v, t, p
#    elif hi == 1: r, g, b = q, v, p
#    elif hi == 2: r, g, b = p, v, t
#    elif hi == 3: r, g, b = p, q, v
#    elif hi == 4: r, g, b = t, p, v
#    elif hi == 5: r, g, b = v, p, q
#    r, g, b = int(r * 255), int(g * 255), int(b * 255)
#    return r, g, b

###### Main ######
logger.debug("Calling hsv_to_rgb with H=: %s, S= %s, V=%s",H,S,V) 
rgbhex = ("#" + hex(int(rgb[0])) + hex(int(rgb[1])) + hex(int(rgb[2])))
rgb = hsv_to_rgb(H,S,V)
logger.debug("R=: %s, G= %s, B=%s",rgb[0],rgb[1],rgb[2]) 
rgbhex = ("#" + hex(int(rgb[0])) + hex(int(rgb[1])) + hex(int(rgb[2])))
logger.debug("RGB hex color is: %s",rgbhex) 

hass.services.call("dreamscreen", "set_ambient_color", {"entity_id" : "DREAMSCREEN_ENTITY_ID", "color" : rgbhex}, False)
