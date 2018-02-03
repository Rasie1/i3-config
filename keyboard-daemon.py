#!/usr/bin/python
import keyboard
import colorsys
import random
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants
import os
import pwd
import subprocess
import sys
import time
import xmlrpc.client

chroma = xmlrpc.client.ServerProxy('http://localhost:16767')

def main():
    keyboard.add_hotkey('shift+alt', on_shiftalt_release, trigger_on_release=True)
    keyboard.on_press(on_press_action)
    keyboard.add_hotkey('windows', light_up_default, args=["windows"], trigger_on_release=True)
    keyboard.add_hotkey('ctrl', light_up_default, args=["ctrl"], trigger_on_release=True)
    keyboard.add_hotkey('shift', light_up_default, args=["shift"], trigger_on_release=True)
    keyboard.add_hotkey('alt', light_up_default, args=["alt"], trigger_on_release=True)
    
    keyboard.wait()

will_switch_lang = [True]
# [0] - ctrl
# [1] - windows
# [2] - shift
# [3] - alt
keys = [False, False, False, False]
def light_up_default(key):
    if keys[0] and key == "ctrl" or keys[1] and key == "windows" or keys[2] and key == "shift" or keys[3] and key == "alt":
        keys[0] = False
        keys[1] = False
        keys[2] = False
        keys[3] = False
        chroma.light_default()

def on_shiftalt_release():
    if will_switch_lang[0]:
        chroma.switchlang()
    else:
        will_switch_lang[0] = True

def on_press_action(c):
    if c.name != "shift" and c.name != "alt" and keyboard.is_pressed("shift+alt"):
        will_switch_lang[0] = False

    if c.name == "shift" and keys[0] == True and keys[1] == False and keys[2] == False and keys[3] == False or \
       c.name == "ctrl" and keys[0] == False and keys[1] == False and keys[2] == True and keys[3] == False:
        keys[0] == True
        keys[2] == True
        chroma.light_ctrlshift()
    if c.name == "shift" and not any(keys):
        keys[2] = True
        chroma.light_shift()
    elif c.name == "ctrl" and not any(keys):
        keys[0] = True
        chroma.light_ctrl()
    elif c.name == "alt" and not any(keys):
        keys[3] = True
        chroma.light_alt()
    elif c.name == "windows" and not any(keys):
        keys[1] = True
        chroma.light_super()


main()

