<p align="center">
  <h2 align="center">Morphing Network Slicing with RYU</h2>

  <p align="center">
  Andreatta - Mereuta - Rizzetto
  </p>
</p>
<br>

---

## Table of contents
- [The project](#Intro)
- [Base topology](#Mininet)
- [How To](#Usage)
    - [Proof of Concept](#PoC)
        - [FullOpen topology](#FullOpen)
        - [Tree topology](#Tree)
        - [Star topology](#Star)
        - [Linear topology](#Linear)
        - [Ring topology](#Ring)
- [Group members](#Group-Members)

# Intro
The starting point of this project is a single domain base topology where we have full control of the network. The aim is to generate different slices as overlays of the original topology. This means that the actual base network remains unaltered but the perceived topology is different from the original one. It is important to understand that this is a virtualization process, new links can't be generated in the process of creating a new virtual slice.
This technique can be useful when a service provider wants to have different topologies on the same physical one.

# Mininet
We based our project on a partial mesh topology which gave us the flexibility needed to build multiple slices with different topologies on top of it.
The topologies that we have decided to implement are:
- Tree topology
- Linear topology
- Star topology
- Ring topology

Specific base topology built with MININET: 
![image info](https://raw.githubusercontent.com/elrich2610/Morphing-Slices/794837be2352d91d2fe320bb3c286427ff3cf161/base.svg
)

Table that maps each connection on the right port for every switch of the base topology:
|HOST|Port 1|Port 2|Port 3|Port 4|
|:--|:--:|:--:|:--:|:--:|
**S1**|  H1  | S2  | S3	    |S9
**S2**|  H2	 | S1	 | 	S4  |S9
**S3**|  H3	 | S1	 | S5 |S9	
**S4**|  H4	 | S2	 | S8  |-
**S5**|  H5	 | S3	 | 	S8  |-
**S6**|  H6	 | S7	 | 	S8    |-
**S7**|  H7	 | H8	 | S6 | -
**S8**|  S4 | 	S5 | 	 S6   | S10
**S9**| S1 	 | 	S2 | 	S3    | S10
**S10**|  S8 | S9 | - |  -


# Usage

```bash
git clone https://github.com/elrich2610/Morphing-Slices.git
cd Morphing-Slices
```
From now on  **2** separate terminals are needed.
The first terminal is used to run the ryu-controller.
Each slice has its own ryu-controller, so it is necessary to run the one corresponding to the desired virtual topology.


```bash
#Terminal 1
#virtual topologies: [fullOpen - tree - star - ring - linear]
./start.sh [virtual topology name]
```

On the  second terminal, run the physical base topology created with mininet; once started it'll automatically connect to the mininet console
```
#Terminal 2
sudo python3 baseTopology.py
```
Now the chosen virtual slice has been created on top of the physical topology.

### PoC
Using the "pingall" command, it is possible to verify the structure of the newly created virtual topology. This command allows you to follow the path of the packets and see that it indeed isn't the one of the base physical topology but the one determined by the running controller.
Another way to explore the newly created topology is to use the script "check.sh" which simply dumps the flow for each switch.

### FullOpen:
The expected result for the base topology with all the switches in OFPP_FLOOD mode is the following:
```txt
#everything reach everything
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 h4 h5 h6 h7 h8
h2 -> h1 h3 h4 h5 h6 h7 h8
h3 -> h1 h2 h4 h5 h6 h7 h8
h4 -> h1 h2 h3 h5 h6 h7 h8
h5 -> h1 h2 h3 h4 h6 h7 h8
h6 -> h1 h2 h3 h4 h5 h7 h8
h7 -> h1 h2 h3 h4 h5 h6 h8
h8 -> h1 h2 h3 h4 h5 h6 h7
*** Results: 0% dropped (56/56 received)
```

### Tree:
In order to create a slice with a tree topology it is necessary to cut every connection involving S2 or S3.
The resulting topology is an horizontal tree, oriented from left to right with root S1.
Even if we wanted to add more devices to the the base topology on the S1-S9-S10 path, the implemented tree-controller is still going to correctly generate a tree topology and the new links would all act accordingly.

![image info](https://raw.githubusercontent.com/elrich2610/Morphing-Slices/794837be2352d91d2fe320bb3c286427ff3cf161/tree.svg
)

```txt
mininet> pingall
*** Ping: testing ping reachability
h1 -> X X h4 h5 h6 h7 h8
h2 -> X X X X X X X
h3 -> X X X X X X X
h4 -> h1 X X h5 h6 h7 h8
h5 -> h1 X X h4 h6 h7 h8
h6 -> h1 X X h4 h5 h7 h8
h7 -> h1 X X h4 h5 h6 h8
h8 -> h1 X X h4 h5 h6 h7
*** Results: 46% dropped (30/56 received)
```

Dump-flow  
\*only affected switches are reported, the others are rightly empty
```
===== S1 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s1-eth1"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s1-eth4"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s1-eth4"
[...] dl_dst=00:00:00:00:00:06 actions=output:"s1-eth4"
[...] dl_dst=00:00:00:00:00:07 actions=output:"s1-eth4"
[...] dl_dst=00:00:00:00:00:08 actions=output:"s1-eth4"

 ===== S8 =====

[...] dl_dst=00:00:00:00:00:04 actions=output:"s8-eth1"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s8-eth2"
[...] dl_dst=00:00:00:00:00:06 actions=output:"s8-eth3"
[...] dl_dst=00:00:00:00:00:07 actions=output:"s8-eth3"
[...] dl_dst=00:00:00:00:00:08 actions=output:"s8-eth3"

 ===== S9 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s9-eth1"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s9-eth4"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s9-eth4"
[...] dl_dst=00:00:00:00:00:06 actions=output:"s9-eth4"
[...] dl_dst=00:00:00:00:00:07 actions=output:"s9-eth4"
[...] dl_dst=00:00:00:00:00:08 actions=output:"s9-eth4"

 ===== S10 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s10-eth2"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s10-eth1"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s10-eth1"
[...] dl_dst=00:00:00:00:00:06 actions=output:"s10-eth1"
[...] dl_dst=00:00:00:00:00:07 actions=output:"s10-eth1"
[...] dl_dst=00:00:00:00:00:08 actions=output:"s10-eth1"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s10-eth1"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s10-eth1"
[...] dl_dst=00:00:00:00:00:06 actions=output:"s10-eth1"
[...] dl_dst=00:00:00:00:00:07 actions=output:"s10-eth1"
[...] dl_dst=00:00:00:00:00:08 actions=output:"s10-eth1"

```
### Star:
In order to create a slice with a star topology, only the paths that connects the center to the edge switches S1, S4, S5 and S6 are preserved, any other connection is cut. The logic behind this slice is that any packet coming from a port that isn't part of the path that connects the device to the center is sent to the central switch of the virtual star topology otherwise the flooding algorithm is applied.
The resulting topology is a star where the packets must always go through the center to arrive at their destination.

![image info](https://raw.githubusercontent.com/elrich2610/Morphing-Slices/794837be2352d91d2fe320bb3c286427ff3cf161/star.svg)

```txt
mininet> pingall
*** Ping: testing ping reachability
h1 -> X X h4 h5 h6 X X
h2 -> X X X X X X X
h3 -> X X X X X X X
h4 -> h1 X X h5 h6 X X
h5 -> h1 X X h4 h6 X X
h6 -> h1 X X h4 h5 X X
h7 -> X X X X X X X
h8 -> X X X X X X X
*** Results: 78% dropped (12/56 received)
```
Dump-flow 
\*only some representative switches are reported

```

===== S1 =====

[...] dl_dst=00:00:00:00:00:04 actions=output:"s1-eth4"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s1-eth4"
[...] dl_dst=00:00:00:00:00:06 actions=output:"s1-eth4"

===== S2 =====


===== S9 =====
[...] dl_dst=00:00:00:00:00:04 actions=output:"s9-eth4"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s9-eth4"
[...] dl_dst=00:00:00:00:00:06 actions=output:"s9-eth4"


```


### Linear:
In order to create a slice with a linear topology only the path that connects S1, S2, and S3 is preserved, any other connection is cut.
The resulting topology connects H1, H2 and H4 through the S1-S2-S4 channel.

![image info](https://raw.githubusercontent.com/elrich2610/Morphing-Slices/794837be2352d91d2fe320bb3c286427ff3cf161/linear.svg
)
```txt
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 X h4 X X X X
h2 -> h1 X h4 X X X X
h3 -> X X X X X X X
h4 -> h1 h2 X X X X X
h5 -> X X X X X X X
h6 -> X X X X X X X
h7 -> X X X X X X X
h8 -> X X X X X X X
*** Results: 89% dropped (6/56 received)
```
Dump-flow  
\*only affected switches are reported, the others are rightly empty
```
===== S1 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s1-eth1"
[...] dl_dst=00:00:00:00:00:02 actions=output:"s1-eth2"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s1-eth2"

===== S2 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s2-eth2"
[...] dl_dst=00:00:00:00:00:02 actions=output:"s2-eth1"
[...] dl_dst=00:00:00:00:00:01 actions=output:"s2-eth2"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s2-eth3"
[...] dl_dst=00:00:00:00:00:02 actions=output:"s2-eth1"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s2-eth3"

===== S4 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s4-eth2"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s4-eth1"
[...] dl_dst=00:00:00:00:00:02 actions=output:"s4-eth2"

```

### Ring:
In order to create a slice with a ring topology all the connections involving S6, S7, S9 or S10 are cut and the output ports of each remaining switch are mapped based on the input port of the arriving packets.
The resulting topology is an oriented ring where the packets travel in one direction only; this means that if for example H1 wants to ping H3,the packets can't simply  follow the S1->S3 path, they must follow the ring topology and take the S1->S2->S4->S5->S3 path.

![image info](https://raw.githubusercontent.com/elrich2610/Morphing-Slices/48494969afcd059c64dc7cf197c247a6adb67b66/images/oriented%20ring.svg
)

```txt
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 h3 h4 h5 X X X
h2 -> h1 h3 h4 h5 X X X
h3 -> h1 h2 h4 h5 X X X
h4 -> h1 h2 h3 h5 X X X
h5 -> h1 h2 h3 h4 X X X
h6 -> X X X X X X X
h7 -> X X X X X X X
h8 -> X X X X X X X
```
Dump-flow 
\*only affected switches are reported, the others are rightly empty
```
 ===== S1 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s1-eth1"
[...] dl_dst=00:00:00:00:00:02 actions=output:"s1-eth2"
[...] dl_dst=00:00:00:00:00:03 actions=output:"s1-eth2"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s1-eth2"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s1-eth2"

===== S2 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s2-eth3"
[...] dl_dst=00:00:00:00:00:02 actions=output:"s2-eth1"
[...] dl_dst=00:00:00:00:00:03 actions=output:"s2-eth3"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s2-eth3"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s2-eth3"

===== S3 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s3-eth2"
[...] dl_dst=00:00:00:00:00:03 actions=output:"s3-eth1"
[...] dl_dst=00:00:00:00:00:02 actions=output:"s3-eth2"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s3-eth2"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s3-eth2"

===== S4 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s4-eth3"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s4-eth1"
[...] dl_dst=00:00:00:00:00:02 actions=output:"s4-eth3"
[...] dl_dst=00:00:00:00:00:03 actions=output:"s4-eth3"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s4-eth3"

 ===== S5 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s5-eth2"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s5-eth1"
[...] dl_dst=00:00:00:00:00:02 actions=output:"s5-eth2"
[...] dl_dst=00:00:00:00:00:03 actions=output:"s5-eth2"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s5-eth2"

```


### Group-Members
[Andreatta Thomas - 213912](https://github.com/ThomasAndreatta)

[Mereuta Mihaela - 209035](https://github.com/plsmiha)

[Rizzetto Alessandro - 209783](https://github.com/elrich2610)
