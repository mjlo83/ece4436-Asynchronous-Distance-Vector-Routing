# node0.py

import sys
sys.path.append("..")  # This allows importing from the parent directory
from utils import tolayer2, Rtpkt, clocktime

# Distance Table for node 0
distance_table = [[999 for _ in range(4)] for _ in range(4)]
neighbors = [1, 2, 3] #Node 0's neighbors

# Initialization function for node 0
def rtinit0():
    global distance_table
    distance_table[0][0] = 0    # Cost to self is zero
    distance_table[1][0] = 1    # Direct cost to node 1
    distance_table[2][0] = 3    # Direct cost to node 2
    distance_table[3][0] = 7    # Direct cost to node 3
    print(f"rtinit0 called at time {clocktime}. Distance table: {distance_table}")
    send_to_neighbors()

# Send distance vector to all neighbors
def send_to_neighbors():
    for neighbor in neighbors:
        pkt = Rtpkt(0, neighbor, [distance_table[i][0] for i in range(4)])
        tolayer2(pkt)

# Update function for node 0
def rtupdate0(pkt):
    print(f"rtupdate0 called at time {clocktime}. Received packet: {pkt}")
    global distance_table
    updated = False
    src = pkt.sourceid
    # Update the distance table with the received mincost if it's less than current cost
    for i in range(4):
        if pkt.mincost[i] + distance_table[src][0] < distance_table[i][0]:
            distance_table[i][0] = pkt.mincost[i] + distance_table[src][0]
            updated = True
    
    # If the distance table was updated, send the new distance vector to all neighbors
    if updated:
        print(f"Node 0's distance table updated: {distance_table}")
        send_to_neighbors()

# Link change handler for node 0
def linkhandler0(linkid, newcost):
    # If handling link cost changes is required, implement this function
    pass


# for part 2 to handle changes in the link cost between node 0 and node 1
# For node0.py
def rtlinkhandler0(linkid, newcost):
    print("HERE")
    global distance_table
    updated = False
    old_cost = distance_table[linkid][0]
    distance_table[linkid][0] = newcost

    # Check if this new link cost affects the minimum cost path to other nodes
    for i in range(4):
        if i != 0:  # Skip the distance to self
            print("OKEEE 1")
            via_link_cost = distance_table[i][linkid] + newcost
            if via_link_cost < distance_table[i][0]:
                print("VIA LINK COST < DISTANCE TABE")
                distance_table[i][0] = via_link_cost
                updated = True
            elif old_cost + distance_table[i][linkid] == distance_table[i][0]:  # If the old route was the shortest
                print("GOT ELSE IF")
                distance_table[i][0] = min([distance_table[i][j] for j in range(4)])  # Recalculate the shortest path
                updated = True

    if updated:
        print("TRIGGERED")
        print(f"Node 0 link cost updated. New distance table: {distance_table}")
        send_to_neighbors()
