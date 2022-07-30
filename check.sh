#!/usr/bin/bash
for i in {1..10}
do
	echo -e "\n\n\t\t===== S$i =====\n"
	sudo ovs-ofctl dump-flows s$i
done

