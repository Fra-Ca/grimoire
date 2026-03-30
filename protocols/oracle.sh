#!/bin/bash

hyprctl dispatch workspace 2
#sleep 0.5
setsid /usr/bin/kitty &
setsid /usr/bin/firefox &
