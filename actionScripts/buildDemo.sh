#!/bin/bash

counter=1
student_id=1
vendor_id=11
faculty_id=21
admin_id=31
# Loop to make 10 of each Participant Type
while [ $counter -le 10 ]
do
    #echo $counter
    python3 make/makeStudent.py -i $student_id -f Student -l $counter -b 100 -m CSB -a FALSE
    ((student_id++))
    python3 make/makeVendor.py -i $vendor_id -n Vendor$counter -c WEEKLY -b 1000
    ((vendor_id++))
    python3 make/makeFaculty.py -i $faculty_id -f Faculty -l $counter -b 100 -d DEPT
    ((faculty_id++))
    python3 make/makeAdmin.py -i $admin_id -f Administrator -l $counter -b 100
    ((admin_id++))

    ((counter++))
done

#python3 makeStudent.py -i 1234567 -f Test -l Student -b 100 -m CSB -a FALSE
#transferFunds.py -a <amount> -f <fromType> -F <fromID> -t <toType> -T <toID>

loop=1
while [ $loop -le 10 ]
do
    student_id=$((1 + RANDOM % 10))
    vendor_id=$(( (11 + RANDOM % 10) ))
    faculty_id=$(( (21 + RANDOM % 10) ))
    admin_id=$(( (31 + RANDOM % 10) ))

    echo Transfering Funds from Student $student_id to Vendor $vendor_id
    python3 transactions/transferFunds.py -a 10 -f Student -F $student_id -t Vendor -T $vendor_id

    vendor_id=$(( (11 + RANDOM % 10) ))
    echo Transfering Funds from Faculty $faculty_id to Vendor $vendor_id
    python3 transactions/transferFunds.py -a 10 -f Faculty -F $faculty_id -t Vendor -T $vendor_id

    vendor_id=$(( (11 + RANDOM % 10) ))
    echo Transfering Funds from Admin $admin_id to Vendor $vendor_id
    python3 transactions/transferFunds.py -a 10 -f Administrator -F $admin_id -t Vendor -T $vendor_id

    ((loop++))
done

echo Demo Setup Complete.