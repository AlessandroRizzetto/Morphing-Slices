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
We have based our project on a "star like" topology wich gave us the flexibility needed for building on top of that multiple topologies.
The ones that we've decided to implement are:
- Tree topology
- Linear topology
- Star topology
- Ring topology

The following schema rappresent our base topology built with MININET and the virtual topologies made with RYU-Manager, the red lines are used to easily identify the differences between the base and the current topology. 
![image info](https://raw.githubusercontent.com/elrich2610/Morphing-Slices/a3d48e770b402eb33f813cfb6ddaa3ae23aef37a/topologie.svg
)

Below a table rappresenting the ports/device connection of every switch
|HOST|Port 1|Port 2|Port 3|Port 4|
|:--|:--:|:--:|:--:|:--:|
**S1**|  H1  | S2  | S3	    |S4
**S2**|  H2	 | S1	 | 	S4  |S9
**S3**|  H3	 | S1	 | S5 |S9	
**S4**|  H4	 | S2	 | 	  -  |-
**S5**|  H5	 | S3	 | 	  -  |-
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
From now on we'll have to work with **2** separate terminals:

On your first terminal start the controller which will decide how our virtualTopology will looks like
```bash
#Terminal 1
#virtual topologies: [fullOpen - tree - star - ring - linear]
./start.sh [virtual topology name]
```

On your second terminal run the mininet topology (the physical topology), once started it'll automatically connect to the mininet console
```
#Terminal 2
sudo python3 baseTopology.py
```

### PoC
Using the "pingall" command we'll see how our packets won't follow the base topology but will run trough the path 
choosen from our controller AKA our controller has modified the logical topology.

##### FullOpen:
The expected result for the basetopology with all the switches in OFPP_FLOOD mode is the following:
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
We are cutting everything that is connected to the swtich 2 and 3 for building a treeTopology (Horizontaly oriented).
If we want we can add more device (switches and hosts) to our topology and they will all act accordingly with our controller, answering if they're not connected ouside of the (single) path running trough the switch number 9: S1-S9-S10-SN
Or, in a easier way, if they are not cutted off from the topology by some red line. 
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

##### Star:
explanation of the cutted branches and why it should result like this
```txt
pingall star.py
```

##### Linear:
Based on the Tree topology simply removing the connection between the S6 and the S7 we'll be able to modify our topology from the Tree one to the Linear one.
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

##### Ring:
explanation of the cutted branches and why it should result like this
```txt
pingall ring.py
```



### Group-Members
[Andreatta Thomas - 213912](https://github.com/ThomasAndreatta)

[Mereuta Mihaela - 209035](https://github.com/plsmiha)

[Rizzetto Alessandro - 209783](https://github.com/elrich2610)
>>>>>>> main
