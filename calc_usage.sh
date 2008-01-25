#!/bin/bash
# calc_usage.sh

# Calculates the total disk space taken up by all directories within the 
# calling directory.  Output is written to file specified on command line.

out_file=$1
rm ${out_file} -f

for d in `ls .`; do
    echo $d >> ${out_file}
    du -ch $d | grep total >> ${out_file}
done
