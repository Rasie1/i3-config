#!/usr/bin/python
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import colorsys
import random
import subprocess
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants

device_manager = DeviceManager()
device_manager.sync_effects = False

def main():
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(("localhost", 16767),
                            requestHandler=RequestHandler,
                            allow_none=True,
                            logRequests=False) as server:
        server.register_introspection_functions()

        server.register_function(random_keys)
        server.register_function(switchlang)
        server.register_function(light_alt)
        server.register_function(light_ctrl)
        server.register_function(light_super)
        server.register_function(light_shift)
        server.register_function(light_altshift)
        server.register_function(light_altsuper)
        server.register_function(light_shiftsuper)
        server.register_function(light_ctrlsuper)
        server.register_function(light_ctrlalt)
        server.register_function(light_ctrlshiftsuper)
        server.register_function(light_ctrlaltshift)
        server.register_function(light_ctrlshift)
        server.register_function(light_default)
        server.register_function(wave)

        server.serve_forever()


red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
darkgreen = (0, 10, 0)
blue = (0, 0, 255)
magenta = (255, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
def language_dependent_color():
    if language_us[0]:
        return blue
    else:
        return magenta

previous_brightness = [40]
language_us = [True]
subprocess.call(["setxkbmap", "us"])

def switchlang():
    if language_us[0]:
        language = "ru"
        language_us[0] = False
    else:
        language = "us"
        language_us[0] = True
    subprocess.call(["setxkbmap", language])

def random_color():
    rgb = colorsys.hsv_to_rgb(random.uniform(0, 1), random.uniform(0.5, 1), 1)
    return tuple(map(lambda x: int(256 * x), rgb))
def clear_light(device):
    rows, cols = device.fx.advanced.rows, device.fx.advanced.cols
    for row in range(rows):
        for col in range(cols):
            device.fx.advanced.matrix[row, col] = black
def fill_workspaces(device):
    device.fx.advanced.matrix[1,1] = darkgreen # numbers
    device.fx.advanced.matrix[1,2] = white 
    device.fx.advanced.matrix[1,3] = darkgreen
    device.fx.advanced.matrix[1,4] = green
    device.fx.advanced.matrix[1,5] = darkgreen
    device.fx.advanced.matrix[1,6] = green
    device.fx.advanced.matrix[1,7] = green
    device.fx.advanced.matrix[1,8] = darkgreen
    device.fx.advanced.matrix[1,9] = darkgreen
    device.fx.advanced.matrix[1,10] = darkgreen
    device.fx.advanced.matrix[1,11] = darkgreen
    device.fx.advanced.matrix[1,12] = darkgreen
    device.fx.advanced.matrix[1,13] = darkgreen

def light_ctrl():
    device = device_manager.devices[0]
    clear_light(device)

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
    device.fx.advanced.matrix[2,6] = green # t
    device.fx.advanced.matrix[2,10] = green # o
    device.fx.advanced.matrix[2,11] = green # p
    device.fx.advanced.matrix[2,12] = green # p
    device.fx.advanced.matrix[2,13] = green # p
    device.fx.advanced.matrix[3,2] = green # a
    device.fx.advanced.matrix[3,3] = green # s
    device.fx.advanced.matrix[3,4] = green # d
    device.fx.advanced.matrix[3,5] = green # f
    device.fx.advanced.matrix[3,6] = green # g
    device.fx.advanced.matrix[3,9] = green # k
    device.fx.advanced.matrix[3,15] = green # enter
    device.fx.advanced.matrix[4,1] = language_dependent_color() # shift
    device.fx.advanced.matrix[4,3] = green # y
    device.fx.advanced.matrix[4,4] = yellow # x
    device.fx.advanced.matrix[4,5] = yellow # c
    device.fx.advanced.matrix[4,6] = yellow # v
    device.fx.advanced.matrix[4,12] = green # -
    device.fx.advanced.matrix[4,15] = language_dependent_color() # shift
    device.fx.advanced.matrix[5,1] = white # strg
    device.fx.advanced.matrix[5,2] = language_dependent_color() # fn
    device.fx.advanced.matrix[5,3] = language_dependent_color() # super
    device.fx.advanced.matrix[5,4] = language_dependent_color() # alt
    device.fx.advanced.matrix[5,9] = language_dependent_color() # alt
    device.fx.advanced.matrix[5,10] = language_dependent_color() # fn
    device.fx.advanced.matrix[5,11] = white # strg
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,13] = green # arrow
    device.fx.advanced.matrix[5,14] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.draw()

    device.brightness = 100

