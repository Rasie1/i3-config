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
    keyboard.on_press(block_switcher)
    keyboard.add_hotkey('windows', light_up_default, args=["windows"], trigger_on_release=True)
    keyboard.add_hotkey('ctrl', light_up_default, args=["ctrl"], trigger_on_release=True)
    
    keyboard.wait()

# [0] - will switch lang
# [1] - us/ru
lang = [True, False]
# [0] - ctrl
# [1] - windows
keys = [False, False]
def light_up_default(key):
    if keys[0] and key == "ctrl" or keys[1] and key == "windows":
        keys[0] = False
        keys[1] = False
        chroma.wave()


def light_up_ctrl():
    chroma.light_ctrl()
def light_up_windows():
    chroma.light_super()

def on_shiftalt_release():
    if lang[0]:
        lang[1] = not lang[1]
        chroma.switchlang(lang[1])
    else:
        lang[0] = True

def block_switcher(c):
    if c.name != "shift" and c.name != "alt" and keyboard.is_pressed("shift+alt"):
        lang[0] = False
    if c.name == "ctrl" and not any(keys):
        keys[0] = True
        light_up_ctrl()
    elif c.name == "windows" and not any(keys):
        keys[1] = True
        light_up_windows()


main()

