#!/bin/bash

if [[ ! "${1}" ]]; then
    echo "specify \"start\" or \"stop\""
    exit
fi

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [[ "${1}" == "start" ]]; then
    sudo vpnc-connect /etc/vpnc/uovpn.conf
    $DIR/checkIP.sh

elif [[ "${1}" == "stop" ]]; then
    sudo vpnc-disconnect
    $DIR/checkIP.sh
else
    echo "${1} not recognized."
fi

