#!/usr/bin/python
import colorsys
import os
import random
import subprocess
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants
import i3
import time

device_manager = DeviceManager()
device_manager.sync_effects = False
i3socket = i3.Socket()

if not os.path.exists("/etc/rasiel/keyboardrasiel"):
    os.mkfifo("/etc/rasiel/keyboardrasiel")  

try:
    pipe = [open("/etc/rasiel/keyboardrasiel", "r")]
except:
    print("Failed opening pipe")
    pipe.close()
    quit()




red = (255, 0, 0)
greenplus = (60, 255, 20)
green = (0, 255, 0)
lightgreen = (55, 255, 55)
darkgreen = (0, 10, 0)
blue = (0, 0, 255)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 64, 0)
def language_dependent_color():
    if language_us[0]:
        return blue
    else:
        return red

language_us = [True]
subprocess.call(["setxkbmap", "us,ru"])

environment_color = [green]
env_effect = [False]
reactive_effect = [False]
previous_brightness = [40]
remember_brightness = [True]

def getKeyboard(device_manager):
    for device in device_manager.devices:
        if device.name == 'Razer Blade Stealth (Late 2017)':
            return device

def set_max_brightness(device):
    if remember_brightness[0]:
        # trick to bypass keyboard bug where it randomly returns 0
        b = max([device.brightness, device.brightness, device.brightness, device.brightness])
        previous_brightness[0] = b
    device.brightness = 100
    remember_brightness[0] = False
    pass

def set_brightness_back(device):
    device.brightness = previous_brightness[0]
    remember_brightness[0] = True
    pass

def hex_to_light(value):
    value = value.lstrip('#')
    lv = len(value)
    rgb = list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    # rgb[0] = floor(rgb[0] / 255 * 200) + 55
    rgb[0] = max(0, floor(rgb[0] / 255 * 355) - 100)
    rgb[1] = max(0, floor(rgb[0] / 255 * 355) - 100)
    rgb[2] = max(0, floor(rgb[0] / 255 * 355) - 100)
    return tuple(rgb)

def load_env_type():
    current = [ws for ws in i3.get_workspaces() if ws['focused']][0]
    workspace = i3.filter(num=current['num'])
    if workspace:
        found = str(workspace).find("Sublime")
        if found == -1:
            env_effect[0] = False
        else:
            env_effect[0] = True

def load_environment_color():
    with open('/home/rasiel/.config/i3/envcolor.txt') as f:
        rgb = list([int(x) for x in next(f).split()])
        m = rgb.index(max(rgb))
        rgb[m] = 255
        rgb[(m + 1) % 3] //= 2
        rgb[(m + 2) % 3] //= 2
        environment_color[0] = tuple(rgb)

def switchlang():
    if language_us[0]:
        language = "ru,us"
        language_us[0] = False
    else:
        language = "us,ru"
        language_us[0] = True
    subprocess.call(["setxkbmap", language])

    device = getKeyboard(device_manager)
    light_modifiers(device)
    device.fx.advanced.matrix[5,4] = white # alt
    device.fx.advanced.matrix[5,9] = white # alt
    device.fx.advanced.draw()

def random_color():
    rgb = colorsys.hsv_to_rgb(random.uniform(0, 1), random.uniform(0.5, 1), 1)
    return tuple(map(lambda x: int(256 * x), rgb))
def fill(device, color):
    device.fx.static(color[0], color[1], color[2])
def clear_light(device):
    rows, cols = device.fx.advanced.rows, device.fx.advanced.cols
    for row in range(rows):
        for col in range(cols):
            device.fx.advanced.matrix[row, col] = black
def fill_workspaces(device):
    load_env_type()
    if env_effect[0]:
        load_environment_color()
    workspaces = i3socket.get("get_workspaces")
    for i in range(1, 14):
        device.fx.advanced.matrix[1, i] = darkgreen
    for ws in workspaces:
        if ws['urgent']:
            color = orange
        elif ws['visible']:
            color = white
        else:
            color = yellow
        device.fx.advanced.matrix[1, ws['num']] = color
def light_modifiers(device):
    newcolor = language_dependent_color()
    device.fx.advanced.matrix[4,1] = newcolor # shift
    device.fx.advanced.matrix[4,15] = newcolor # shift
    device.fx.advanced.matrix[5,1] = newcolor # strg
    device.fx.advanced.matrix[5,2] = newcolor # fn
    device.fx.advanced.matrix[5,3] = newcolor # super
    device.fx.advanced.matrix[5,4] = newcolor # alt
    device.fx.advanced.matrix[5,9] = newcolor # alt
    device.fx.advanced.matrix[5,10] = newcolor # fn
    device.fx.advanced.matrix[5,11] = newcolor # strg

