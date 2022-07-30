#!/usr/bin/bash
if [[ $1 = "ring" ]]
then
	echo -e "\t\t\t\t\t===== RING ======"
	for i in {1..10}
	do
		echo -e "\n\n\t\t===== S$i =====\n"
		sudo ovs-ofctl dump-flows s$i
	done
elif [[ $1 = "tree" ]]
then
	echo -e "\t\t\t\t\t===== TREE ======"
	for i in {1..10}
	do
		echo -e "\n\n\t\t===== S$i =====\n"
		sudo ovs-ofctl dump-flows s$i
	done
elif [[ $1 = "linear" ]]
then
	echo -e "\t\t\t\t\t===== LINEAR ======"
	for i in {1..10}
	do
		echo -e "\n\n\t\t===== S$i =====\n"
		sudo ovs-ofctl dump-flows s$i
	done
elif [[ $1 = "star" ]]
then
	echo -e "\t\t\t\t\t===== STAR ======"
	for i in {1..10}
	do
		echo -e "\n\n\t\t===== S$i =====\n"
		sudo ovs-ofctl dump-flows s$i
	done

else
	echo -e "bash check.sh [topology]"
	echo -e "[ring,star,tree,linear]"
fi

