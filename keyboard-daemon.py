import keyboard
import colorsys
import random
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants
import os
import pwd
import subprocess
import sys

import xmlrpc.client

chroma = xmlrpc.client.ServerProxy('http://localhost:16767')

def main():
    keyboard.add_hotkey('shift+alt', on_shiftalt_release, trigger_on_release=True)
    keyboard.on_press(block_switcher)
    keyboard.add_hotkey('windows', light_up_default, args=["windows"], trigger_on_release=True)
    keyboard.add_hotkey('ctrl', light_up_default, args=["ctrl"], trigger_on_release=True)
    
    keyboard.wait()



def random_color():
    rgb = colorsys.hsv_to_rgb(random.uniform(0, 1), random.uniform(0.5, 1), 1)
    return tuple(map(lambda x: int(256 * x), rgb))

# [0] - will switch lang
# [1] - us/ru
lang = [True, False]
# [0] - ctrl
# [1] - windows
keys = [False, False]
def light_up_default(key):
    if keys[0] and key == "ctrl" or keys[1] and key == "windows":
        print("default")
        keys[0] = False
        keys[1] = False
        chroma.wave()


def light_up_ctrl():
    print("ctrl")
    chroma.random_keys()
def light_up_windows():
    chroma.random_keys()

def on_shiftalt_release():
    if lang[0]:
        if lang[1]:
            language = "us"
        else:
            language = "ru"
        lang[1] = not lang[1]
        subprocess.call(["setxkbmap", language])
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



if __name__ == '__main__':
    main()
