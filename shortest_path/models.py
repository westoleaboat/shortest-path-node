""" shortest_path/models.py"""

from .constants import FieldTypes as FT
from .views import NodeNetwork, Simulation

import networkx as nx
import matplotlib 
import matplotlib.pyplot
from numpy.random import default_rng
from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

class DrawSim(Simulation):
    # Continue for dynamic functionality when changing values in GUI ...
    fields = {}
    # def sim()

class DrawNetwork(NodeNetwork):
    fields = {
        "num_nodes": {'req': True, 'type': FT.integer},
        "num_edges": {'req': True, 'type': FT.integer},
        "start_node": {'req': True, 'type': FT.integer},
        "end_node": {'req': True, 'type': FT.integer}
    }


    def network(self, nodes, edges, start, end):
        rng = default_rng(12345)
        G = nx.gnm_random_graph(nodes, edges, seed=rng)
        pos = nx.circular_layout(G)

        nx.draw(G, ax=self.axes, pos=pos, with_labels=True)

        # add weight to each edge so that some routes are preferable
        for u, v in G.edges:
            G.edges[u,v]["weight"] = rng.integers(5, 15)
        path = nx.shortest_path(G, start, end, weight="weight") 
        # print(path)
        short_path=([tuple(path[0:2]), tuple(path[1:3]), tuple(path[2:4])])

        # show shortest path
        nx.draw_networkx_edges(
            G, 
            edgelist=short_path, 
            pos=pos, 
            ax=self.axes, 
            width=4.5, 
            edge_color="b",
            )
        nx.draw_networkx_nodes(G, pos=pos, ax=self.axes, node_color='w')
        nx.draw_networkx_nodes(G, pos=pos, nodelist=path, ax=self.axes, node_shape='o', node_color='lightblue', edgecolors='y')


        self.nodes.append(G)

        # show edges in path
        # nx.draw_networkx_edges(G, edgelist=G.edges(path), pos=pos, ax=self.axes, width=1.5, edge_color="r")

        # find length of this shortest path
        # lenght=nx.shortest_path_length(G, start, end, weight="weight",)
        # print(f"lenght: {lenght}")

        # self.node_label.append(label)


############### EXAMPLE DATA #####################
#   views.py LineChart Example Data
#
#     def nodes(self):
#         num_nodes = {'A', 'B', 'C'}
#         data = [
#     {"Day": 0, "lab_id": "A", "Average Height (cm)": 1.4198750000000000},
#     {"Day": 0, "lab_id": "B", "Average Height (cm)": 1.3320000000000000},
#     {"Day": 0, "lab_id": "C", "Average Height (cm)": 1.5377500000000000},
#     {"Day": 1, "lab_id": "A", "Average Height (cm)": 1.7266250000000000},
#     {"Day": 1, "lab_id": "B", "Average Height (cm)": 1.8503750000000000},
#     {"Day": 1, "lab_id": "C", "Average Height (cm)": 1.4633750000000000},
# ]
#         return data

#   views.py YieldChartView Example Data
#
#     def seeds(self):
#         data2 = [
#     {"seed_sample": "AXM480", "yield": 11, "avg_humidity": 27.7582142857142857, "avg_temperature": 23.7485714285714286},
#     {"seed_sample": "AXM480", "yield": 20, "avg_humidity": 27.2146428571428571, "avg_temperature": 23.8032142857142857},
#     {"seed_sample": "AXM480", "yield": 15, "avg_humidity": 26.2896428571428571, "avg_temperature": 23.6750000000000000},
#     {"seed_sample": "AXM478", "yield": 31, "avg_humidity": 27.2928571428571429, "avg_temperature": 23.8317857142857143},
#     {"seed_sample": "AXM477", "yield": 39, "avg_humidity": 27.1003571428571429, "avg_temperature": 23.7360714285714286},
#     {"seed_sample": "AXM478", "yield": 39, "avg_humidity": 26.8550000000000000, "avg_temperature": 23.7632142857142857}
# ]
#         return data2
#####################################
