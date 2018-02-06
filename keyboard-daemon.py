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
    keyboard.on_release(on_release_action)
    
    keyboard.wait()

will_switch_lang = [True]
keymap = {'ctrl': 0, 'windows': 1, 'shift': 2, 'alt': 3}
keys = [False, False, False, False]

def update_light():
    if keys[0]:
        if keys[1]:
            if keys[2]:
                if not keys[3]:
                    chroma.light_ctrlshiftsuper()
            else:
                if not keys[3]:
                    chroma.light_ctrlsuper()
        else:
            if keys[2]:
                if keys[3]:
                    chroma.light_ctrlaltshift()
                else:
                    chroma.light_ctrlshift()
            else:
                if keys[3]:
                    chroma.light_ctrlalt()
                else:
                    chroma.light_ctrl()
    else:
        if keys[1]:
            if keys[2]:
                chroma.light_shiftsuper()
            else:
                if keys[3]:
                    chroma.light_altsuper()
                else:
                    chroma.light_super()
        else:
            if keys[2]:
                if keys[3]:
                    chroma.light_altshift()
                else:
                    chroma.light_shift()
            else:
                if keys[3]:
                    chroma.light_alt()
                else:
                    chroma.light_default()
        
def on_release_action(c):
    if c.name not in keymap:
        return
    keynum = keymap[c.name]
    keys[keynum] = False
    
    if keynum != 2 and keynum != 3 and keyboard.is_pressed("shift+alt"):
        will_switch_lang[0] = False

    update_light()

def on_shiftalt_release():
    if will_switch_lang[0]:
        chroma.switchlang()
    else:
        will_switch_lang[0] = True

def on_press_action(c):
    if c.scan_code >= 2 and c.scan_code <= 13 or c.scan_code == 41:
        if not keys[0] and keys[1] and not keys[2] and not keys[3]:
            keyboard.call_later(chroma.update_workspaces, (), delay=0.05)
        return
    if c.name not in keymap:
        return
    keynum = keymap[c.name]
    if keynum != 2 and keynum != 3 and keyboard.is_pressed("shift+alt"):
        will_switch_lang[0] = False

    if keys[keynum]:
        return
    keys[keynum] = True


    update_light()

main()

