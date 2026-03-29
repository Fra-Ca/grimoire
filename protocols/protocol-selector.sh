#!/bin/bash

trap 'tput cnorm' EXIT
tput civis

protocols=("ARMAGEDDON" "ORACLE" "GRIMOIRE" "SANCTUM")
selected=0

draw_menu() {
  clear
  echo ""
  echo " DEUS // BOOT INTERFACE"
  echo ""
  for i in "${!protocols[@]}"; do
    if [ "$i" -eq "$selected" ]; then
      echo " > ${protocols[$i]}"
    else
      echo "   ${protocols[$i]}"
    fi
  done
}

draw_menu

while true; do
  read -s -n3 key
  case "$key" in
  $'\e[A')
    [ "$selected" -gt 0 ] && ((selected--))
    ;;
  $'\e[B')
    [ "$selected" -lt $((${#protocols[@]} - 1)) ] && ((selected++))
    ;;
  $'\n' | '')
    break
    ;;
  esac
  draw_menu
done

case "$selected" in
0) bash ~/athanor/grimoire/protocols/armageddon.sh ;;
1) bash ~/athanor/grimoire/protocols/oracle.sh ;;
2) bash ~/athanor/grimoire/protocols/grimoire.sh ;;
3) bash ~/athanor/grimoire/protocols/sanctum.sh ;;
esac