def light_ctrl():
    device = getKeyboard(device_manager)
    clear_light(device)
    
    light_modifiers(device)
    device.fx.advanced.matrix[1,2] = green 
    device.fx.advanced.matrix[1,3] = green
    device.fx.advanced.matrix[1,4] = green
    device.fx.advanced.matrix[1,5] = green
    device.fx.advanced.matrix[1,6] = green
    device.fx.advanced.matrix[1,7] = green
    device.fx.advanced.matrix[1,8] = green
    device.fx.advanced.matrix[1,9] = green
    device.fx.advanced.matrix[1,10] = green
    device.fx.advanced.matrix[1,11] = green
    device.fx.advanced.matrix[1,12] = green
    device.fx.advanced.matrix[1,13] = green
    device.fx.advanced.matrix[1,14] = green
    device.fx.advanced.matrix[2,1] = green # tab
    device.fx.advanced.matrix[2,2] = red # q
    device.fx.advanced.matrix[2,3] = green # w
    device.fx.advanced.matrix[2,5] = green # r
    device.fx.advanced.matrix[2,6] = yellow # t
    device.fx.advanced.matrix[2,10] = green # o
    device.fx.advanced.matrix[2,11] = green # p
    device.fx.advanced.matrix[2,12] = green # p
    device.fx.advanced.matrix[2,13] = green # p
    device.fx.advanced.matrix[3,2] = yellow # a
    device.fx.advanced.matrix[3,3] = magenta # s
    device.fx.advanced.matrix[3,4] = green # d
    device.fx.advanced.matrix[3,5] = yellow # f
    device.fx.advanced.matrix[3,6] = green # g
    device.fx.advanced.matrix[3,8] = green # j
    device.fx.advanced.matrix[3,9] = green # k
    device.fx.advanced.matrix[3,10] = green # l
    device.fx.advanced.matrix[3,15] = green # enter
    device.fx.advanced.matrix[4,3] = yellow # y
    device.fx.advanced.matrix[4,4] = yellow # x
    device.fx.advanced.matrix[4,5] = yellow # c
    device.fx.advanced.matrix[4,6] = yellow # v
    device.fx.advanced.matrix[4,10] = green # ,
    device.fx.advanced.matrix[4,11] = green # .
    device.fx.advanced.matrix[4,12] = green # -
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,13] = green # arrow
    device.fx.advanced.matrix[5,14] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.matrix[5,1] = white # strg
    device.fx.advanced.matrix[5,11] = white # strg
    device.fx.advanced.draw()
    set_max_brightness(device)


def update_workspaces():
    device = getKeyboard(device_manager)
    
    fill_workspaces(device)
    device.fx.advanced.draw_fb_or()

def light_super():
    device = getKeyboard(device_manager)
    clear_light(device)
    
    light_modifiers(device)
    fill_workspaces(device)
    device.fx.advanced.matrix[0,9] = green
    device.fx.advanced.matrix[0,10] = green
    device.fx.advanced.matrix[2,2] = red # q
    device.fx.advanced.matrix[2,3] = red # w
    device.fx.advanced.matrix[2,5] = green # r
    device.fx.advanced.matrix[2,6] = green # t
    device.fx.advanced.matrix[2,11] = green # p
    device.fx.advanced.matrix[3,4] = green # d
    device.fx.advanced.matrix[3,5] = green # f
    device.fx.advanced.matrix[3,7] = green # h
    device.fx.advanced.matrix[3,10] = green # l
    device.fx.advanced.matrix[3,15] = green # enter
    device.fx.advanced.matrix[4,3] = green # y
    device.fx.advanced.matrix[4,4] = green # x
    device.fx.advanced.matrix[4,6] = green # v
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,13] = green # arrow
    device.fx.advanced.matrix[5,14] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.matrix[5,3] = white # super
    device.fx.advanced.draw()
    set_max_brightness(device)

