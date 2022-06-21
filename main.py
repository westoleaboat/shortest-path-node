import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt
from numpy.random import default_rng

rng = default_rng(12345) #seed for reproducibility
"""shortest path between two nodes in a network"""

# create random network
G = nx.gnm_random_graph(10, 17, seed=12345)#nodes, edges, randomnes

# draw the network in circular arrengement to see node connect to each other
fig, ax = plt.subplots()
pos = nx.circular_layout(G)
nx.draw(G, ax=ax, pos=pos, with_labels=True)
ax.set_title("Random network for shortest path finding\nFrom node 7 to 9")

# add weight to each edge so that some routes are preferable
for u, v in G.edges:
    G.edges[u,v]["weight"] = rng.integers(5, 15)

# compute shortest path from node 7 to node 9 using nx.shortest_path routine
path = nx.shortest_path(G, 7, 9, weight="weight") #find shortest path according to "weight" attribute of edge, meaning "shortest" being "fewest edges"
print(f'shortest path = {path}')

short_path=([tuple(path[0:2]), tuple(path[1:3]), tuple(path[2:4])])

# show shortest path
nx.draw_networkx_edges(G, edgelist=short_path, pos=pos, ax=ax, width=4.5, edge_color="b")

# show edges in path
nx.draw_networkx_edges(G, edgelist=G.edges(path), pos=pos, ax=ax, width=1.5, edge_color="r")

# find length of this shortest path
lenght=nx.shortest_path_length(G, 7, 9, weight="weight",)
print("length", lenght)


plt.show()
