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

project description:)

# Mininet
We based our project on a "star like" topology wich gave us the flexibility needed to build multiple slices with different topologies on top of it.
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
Each slice has its own ryu-controller, so it is necessary to run the one corrisponding to the desired virtual topology.


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
Now the virtual slice has been created on top of the physical topology.

### PoC
Using the "pingall" command, it is possible to verify the structure of the newly created virtual topology. This command allows you to follow the path of the packets and see that it indeed isn't the one of the base physical topology but the one determined by the running controller.
Another way to explore the newly created topology is to use the script "check.sh" which simply dumps the flow for each switch.

##### FullOpen:
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

##### Tree:
In order to create a slice with a tree topology it is necessary to cut every connection involving S2 or S3.
The resulting topology is an horizontal tree, oriented from left to right with root S1.
If we want, we can add more deviceS (switches and hosts) to our topology and they will all act accordingly with our controller, answering if they're not connected outside of the (single) path running trough the switches number 9: S1-S9-S10-SN

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
*only affected switches are reported, the others are rightly empty
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
##### Star:
explanation of the cutted branches and why it should result like this

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
*only affected switches are reported, the others are rightly empty
```
===== S1 =====

[...] dl_dst=00:00:00:00:00:01 actions=output:"s1-eth1"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s1-eth4"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s1-eth4"
[...] dl_dst=00:00:00:00:00:06 actions=output:"s1-eth4"

 ===== S9 =====
[...]  dl_dst=00:00:00:00:00:01 actions=output:"s9-eth1"
[...] dl_dst=00:00:00:00:00:04 actions=output:"s9-eth4"
[...] dl_dst=00:00:00:00:00:05 actions=output:"s9-eth4"
[...]  dl_dst=00:00:00:00:00:06 actions=output:"s9-eth4"
[...]  dl_dst=ff:ff:ff:ff:ff:ff actions=output:"s9-eth1"
 
 ===== S10 =====
 
 dl_dst=00:00:00:00:00:01 actions=output:"s10-eth2"
 dl_dst=00:00:00:00:00:04 actions=output:"s10-eth1"
 dl_dst=00:00:00:00:00:05 actions=output:"s10-eth1"
 dl_dst=00:00:00:00:00:06 actions=output:"s10-eth1"
 
 ===== S8 =====
 
 dl_dst=00:00:00:00:00:01 actions=output:"s8-eth4"
 dl_dst=00:00:00:00:00:04 actions=output:"s8-eth1"
 dl_dst=00:00:00:00:00:01 actions=output:"s8-eth4"
 dl_dst=00:00:00:00:00:05 actions=output:"s8-eth2"
 dl_dst=00:00:00:00:00:05 actions=output:"s8-eth2"
 dl_dst=00:00:00:00:00:01 actions=output:"s8-eth4"
 dl_dst=00:00:00:00:00:06 actions=output:"s8-eth3"
 dl_dst=00:00:00:00:00:04 actions=output:"s8-eth1"
 dl_dst=00:00:00:00:00:05 actions=output:"s8-eth2"
 dl_dst=00:00:00:00:00:04 actions=output:"s8-eth1"
 dl_dst=00:00:00:00:00:06 actions=output:"s8-eth3"
 dl_dst=00:00:00:00:00:05 actions=output:"s8-eth2"
 dl_dst=00:00:00:00:00:06 actions=output:"s8-eth3"

 ===== S4 =====
 
 dl_dst=00:00:00:00:00:01 actions=output:"s4-eth3"
 dl_dst=00:00:00:00:00:04 actions=output:"s4-eth1"
 dl_dst=00:00:00:00:00:05 actions=output:"s4-eth3"
 dl_dst=00:00:00:00:00:06 actions=output:"s4-eth3"
 
 ===== S5 =====
 
 dl_dst=00:00:00:00:00:01 actions=output:"s5-eth3"
 dl_dst=00:00:00:00:00:05 actions=output:"s5-eth1"
 dl_dst=00:00:00:00:00:04 actions=output:"s5-eth3"
 dl_dst=00:00:00:00:00:06 actions=output:"s5-eth3"

 ===== S6 =====
 dl_dst=00:00:00:00:00:01 actions=output:"s6-eth3"
 dl_dst=00:00:00:00:00:06 actions=output:"s6-eth1"
 dl_dst=00:00:00:00:00:04 actions=output:"s6-eth3"
 dl_dst=00:00:00:00:00:05 actions=output:"s6-eth3"

```
##### Linear:
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
*only affected switches are reported, the others are rightly empty
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

##### Ring:
This is an oriented topology so every packet can only travel in one direction.
If the H1 wants to ping H3 it cannot simply go S1->S3, it must follow the full path S1->S2->S4->S5->S3 (as proven in the dump-flow output where only one dst is on a different port which is the HOST connected to that switch).

![image info](https://raw.githubusercontent.com/elrich2610/Morphing-Slices/794837be2352d91d2fe320bb3c286427ff3cf161/ring.svg
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
Dump-flow (only affected switches are reported, the others are empty as they should).
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