def light_shift():
    device = getKeyboard(device_manager)
    clear_light(device)
    
    light_modifiers(device)

    device.fx.advanced.matrix[0,13] = green
    device.fx.advanced.matrix[1,1] = green
    device.fx.advanced.matrix[1,2] = green 
    device.fx.advanced.matrix[1,3] = green
    device.fx.advanced.matrix[1,4] = green
    device.fx.advanced.matrix[1,5] = green
    device.fx.advanced.matrix[1,6] = green
    device.fx.advanced.matrix[1,7] = green
    device.fx.advanced.matrix[1,8] = green
    device.fx.advanced.matrix[1,9] = green
    device.fx.advanced.matrix[1,10] = yellow
    device.fx.advanced.matrix[1,11] = yellow
    device.fx.advanced.matrix[1,12] = green
    device.fx.advanced.matrix[1,13] = green
    device.fx.advanced.matrix[2,1] = green
    device.fx.advanced.matrix[2,2] = green 
    device.fx.advanced.matrix[2,3] = green
    device.fx.advanced.matrix[2,4] = green
    device.fx.advanced.matrix[2,5] = green
    device.fx.advanced.matrix[2,6] = green
    device.fx.advanced.matrix[2,7] = green
    device.fx.advanced.matrix[2,8] = green
    device.fx.advanced.matrix[2,9] = green
    device.fx.advanced.matrix[2,10] = green
    device.fx.advanced.matrix[2,11] = green
    device.fx.advanced.matrix[2,12] = green
    device.fx.advanced.matrix[2,13] = green
    device.fx.advanced.matrix[3,2] = green 
    device.fx.advanced.matrix[3,3] = green
    device.fx.advanced.matrix[3,4] = green
    device.fx.advanced.matrix[3,5] = green
    device.fx.advanced.matrix[3,6] = green
    device.fx.advanced.matrix[3,7] = green
    device.fx.advanced.matrix[3,8] = green
    device.fx.advanced.matrix[3,9] = green
    device.fx.advanced.matrix[3,10] = green
    device.fx.advanced.matrix[3,11] = yellow
    device.fx.advanced.matrix[3,12] = green
    device.fx.advanced.matrix[3,13] = green
    device.fx.advanced.matrix[3,15] = green
    device.fx.advanced.matrix[4,1] = white 
    device.fx.advanced.matrix[4,2] = green 
    device.fx.advanced.matrix[4,3] = green
    device.fx.advanced.matrix[4,4] = green
    device.fx.advanced.matrix[4,5] = green
    device.fx.advanced.matrix[4,6] = green
    device.fx.advanced.matrix[4,7] = green
    device.fx.advanced.matrix[4,8] = green
    device.fx.advanced.matrix[4,9] = green
    device.fx.advanced.matrix[4,10] = green
    device.fx.advanced.matrix[4,11] = green
    device.fx.advanced.matrix[4,12] = green
    device.fx.advanced.matrix[4,13] = green
    device.fx.advanced.matrix[4,15] = white
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,13] = green # arrow
    device.fx.advanced.matrix[5,14] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.draw()
    set_max_brightness(device)

def light_alt():
    device = getKeyboard(device_manager)
    clear_light(device)
    
    light_modifiers(device)

    device.fx.advanced.matrix[1,15] = green # backspace
    device.fx.advanced.matrix[2,1] = green # tab
    device.fx.advanced.matrix[5,4] = white # alt
    device.fx.advanced.matrix[5,9] = white # alt
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.draw()
    set_max_brightness(device)

def light_altshift():
    device = getKeyboard(device_manager)
    clear_light(device)
    
    light_modifiers(device)

    device.fx.advanced.matrix[1,2] = green 
    device.fx.advanced.matrix[1,3] = green
    device.fx.advanced.matrix[1,4] = green
    device.fx.advanced.matrix[1,5] = green
    device.fx.advanced.matrix[1,6] = green
    device.fx.advanced.matrix[1,7] = green
    device.fx.advanced.matrix[1,8] = green
    device.fx.advanced.matrix[1,9] = green
    device.fx.advanced.matrix[1,10] = green
    device.fx.advanced.matrix[4,1] = white 
    device.fx.advanced.matrix[4,15] = white
    device.fx.advanced.matrix[5,4] = white # alt
    device.fx.advanced.matrix[5,9] = white # alt
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,13] = green # arrow
    device.fx.advanced.matrix[5,14] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.draw()
    set_max_brightness(device)


def light_altsuper():
    device = getKeyboard(device_manager)
    
    light_unsupported()
    device.fx.advanced.draw()

def light_shiftsuper():
    device = getKeyboard(device_manager)
    clear_light(device)
    
    light_modifiers(device)

    fill_workspaces(device)
    device.fx.advanced.matrix[0,2] = red
    device.fx.advanced.matrix[0,3] = magenta
    device.fx.advanced.matrix[0,4] = orange
    device.fx.advanced.matrix[0,5] = yellow
    device.fx.advanced.matrix[0,6] = (255, 255, 255)
    device.fx.advanced.matrix[0,7] = cyan
    device.fx.advanced.matrix[0,8] = blue
    device.fx.advanced.matrix[0,9] = (10, 10, 10)
    device.fx.advanced.matrix[0,10] = (50, 50, 50)
    device.fx.advanced.matrix[0,11] = (100, 100, 100)
    device.fx.advanced.matrix[0,12] = (150, 150, 150)
    device.fx.advanced.matrix[0,13] = (255, 255, 255)
    device.fx.advanced.matrix[2,4] = red
    device.fx.advanced.matrix[2,5] = green
    device.fx.advanced.matrix[2,6] = red
    device.fx.advanced.matrix[2,11] = green # p
    device.fx.advanced.matrix[3,15] = red # enter
    device.fx.advanced.matrix[4,1] = white 
    device.fx.advanced.matrix[4,3] = green 
    device.fx.advanced.matrix[4,4] = green 
    device.fx.advanced.matrix[4,5] = yellow # c 
    device.fx.advanced.matrix[4,6] = yellow 
    device.fx.advanced.matrix[4,7] = yellow 
    device.fx.advanced.matrix[4,8] = yellow 
    device.fx.advanced.matrix[4,15] = white
    device.fx.advanced.matrix[5,3] = white # super
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,13] = green # arrow
    device.fx.advanced.matrix[5,14] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.draw()
    set_max_brightness(device)

