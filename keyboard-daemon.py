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
import pipes


if not os.path.exists("/etc/rasiel/keyboardrasiel"):
    os.mkfifo("/etc/rasiel/keyboardrasiel")  
will_switch_lang = [True, False]
keymap = {'ctrl': 0, 'windows': 1, 'shift': 2, 'alt': 3}
keys = [False, False, False, False]

try:
    pipe = [os.open("/etc/rasiel/keyboardrasiel", os.O_WRONLY)]
except Exception as e: 
    print(e)
    quit()


def light_ctrlshiftsuper(): 
    os.write(pipe[0], bytes([0]))             
def light_ctrlsuper():      
    os.write(pipe[0], bytes([1]))        
def light_ctrlaltshift():   
    os.write(pipe[0], bytes([2]))           
def light_ctrlshift():      
    os.write(pipe[0], bytes([3]))        
def light_ctrlalt():        
    os.write(pipe[0], bytes([4]))       
def light_ctrl():           
    os.write(pipe[0], bytes([5]))    
def light_shiftsuper():     
    os.write(pipe[0], bytes([6]))          
def light_altsuper():       
    os.write(pipe[0], bytes([7]))        
def light_super():          
    os.write(pipe[0], bytes([8]))     
def light_altshift():       
    os.write(pipe[0], bytes([9]))        
def light_shift():          
    os.write(pipe[0], bytes([10]))     
def light_alt():            
    os.write(pipe[0], bytes([11]))  
def light_default():        
    os.write(pipe[0], bytes([12]))       
def switchlang():
    os.write(pipe[0], bytes([15]))    
def update_workspaces():    
    os.write(pipe[0], bytes([14]))           


def update_light():
    if keys[0]:
        if keys[1]:
            if keys[2]:
                if not keys[3]:
                    light_ctrlshiftsuper()
            else:
                if not keys[3]:
                    light_ctrlsuper()
        else:
            if keys[2]:
                if keys[3]:
                    light_ctrlaltshift()
                else:
                    light_ctrlshift()
            else:
                if keys[3]:
                    light_ctrlalt()
                else:
                    light_ctrl()
    else:
        if keys[1]:
            if keys[2]:
                light_shiftsuper()
            else:
                if keys[3]:
                    light_altsuper()
                else:
                    light_super()
        else:
            if keys[2]:
                if keys[3]:
                    will_switch_lang[1] = True
                    light_altshift()
                else:
                    light_shift()
            else:
                if keys[3]:
                    light_alt()
                else:
                    light_default()
        
def on_release_action(c):
    if c.name not in keymap:
        return
    keynum = keymap[c.name]
    keys[keynum] = False
    
    if keynum != 2 and keynum != 3 and keyboard.is_pressed("shift+alt"):
        will_switch_lang[0] = False
    update_light()

def on_shiftalt_release():
    if will_switch_lang[0] and will_switch_lang[1]:
        switchlang()
    else:
        will_switch_lang[0] = True
        will_switch_lang[1] = False

def on_press_action(c):
    if c.scan_code >= 2 and c.scan_code <= 13 or c.scan_code == 41 or c.scan_code == 15:
        if not keys[0] and keys[1] and not keys[3] or not keys[0] and not keys[1] and keys[3]:
            keyboard.call_later(update_workspaces, (), delay=0.05)

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

keyboard.on_press(on_press_action)
keyboard.on_release(on_release_action)
keyboard.add_hotkey('shift+alt', on_shiftalt_release, trigger_on_release=True)

keyboard.wait()
