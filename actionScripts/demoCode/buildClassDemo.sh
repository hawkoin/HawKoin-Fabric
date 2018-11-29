#!/bin/bash

counter=1; 
name=none;
# Loop through input file (studentList.txt)
while read -r LINE || [[ -n $LINE ]]; 
do
    if [ $(($counter % 2)) -eq 1 ];
    then
        string=$LINE
        #echo $string
    fi 
    if [ $(($counter % 2)) -eq 0 ];
    then 
        #echo $LINE
        python3 makeClassStudent.py -i $LINE -f $name -l None -b 100 -m CSB -a FALSE
    fi

    ((counter++))
done

echo Demo Setup Complete.