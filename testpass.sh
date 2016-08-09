#!/bin/bash

USAGE="testpass.sh decrypt_file list_of_pwd"

decrypt_file=${1}
if [[ ! "${decrypt_file}" ]]; then
    echo ${USAGE}
    exit
fi

pass_file=${2}
if [[ ! "${pass_file}" ]]; then
    echo ${USAGE}
    exit
fi

num_pass=`wc -l ${pass_file}`
rm -f outfile.txt

counter=0
for p in `cat ${pass_file}`; do
    counter=$((counter + 1))
    echo "${p} ${counter}/${num_pass}"
    success=`echo ${p} | gpg --passphrase-fd 0  -d ${decrypt_file} 2> >(grep "decryption failed") | wc -l`
    if [[ ${success} -ne 1 ]]; then
        echo "${counter}, PASSWORD IS: ${p}" >> outfile.txt
        break
    fi
done
 
    