def light_super():
    device = device_manager.devices[0]
    clear_light(device)
    
    fill_workspaces(device)
    device.fx.advanced.matrix[2,2] = red # q
    device.fx.advanced.matrix[2,3] = green # w
    device.fx.advanced.matrix[2,6] = green # t
    device.fx.advanced.matrix[2,11] = green # p
    device.fx.advanced.matrix[3,4] = green # d
    device.fx.advanced.matrix[3,7] = green # h
    device.fx.advanced.matrix[3,10] = green # l
    device.fx.advanced.matrix[3,15] = green # enter
    device.fx.advanced.matrix[4,1] = language_dependent_color() # shift
    device.fx.advanced.matrix[4,3] = green # y
    device.fx.advanced.matrix[4,4] = green # x
    device.fx.advanced.matrix[4,6] = green # v
    device.fx.advanced.matrix[4,10] = green # ,
    device.fx.advanced.matrix[4,11] = green # .
    device.fx.advanced.matrix[4,15] = language_dependent_color() # shift
    device.fx.advanced.matrix[5,1] = language_dependent_color() # strg
    device.fx.advanced.matrix[5,3] = white # super
    device.fx.advanced.matrix[5,11] = language_dependent_color() # strg
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,13] = green # arrow
    device.fx.advanced.matrix[5,14] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.draw()
    device.brightness = 100

def light_shift():
    device = device_manager.devices[0]
    clear_light(device)

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
    device.fx.advanced.matrix[1,10] = green
    device.fx.advanced.matrix[1,11] = green
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
    device.fx.advanced.matrix[3,11] = green
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
    device.fx.advanced.matrix[5,1] = language_dependent_color() # strg
    device.fx.advanced.matrix[5,2] = language_dependent_color() # fn
    device.fx.advanced.matrix[5,3] = language_dependent_color() # super
    device.fx.advanced.matrix[5,4] = language_dependent_color() # alt
    device.fx.advanced.matrix[5,9] = language_dependent_color() # alt
    device.fx.advanced.matrix[5,10] = language_dependent_color() # fn
    device.fx.advanced.matrix[5,11] = language_dependent_color() # strg
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,13] = green # arrow
    device.fx.advanced.matrix[5,14] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.draw()
    device.brightness = 100

def light_alt():
    device = device_manager.devices[0]
    clear_light(device)
    device.fx.advanced.matrix[2,1] = green # tab
    device.fx.advanced.matrix[4,1] = language_dependent_color() 
    device.fx.advanced.matrix[4,15] = language_dependent_color()
    device.fx.advanced.matrix[5,1] = language_dependent_color() # strg
    device.fx.advanced.matrix[5,2] = language_dependent_color() # fn
    device.fx.advanced.matrix[5,4] = white # alt
    device.fx.advanced.matrix[5,9] = white # alt
    device.fx.advanced.matrix[5,10] = language_dependent_color() # fn
    device.fx.advanced.matrix[5,11] = language_dependent_color() # strg
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.draw()
    device.brightness = 100

def light_altshift():
    device = device_manager.devices[0]
    clear_light(device)
    device.fx.advanced.draw()

    device.brightness = 100

def light_altsuper():
    device = device_manager.devices[0]
    clear_light(device)
    device.fx.advanced.draw()

    device.brightness = 100

