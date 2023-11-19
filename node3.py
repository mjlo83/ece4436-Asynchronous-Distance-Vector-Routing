# node3.py

import sys
sys.path.append("..")  # Adjusts the path to find utils if it's in the parent directory
from utils import tolayer2, Rtpkt, clocktime

# Distance Table for node 3
distance_table = [[999 for _ in range(4)] for _ in range(4)]
neighbors = [0, 2]  # Node 3's neighbors

# Initialization function for node 3
def rtinit3():
    global distance_table
    distance_table[0][3] = 7    # Direct cost to node 0
    distance_table[1][3] = 999  # Node 3 is not connected to node 1
    distance_table[2][3] = 2    # Direct cost to node 2
    distance_table[3][3] = 0    # Cost to self is zero
    print(f"rtinit3 called at time {clocktime}. Distance table: {distance_table}")
    send_to_neighbors()

# Send distance vector to all neighbors
def send_to_neighbors():
    for neighbor in neighbors:
        pkt = Rtpkt(3, neighbor, [distance_table[i][3] for i in range(4)])
        tolayer2(pkt)

# Update function for node 3
def rtupdate3(pkt):
    print(f"rtupdate3 called at time {clocktime}. Received packet: {pkt}")
    global distance_table
    updated = False
    src = pkt.sourceid
    # Update the distance table with the received mincost if it's less than current cost
    for i in range(4):
        if pkt.mincost[i] + distance_table[src][3] < distance_table[i][3]:
            distance_table[i][3] = pkt.mincost[i] + distance_table[src][3]
            updated = True
    
    # If the distance table was updated, send the new distance vector to all neighbors
    if updated:
        print(f"Node 3's distance table updated: {distance_table}")
        send_to_neighbors()

# Link change handler for node 3
def linkhandler3(linkid, newcost):
    # Optional: Implement if handling dynamic link cost changes is required
    pass
