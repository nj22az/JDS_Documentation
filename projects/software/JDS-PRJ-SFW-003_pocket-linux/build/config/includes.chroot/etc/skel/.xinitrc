#!/bin/sh
# Pocket Linux default X session — JDS-PRJ-SFW-003
# No display manager: log in on the console and run `startx`.
xrdb -merge "$HOME/.Xresources"
exec icewm-session
