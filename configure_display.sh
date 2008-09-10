#!/bin/bash
#configure_display.sh

# Configures displays to my specifications using aticonfig

# Make sure the user is root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root!"
    exit
fi

# Parse command line.  If no mode is specified, use "help" mode
mode=${1}
if ! [ "${mode}" ]; then
    mode="help"
fi

# Depending on specified mode, do different things
case "${mode}" in
    "help")
        echo "A script for automatically configuring display modes using the"
        echo "aticonfig utility."
        echo ""; echo '    Usage: $> configure_display MODE'
        echo ""; echo "Allowed MODE values are:"
        echo "    single: only use the laptop monitor"
        echo "    clone x y: clone the display on an external monitor"
        echo "               using the given x/y resolution"
        echo "    big: span display across laptop and external monitor"
        echo "    clean: removes xorg.conf.fglrx-* backup files."
        echo "    help: displays this help message and exits"
        exit
        ;;
    "single")
        echo "Configuring X for a single display"
        aticonfig --desktop-setup=single --sync-vsync=on \
                  --resolution=0,1400x1050
        ;;
    "clone")
        if ! ( [ $2 ] && [ $3 ] ); then
            echo "\"clone\" option requires x and y resolution!"
            echo "example: clone 1024 768"
            exit
        fi

        x=$2
        y=$3
        echo "Configuring X for a ${x}x${y} cloneed display!"
        aticonfig --desktop-setup=clone --mode2=${x}x${y} \
                  --sync-vsync=on --resolution=0,${x}x${y}

        ;;
    "big")
        echo "Configuring X for a big desktop display"
        aticonfig --desktop-setup=horizontal,reverse --sync-vsync=on \
                  --resolution=0,1400x1050 --mode2=1280x1024,1024x768
        ;;
    "clean")
        echo "This will remove all flgrx backups of xorg.conf!"
        echo "Are you sure you want to do this! [y|n]"
        read response
        if [ ${response:0:1} == "y" ] || [ ${response:0:1} == "Y" ]; then
            echo "Deleting files!"
            rm /etc/X11/xorg.conf.fglrx-* -f
        fi
        exit
        ;;
    *)
        echo "Option \"${mode}\" not recognized!  Type:"; echo ""
        echo "    $> configure_display.sh help"; echo ""
        echo "for available options!"
        exit
        ;;
esac

