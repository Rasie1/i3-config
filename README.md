# i3-config
This is i3 config for using with Razer Blade Stealth (Late 2017)

# Features 
It supports shortcut backlighting for each modifier button. 
Also, when you press `super`, among with other shortcuts, workspaces are shown on the keyboard: active, empty, current and urgent have each own color. 

`Alt+Shift` is set up to work properly without intrusion into other apps worksflow. You can now switch languages with Alt and Shift in Sublime Text in i3 without losing other shortcuts with Alt and Shift.

Also, there are shortcuts for yeelight to turn lights off and on in your room.

One of daemons listens to key events using python keyboard https://github.com/boppreh/keyboard

Tested on manjaro with kernel 4.15

# Installation

You should use `systemd` to use keyboard daemons.
You should have `openrazer` installed. 

1. copy everything to `~/.config/i3` dir and `cd` into it
2. `sudo make install` to install daemons
3. `systemctl enable keyboard-rasiel.service` and `systemctl --user enable chroma-rasiel.service` to set daemons to autostart
4. `./reload_services.sh` to run daemons