def light_shiftsuper():
    device = device_manager.devices[0]
    clear_light(device)

    fill_workspaces(device)
    device.fx.advanced.matrix[2,4] = red
    device.fx.advanced.matrix[2,5] = green
    device.fx.advanced.matrix[2,11] = green # p
    device.fx.advanced.matrix[3,15] = red # enter
    device.fx.advanced.matrix[4,1] = white 
    device.fx.advanced.matrix[4,3] = green 
    device.fx.advanced.matrix[4,4] = green 
    device.fx.advanced.matrix[4,10] = green 
    device.fx.advanced.matrix[4,11] = green 
    device.fx.advanced.matrix[4,15] = white
    device.fx.advanced.matrix[5,1] = language_dependent_color() # strg
    device.fx.advanced.matrix[5,2] = language_dependent_color() # fn
    device.fx.advanced.matrix[5,3] = white # super
    device.fx.advanced.matrix[5,4] = language_dependent_color() # alt
    device.fx.advanced.matrix[5,9] = language_dependent_color() # alt
    device.fx.advanced.matrix[5,10] = language_dependent_color() # fn
    device.fx.advanced.matrix[5,11] = language_dependent_color() # strg
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,13] = green # arrow
    device.fx.advanced.matrix[5,14] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.draw()

    device.brightness = 100

def light_ctrlshiftsuper():
    device = device_manager.devices[0]
    clear_light(device)
    device.fx.advanced.draw()

    device.brightness = 100

def light_ctrlsuper():
    device = device_manager.devices[0]
    clear_light(device)
    device.fx.advanced.draw()

    device.brightness = 100

def light_ctrlalt():
    device = device_manager.devices[0]
    clear_light(device)
    device.fx.advanced.draw()

    device.brightness = 100

def light_ctrlaltshift():
    device = device_manager.devices[0]
    clear_light(device)
    device.fx.advanced.draw()

    device.brightness = 100

def light_ctrlshift():
    device = device_manager.devices[0]
    clear_light(device)
    device.fx.advanced.matrix[1,2] = green 
    device.fx.advanced.matrix[1,3] = green
    device.fx.advanced.matrix[1,4] = green
    device.fx.advanced.matrix[1,5] = green
    device.fx.advanced.matrix[1,6] = green
    device.fx.advanced.matrix[1,7] = green
    device.fx.advanced.matrix[1,8] = green
    device.fx.advanced.matrix[1,9] = green
    device.fx.advanced.matrix[1,10] = green
    device.fx.advanced.matrix[2,3] = green
    device.fx.advanced.matrix[2,3] = green
    device.fx.advanced.matrix[3,6] = green
    device.fx.advanced.matrix[4,1] = white 
    device.fx.advanced.matrix[4,15] = white
    device.fx.advanced.matrix[5,1] = white # strg
    device.fx.advanced.matrix[5,2] = language_dependent_color() # fn
    device.fx.advanced.matrix[5,3] = language_dependent_color() # super
    device.fx.advanced.matrix[5,4] = language_dependent_color() # alt
    device.fx.advanced.matrix[5,9] = language_dependent_color() # alt
    device.fx.advanced.matrix[5,10] = language_dependent_color() # fn
    device.fx.advanced.matrix[5,11] = white # strg
    device.fx.advanced.matrix[5,12] = green # arrow
    device.fx.advanced.matrix[5,13] = green # arrow
    device.fx.advanced.matrix[5,14] = green # arrow
    device.fx.advanced.matrix[5,15] = green # arrow
    device.fx.advanced.draw()

    device.brightness = 100

def light_default():
    device = device_manager.devices[0]
    device.brightness = previous_brightness[0]
    wave()

def random_keys():
    device = device_manager.devices[0]
    rows, cols = device.fx.advanced.rows, device.fx.advanced.cols

    for row in range(rows):
        for col in range(cols):
            device.fx.advanced.matrix[row, col] = random_color()

    device.fx.advanced.draw()


def wave():
    device = device_manager.devices[0]
    device.fx.wave(razer_constants.WAVE_RIGHT)


main()
