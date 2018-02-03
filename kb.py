import keyboard
from subprocess import call

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

def light_up_ctrl():
    print("ctrl")
def light_up_windows():
    print("windows")

def on_shiftalt_release():
    if lang[0]:
        if lang[1]:
            language = "us"
        else:
            language = "ru"
        lang[1] = not lang[1]
        call(["setxkbmap", language])
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

keyboard.add_hotkey('shift+alt', on_shiftalt_release, trigger_on_release=True)
keyboard.on_press(block_switcher)
keyboard.add_hotkey('windows', light_up_default, args=["windows"], trigger_on_release=True)
keyboard.add_hotkey('ctrl', light_up_default, args=["ctrl"], trigger_on_release=True)

keyboard.wait()
