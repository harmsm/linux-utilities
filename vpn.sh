#!/bin/bash

if [[ ! "${1}" ]]; then
    echo "specify \"start\" or \"stop\""
    exit
fi

if [[ "${1}" == "start" ]]; then
    sudo vpnc-connect /etc/vpnc/uovpn.conf
elif [[ "${1}" == "stop" ]]; then
    sudo vpnc-disconnect
else
    echo "${1} not recognized."
fi

