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
keymap = {'ctrl': 0, 'windows': 1, 'shift': 2, 'alt': 3}
keys = [False, False, False, False]
def light_up_default(key):
    keynum = keymap[key]
    keys[keynum] = False
    
    if keynum != 2 and keynum != 3 and keyboard.is_pressed("shift+alt"):
        will_switch_lang[0] = False

    if not keys[0] and not keys[1] and not keys[2] and not keys[3]:
        chroma.light_default()
    elif keys[0] and not keys[1] and not keys[2] and not keys[3]:
        chroma.light_ctrl(False)
    elif not keys[0] and keys[1] and not keys[2] and not keys[3]:
        chroma.light_super(False)
    elif not keys[0] and not keys[1] and keys[2] and not keys[3]:
        chroma.light_shift(False)
    elif not keys[0] and not keys[1] and not keys[2] and keys[3]:
        chroma.light_alt(False)
    elif keys[0] and keys[1] and not keys[2] and not keys[3]:
        chroma.light_ctrlsuper()
    elif keys[0] and not keys[1] and keys[2] and not keys[3]:
        chroma.light_ctrlshift()
    elif keys[0] and not keys[1] and not keys[2] and keys[3]:
        chroma.light_ctrlalt()
    elif not keys[0] and keys[1] and keys[2] and not keys[3]:
        chroma.light_shiftsuper()
    elif not keys[0] and not keys[1] and keys[2] and keys[3]:
        chroma.light_altsuper()
    elif keys[0] and keys[1] and keys[2] and not keys[3]:
        chroma.light_ctrlshiftsuper()
    elif keys[0] and keys[1] and keys[2] and not keys[3]:
        chroma.light_ctrlaltshift()

def on_shiftalt_release():
    if will_switch_lang[0]:
        chroma.switchlang()
    else:
        will_switch_lang[0] = True

def on_press_action(c):
    if c.name not in keymap:
        return
    keynum = keymap[c.name]
    if keynum != 2 and keynum != 3 and keyboard.is_pressed("shift+alt"):
        will_switch_lang[0] = False
    if not keys[0] and not keys[1] and not keys[2] and not keys[3]:
        if keynum == 0:
            chroma.light_ctrl(True)
        elif keynum == 1:
            chroma.light_super(True)
        elif keynum == 2:
            chroma.light_shift(True)
        elif keynum == 3:
            chroma.light_alt(True)
    elif keys[0] and not keys[1] and not keys[2] and not keys[3]:
        if keynum == 1:
            chroma.light_ctrlsuper()
        elif keynum == 2:
            chroma.light_ctrlshift()
        elif keynum == 3:
            chroma.light_ctrlalt()
    elif not keys[0] and keys[1] and not keys[2] and not keys[3]:
        if keynum == 0:
            chroma.light_ctrlsuper()
        elif keynum == 2:
            chroma.light_shiftsuper()
        elif keynum == 3:
            chroma.light_altsuper()
    elif not keys[0] and not keys[1] and keys[2] and not keys[3]:
        if keynum == 0:
            chroma.light_ctrlshift()
        elif keynum == 1:
            chroma.light_shiftsuper()
        elif keynum == 3:
            chroma.light_altshift()
    elif not keys[0] and not keys[1] and not keys[2] and keys[3]:
        if keynum == 0:
            chroma.light_ctrlalt()
        elif keynum == 1:
            chroma.light_altsuper()
        elif keynum == 2:
            chroma.light_altshift()
    elif keys[0] and keys[1] and not keys[2] and not keys[3]:
        if keynum == 2:
            chroma.light_ctrlshiftsuper()
    elif keys[0] and not keys[1] and keys[2] and not keys[3]:
        if keynum == 1:
            chroma.light_ctrlshiftsuper()
        elif keynum == 3:
            chroma.light_ctrlaltshift()
    elif keys[0] and not keys[1] and not keys[2] and keys[3]:
        if keynum == 2:
            chroma.light_ctrlaltshift()
    elif not keys[0] and keys[1] and keys[2] and not keys[3]:
        if keynum == 0:
            chroma.light_ctrlshiftsuper()
    elif not keys[0] and not keys[1] and keys[2] and keys[3]:
        if keynum == 0:
            chroma.light_ctrlaltshift()
    keys[keynum] = True

main()

