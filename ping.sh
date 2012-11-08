 count=ping -c1 172.19.1.35| grep 'received' | awk -F',' '{ print $2 }' | awk '{ print $1 }'

  if [ $count -eq 0 ]; then
    # 100% failed
    echo "Host : $myHost is down (ping failed) at $(date)" | mail -s "$SUBJECT" $EMAILID
  fi
done

count=$1                                   # Initialise count to first parameter
while [ $count -gt 0 ]                     # while count is greater than 10 do
do
   echo $count seconds till supper time!
   count=$(expr $count -1)                 # decrement count by 1
   sleep 3                                 # sleep for a second using the Unix sleep command
   ping -c1 172.19.1.35

done
##################################################


counter=0
while [ 1 ]                                                     #infinite loop
do

sleep 10                                                    	#pings for every 10 seconds.
count=$(ping -c1 172.19.1.35| grep 'received' | awk -F',' '{ print $2 }' | awk '{ print $1 }')
#echo $count
if [ "$count" -eq 0 ]											#if it receives 0 number of packets
then
counter=`expr $counter + 1`
else
counter=0
fi
#echo $counter
if [ "$counter" -eq 3 ]                                         #if 3 consequence errors report as alert
then
echo "$(date +%F" "%X):alert"
counter=0
fi

done
