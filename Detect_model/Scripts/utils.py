import math

def map_to_screen(cam_x, cam_y, cam_width, cam_height, screen_width, screen_height, flip_x = True):
    
    ratio_x = cam_x / cam_width
    ratio_y = cam_y / cam_height

    if flip_x == True:
        ratio_x = 1 - ratio_x
    
    screen_x = ratio_x * screen_width
    screen_y = ratio_y * screen_height

    screen_x = clamp(screen_x, 0, screen_width)
    screen_y = clamp(screen_y, 0, screen_height)
    
    return screen_x, screen_y

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    dx = x2 - x1
    dy = y2 - y1

    dist = (dx**2 + dy**2)**0.5
    return dist

def clamp (value, min, max):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value
    
    
    