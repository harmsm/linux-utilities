#!/bin/bash

# Use HandBrakeCLI to rip all episodes of a tv show from a dvd, numbering them
# sequentially.  The numbering starts at 1+offset.  Note also that the program
# is set to decomb.

USAGE="ripper.sh dvd_path offset (track numbering starts at 1+offset)"

DVD=${1}
OFFSET=${2}

if [[ ! "$DVD" ]] || [[ ! "$OFFSET" ]]; then
    echo $USAGE
    exit
fi

echo "Finding number of tracks"
HandBrakeCLI -i ${DVD} -t 0 --min-duration 100 &> junk.tmp

counter=$OFFSET
for track in `grep "+ title " junk.tmp | awk '{print $3}' | sed 's/://'`; do
    echo "Ripping track $track"

    counter=`expr 1 + ${counter}`
    HandBrakeCLI -i ${DVD} --preset="Normal" -t ${track} -o msb_${counter}.mp4 --decomb &> track_${track}.log

done

rm -f junk.tmp
