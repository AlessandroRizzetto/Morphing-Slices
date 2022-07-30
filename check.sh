if [[ $1 = "ring" ]]
then
	echo -e "\t\t\t\t\t===== RING ======"
	echo -e "\n\n\t\t===== S1 =====\n"
	sudo ovs-ofctl dump-flows s1
	echo -e "\n\n\t\t===== S2 =====\n"
	sudo ovs-ofctl dump-flows s2
	echo -e "\n\n\t\t===== S3 =====\n"
	sudo ovs-ofctl dump-flows s3
	echo -e "\n\n\t\t===== S4 =====\n"
	sudo ovs-ofctl dump-flows s4
	echo -e "\n\n\t\t===== S5 =====\n"
	sudo ovs-ofctl dump-flows s5
else
	echo -e "bash check.sh [topology]"
	echo -e "[ring,star,tree,linear]"
fi

