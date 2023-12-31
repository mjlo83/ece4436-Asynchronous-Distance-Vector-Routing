# node2.py

import sys
sys.path.append("..")  # Adjusts the path to find utils if it's in the parent directory
from utils import tolayer2, Rtpkt, clocktime

# Distance Table for node 2
distance_table = [[999 for _ in range(4)] for _ in range(4)]
neighbors = [0, 1, 3]  # Node 2's neighbors

# Initialization function for node 2
def rtinit2():
    global distance_table
    distance_table[0][2] = 3    # Direct cost to node 0
    distance_table[1][2] = 1    # Direct cost to node 1
    distance_table[2][2] = 0    # Cost to self is zero
    distance_table[3][2] = 2    # Direct cost to node 3
    print(f"rtinit2 called at time {clocktime}. Distance table: {distance_table}")
    send_to_neighbors()

# Send distance vector to all neighbors
def send_to_neighbors():
    for neighbor in neighbors:
        pkt = Rtpkt(2, neighbor, [distance_table[i][2] for i in range(4)])
        tolayer2(pkt)

# Update function for node 2
def rtupdate2(pkt):
    print(f"rtupdate2 called at time {clocktime}. Received packet: {pkt}")
    global distance_table
    updated = False
    src = pkt.sourceid
    # Update the distance table with the received mincost if it's less than current cost
    for i in range(4):
        if pkt.mincost[i] + distance_table[src][2] < distance_table[i][2]:
            distance_table[i][2] = pkt.mincost[i] + distance_table[src][2]
            updated = True
    
    # If the distance table was updated, send the new distance vector to all neighbors
    if updated:
        print(f"Node 2's distance table updated: {distance_table}")
        send_to_neighbors()

# Link change handler for node 2
def linkhandler2(linkid, newcost):
    # Optional: Implement if handling dynamic link cost changes is required
    pass
