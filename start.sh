#/usr/bin/bash
if [ -z "$1" ]
then
	echo "./start [topology name (star)]"
	val="star"
else
	val=$1
fi
sudo fuser -k 6653/tcp
ryu-manager ./topology/${val}.py
