# Morphing-Slices - Andreatta Mereuta Rizzetto
RYU SDN controller

# PORTS SCHEMA
```txt
       P1	  P2	 P3	      P4
    ________________________________
S1	|  H1	 | S3	 | 	    |
S2	|  H2	 | S3	 | 	    |
S3	|  S1	 | S2	 | S4   | 	
S4	|  H4	 | S3	 | 	    |
S5	|  S3	 | S7	 | 	    |
S6	|  H6	 | S7	 | 	    |
S7	|  S5	 | S6	 | S8   | S9
S8	|  H8	 | S7	 | 	    |
S9	|  H9	 | S7	 | 	    |
S10	|  H10 | H11 | S9   |  
```


### MEMO
> terminal 1

./start.sh prof

> terminal 2

sudo python3 basetopology.py
