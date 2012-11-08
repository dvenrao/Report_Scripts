#!/bin/sh
DIR=/home/sunil

# wget output file
FILE=dailyinfo.`date +"%Y%m%d"`

# wget log file
LOGFILE=wget.log

# wget download url
URL= http://172.19.1.35/s.jpg

cd $DIR
wget $URL -O $FILE -o $LOGFILE


#echo "executing wget"
 wget http://172.19.1.35/s100M -o log -O jpg
a=$(wc -l log|cut -d " " -f1)
#echo "$a"
if [ $a -le 5 ]
then
TIME="ERROR"
else
#echo "executing filters"
TIME="$(tail -n 4 log |grep 100%|cut -d "=" -f 2)"
fi
echo "--timestamp ---$TIME---"
#echo "exit"


#################################################################
#echo "executing wget"
wget http://172.19.1.35/100M -o log -O jpg
a=$(wc -l log|cut -d " " -f1)
#echo "$a"
CONNECTION=$( head -n 2 log |tail -1|cut -d " " -f4)
if [ $CONNECTION == "connected." ]
then
RESPONSE="$(head -n 3 log |tail -1|cut -d " " -f 6-)"
if [ "$RESPONSE" = "200 OK" ]
then
TIME="$(tail -n 4 log |grep 100%|cut -d "=" -f 2)"
else
TIME=$RESPONSE
fi

else
TIME=$CONNECTION
fi


echo "--timestamp ---$TIME---"
#echo "exit"
###################################################################