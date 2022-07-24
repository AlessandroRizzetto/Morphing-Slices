#/usr/bin/bash
topo=(linear star fullOpen ring tree);
if [ -z "$1" ]
then
	echo ""
	echo "No topology supplied. Moving on with default <fullOpen>"
	val="fullOpen"
else
	if [[ " "${topo[@]}" " == *" "$1" "* ]]
	then
		val=$1
	else
		echo ""
		echo "Invalid topology."
		echo "['fullOpen', 'star', 'ring', 'tree', 'linear']"
		echo ""
		exit 1
	fi
fi
echo ""
echo "Starting the controller with a <${val}> topology."
echo ""
sudo fuser -k 6653/tcp
ryu-manager ./topology/${val}.py
