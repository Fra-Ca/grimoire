#!/bin/bash

hyprctl dispatch workspace 2
#sleep 0.5
/usr/bin/kitty &
disown
/usr/bin/firefox &
disown
