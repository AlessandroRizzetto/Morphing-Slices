# Morphing-Slices - Andreatta Mereuta Rizzetto
RYU SDN controller

# PORTS SCHEMA

|HOST|Port 1|Port 2|Port 3|Port 4|
|--|--|--|--|--|
S1|  H1  | S9  | 	    |
S2|  H2	 | S9	 | 	    |
S3|  H3	 | S9	 |    | 	
S4|  H4	 | S8	 | 	    |
S5|  H5	 | S8	 | 	    |
S6|  H6	 | S7	 | 	S8    |
S7|  H7	 | H8	 | S6 | 
S8|  S4 | 	S5 | 	 S6   | S10
S9| S1 	 | 	S2 | 	S3    | s10
S10|  S8 | S9 |  |  


### MEMO
> terminal 1

./start.sh prof

> terminal 2

sudo python3 basetopology.py
