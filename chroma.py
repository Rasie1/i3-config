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
        server.register_function(light_ctrl)
        server.register_function(light_super)
        server.register_function(light_shift)
        server.register_function(light_altshift)
        server.register_function(light_ctrlsuper)
        server.register_function(light_ctrlalt)
        server.register_function(light_ctrlshift)
        server.register_function(light_default)
        server.register_function(wave)

        server.serve_forever()

def switchlang(us):
    if us:
        language = "us"
    else:
        language = "ru"
    subprocess.call(["setxkbmap", language])

red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
darkgreen = (0, 10, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
def random_color():
    rgb = colorsys.hsv_to_rgb(random.uniform(0, 1), random.uniform(0.5, 1), 1)
    return tuple(map(lambda x: int(256 * x), rgb))
def clear_light(device):
    rows, cols = device.fx.advanced.rows, device.fx.advanced.cols
    for row in range(rows):
        for col in range(cols):
            device.fx.advanced.matrix[row, col] = black

def light_ctrl():
    for device in device_manager.devices:
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
        device.fx.advanced.matrix[2,1] = green  
        device.fx.advanced.matrix[2,2] = red 
        device.fx.advanced.matrix[2,5] = green # r
        device.fx.advanced.matrix[2,6] = green # t
        device.fx.advanced.matrix[2,10] = green # o
        device.fx.advanced.matrix[2,11] = green # p
        device.fx.advanced.matrix[3,2] = green # a
        device.fx.advanced.matrix[3,3] = green # s
        device.fx.advanced.matrix[3,4] = green # d
        device.fx.advanced.matrix[3,5] = green # f
        device.fx.advanced.matrix[3,6] = green # g
        device.fx.advanced.matrix[3,9] = green # k
        device.fx.advanced.matrix[3,15] = green # enter
        device.fx.advanced.matrix[4,1] = blue # shift
        device.fx.advanced.matrix[4,3] = green # y
        device.fx.advanced.matrix[4,4] = yellow # x
        device.fx.advanced.matrix[4,5] = yellow # c
        device.fx.advanced.matrix[4,6] = yellow # v
        device.fx.advanced.matrix[4,12] = green # -
        device.fx.advanced.matrix[4,15] = blue # shift
        device.fx.advanced.matrix[5,1] = white # strg
        device.fx.advanced.matrix[5,2] = blue # fn
        device.fx.advanced.matrix[5,3] = blue # super
        device.fx.advanced.matrix[5,4] = blue # alt
        device.fx.advanced.matrix[5,9] = blue # alt
        device.fx.advanced.matrix[5,10] = blue # fn
        device.fx.advanced.matrix[5,11] = white # strg
        device.fx.advanced.matrix[5,12] = green # arrow
        device.fx.advanced.matrix[5,13] = green # arrow
        device.fx.advanced.matrix[5,14] = green # arrow
        device.fx.advanced.matrix[5,15] = green # arrow
        device.fx.advanced.draw()


def light_super():
    for device in device_manager.devices:
        clear_light(device)
        
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
        device.fx.advanced.matrix[2,2] = red # q
        device.fx.advanced.matrix[2,3] = green # w
        device.fx.advanced.matrix[2,6] = green # t
        device.fx.advanced.matrix[2,11] = green # p
        device.fx.advanced.matrix[3,4] = green # d
        device.fx.advanced.matrix[3,7] = green # h
        device.fx.advanced.matrix[3,10] = green # l
        device.fx.advanced.matrix[3,15] = green # enter
        device.fx.advanced.matrix[4,1] = blue # shift
        device.fx.advanced.matrix[4,3] = green # y
        device.fx.advanced.matrix[4,4] = green # x
        device.fx.advanced.matrix[4,6] = green # v
        device.fx.advanced.matrix[4,10] = green # ,
        device.fx.advanced.matrix[4,11] = green # .
        device.fx.advanced.matrix[4,15] = blue # shift
        device.fx.advanced.matrix[5,1] = blue # strg
        device.fx.advanced.matrix[5,3] = white # super
        device.fx.advanced.matrix[5,11] = blue # strg
        device.fx.advanced.matrix[5,12] = green # arrow
        device.fx.advanced.matrix[5,13] = green # arrow
        device.fx.advanced.matrix[5,14] = green # arrow
        device.fx.advanced.matrix[5,15] = green # arrow
        device.fx.advanced.draw()

def light_shift():
    for device in device_manager.devices:
        clear_light(device)

def light_altshift():
    for device in device_manager.devices:
        clear_light(device)

def light_ctrlsuper():
    for device in device_manager.devices:
        clear_light(device)

def light_ctrlalt():
    for device in device_manager.devices:
        clear_light(device)

def light_ctrlshift():
    for device in device_manager.devices:
        clear_light(device)

def light_default():
    wave()

def random_keys():
    for device in device_manager.devices:
        rows, cols = device.fx.advanced.rows, device.fx.advanced.cols

        for row in range(rows):
            for col in range(cols):
                device.fx.advanced.matrix[row, col] = random_color()

        device.fx.advanced.draw()


def wave():
    for device in device_manager.devices:
        device.fx.wave(razer_constants.WAVE_RIGHT)


main()
