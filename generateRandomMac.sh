#!/bin/bash

ethmac=$(echo `date`|md5sum|sed 's/^\(..\)\(..\)\(..\)\(..\)\(..\).*$/02:\1:\2:\3:\4:\5/')
wifimac=$(echo `uname -a` `date`|md5sum|sed 's/^\(..\)\(..\)\(..\)\(..\)\(..\).*$/02:\1:\2:\3:\4:\5/')

ifconfig en0 ether ${ethmac}
ifconfig en1 ether ${wifimac}
