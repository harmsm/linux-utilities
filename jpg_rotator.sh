#/bin/bash
# jpg_rotator.sh

# Uses jpegtran to rotate losslessly rotate images on command line.

USAGE="jpg_rotator.sh cw|ccw jpg1 jpg2 ... jpgN"

# Take rotation from command line
rotation=${1}
shift

if [ "${rotation}" == "cw" ]; then
    rotation=90
elif [ "${rotation}" == "ccw" ]; then
    rotation=270
else
    echo ${USAGE}
    exit
fi

# Rotate every jpg file listed on command line
for arg in "$@"; do

    jpegtran -rotate 270 -copy all ${arg} > tmp.jpg
    mv tmp.jpg ${arg}

done
