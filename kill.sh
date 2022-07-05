#/usr/bin/bash
sudo fuser -k 6653/tcp
ryu-manager star.py