def light_ctrlshiftsuper():
    device = getKeyboard(device_manager)
    clear_light(device)
    
    light_unsupported()

def light_ctrlsuper():
    device = getKeyboard(device_manager)
    clear_light(device)
    
    light_unsupported()

def light_ctrlalt():
    device = getKeyboard(device_manager)
    clear_light(device)
    
    light_unsupported()

def light_ctrlaltshift():
    device = getKeyboard(device_manager)
    clear_light(device)
    
    light_unsupported()

def light_ctrlshift():
    device = getKeyboard(device_manager)
    clear_light(device)
    clear_light(device)
    light_modifiers(device)
    device.fx.advanced.matrix[1,2] = green 
    device.fx.advanced.matrix[1,3] = green
    device.fx.advanced.matrix[1,4] = green
    device.fx.advanced.matrix[1,5] = green
    device.fx.advanced.matrix[1,6] = green
    device.fx.advanced.matrix[1,7] = green
    device.fx.advanced.matrix[1,8] = green
    device.fx.advanced.matrix[1,9] = green
    device.fx.advanced.matrix[1,10] = green
    device.fx.advanced.matrix[2,1] = green # tab
    device.fx.advanced.matrix[2,3] = green
    device.fx.advanced.matrix[2,6] = green
    device.fx.advanced.matrix[3,3] = green
    device.fx.advanced.matrix[3,5] = green
    device.fx.advanced.matrix[3,6] = green
    device.fx.advanced.matrix[4,1] = white 
    device.fx.advanced.matrix[4,3] = green 
    device.fx.advanced.matrix[4,5] = yellow 
    device.fx.advanced.matrix[4,6] = yellow 
    device.fx.advanced.matrix[4,15] = white
    device.fx.advanced.matrix[5,1] = white # strg
    device.fx.advanced.matrix[5,11] = white # strg
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,13] = green # arrow
    device.fx.advanced.matrix[5,14] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.draw()
    set_max_brightness(device)

def light_default():
    device = getKeyboard(device_manager)
    if reactive_effect[0]:
        reactive(device)
    elif env_effect[0]:
        if language_us[0]:
            color_to_fill = environment_color[0]
        else:
            color_to_fill = red
        fill(device, color_to_fill)
    else:
        wave(device)
    set_brightness_back(device)

def light_unsupported():
    random_keys()

def random_keys():
    device = getKeyboard(device_manager)
    rows, cols = device.fx.advanced.rows, device.fx.advanced.cols

    for row in range(rows):
        for col in range(cols):
            device.fx.advanced.matrix[row, col] = random_color()

    device.fx.advanced.draw()

def wave(device):
    device.fx.wave(razer_constants.WAVE_RIGHT)

def setreactive():
    print("set")
    device = getKeyboard(device_manager)
    reactive_effect[0] = True
    reactive(device)

def unsetreactive():
    print("unset")
    reactive_effect[0] = False
    light_default()

def reactive(device):
    device.fx.reactive(environment_color[0][0], environment_color[0][1], environment_color[0][2], 4)

while True:
    line = pipe[0].read(1)
    selector = ord(line[-1])

    # print(selector)
    if selector == 0: 
        light_ctrlshiftsuper() 
    elif selector == 1: 
        light_ctrlsuper()      
    elif selector == 2: 
        light_ctrlaltshift()   
    elif selector == 3: 
        light_ctrlshift()      
    elif selector == 4: 
        light_ctrlalt()        
    elif selector == 5: 
        light_ctrl()           
    elif selector == 6: 
        light_shiftsuper()     
    elif selector == 7: 
        light_altsuper()       
    elif selector == 8: 
        light_super()
    elif selector == 9: 
        light_altshift()       
    elif selector == 10:  
        light_shift()          
    elif selector == 11:  
        light_alt()            
    elif selector == 12:  
        light_default()        
    elif selector == 15:
        switchlang()
    elif selector == 14:  
        update_workspaces()    
    elif selector == 56:  
        setreactive()    
    elif selector == 57:  
        unsetreactive()    
