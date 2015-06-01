#!/bin/bash

# Figure out our current IP address and our apparent location (for making sure
# vpn is working)

TEST_SERVER="google.com"

# Returns 1 if ping is successful, 0 if not
are_we_up=`ping ${TEST_SERVER} -c 1 | grep "1 received" | wc -l`

ip=`curl -s ifconfig.me/ip`
if [[ "${ip}" == "" ]]; then
    ip="unk"
    country="unk"
    state="unk"
    city="unk"
else
    whois ${ip} > whois.tmp
    country=`awk '{ if ($1 == "Country:") { print $2}}' whois.tmp`
    state=`awk '{ if ($1 == "StateProv:") { print $2}}' whois.tmp`
    city=`awk '{ if ($1 == "City:") { print $2}}' whois.tmp`
    rm -rf whois.tmp
fi

echo `date -Iseconds` ${are_we_up} ${ip} ${country} ${state} ${city}

