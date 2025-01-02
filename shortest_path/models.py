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

        # Clear axes in case of re-plot
        self.axes.clear()
        
        # Input validation
        if nodes <= 0 or edges < 0:
            # print("Error: Number of nodes must be positive and edges cannot be negative.")
            error_message = "Error: Number of nodes must be positive and edges cannot be negative."
            print(error_message)
            self.axes.set_title(error_message, fontsize=14, color="red", wrap=True)
            return

        if edges > nodes * (nodes - 1) // 2:
            # print("Error: Too many edges for the given number of nodes.")
            error_message = "Error: Too many edges for the given number of nodes."
            print(error_message)
            self.axes.set_title(error_message, fontsize=14, color="red", wrap=True)
            return
        
        # Generate random graph
        G = nx.gnm_random_graph(nodes, edges, seed=rng)
        
        # Ensure the graph is connected
        if not nx.is_connected(G):
            print("Warning: Generated graph is not connected. Shortest path may not exist.")
        
        pos = nx.circular_layout(G)
        nx.draw(G, ax=self.axes, pos=pos, with_labels=True)

        # Add random weights to edges
        for u, v in G.edges:
            G.edges[u, v]["weight"] = rng.integers(5, 15)
        
        # Check if start and end nodes are valid
        if start not in G.nodes or end not in G.nodes:
            error_message = "Error: Start or end node is invalid."
            print(error_message)
            self.axes.set_title(error_message, fontsize=14, color="red", wrap=True)
            # label_text = "Error: Start or end node is invalid."
            # self.axes.text(0.5, -0.1, label_text, transform=self.axes.transAxes, ha="center", fontsize=10, color="red")
            # print(label_text)
            return

        try:
            # Find shortest path
            path = nx.shortest_path(G, source=start, target=end, weight="weight")
            short_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

            # Highlight shortest path edges
            nx.draw_networkx_edges(
                G,
                edgelist=short_path,
                pos=pos,
                ax=self.axes,
                width=4.5,
                edge_color="b",
            )

            # Highlight nodes in the path
            nx.draw_networkx_nodes(G, pos=pos, ax=self.axes, node_color='w')
            nx.draw_networkx_nodes(
                G,
                pos=pos,
                nodelist=path,
                ax=self.axes,
                node_shape='o',
                node_color='lightblue',
                edgecolors='y',
            )

            # Display path information as a label
            label_text = f"Nodes: {nodes}, Edges: {edges}, Shortest Path: {path}"
            print(label_text)
        except nx.NetworkXNoPath:
            # Handle no path scenario
            label_text = f"Nodes: {nodes}, Edges: {edges}, No path found between {start} and {end}."
            print(label_text)
        
        # Add the label to the plot
        self.axes.text(0.5, -0.1, label_text, transform=self.axes.transAxes, ha="center", fontsize=10, color="blue")

        # Set the title to include nodes and edges
        self.axes.set_title(f"Graph with {nodes} Nodes and {edges} Edges", fontsize=14)

        # Store the graph for further reference
        self.nodes.append(G)


    # def network(self, nodes, edges, start, end):
    #     rng = default_rng(12345)
        
    #     # Input validation
    #     if nodes <= 0 or edges < 0:
    #         print("Error: Number of nodes must be positive and edges cannot be negative.")
    #         return

    #     if edges > nodes * (nodes - 1) // 2:
    #         print("Error: Too many edges for the given number of nodes.")
    #         return
        
    #     # Generate random graph
    #     G = nx.gnm_random_graph(nodes, edges, seed=rng)
        
    #     # Ensure the graph is connected
    #     if not nx.is_connected(G):
    #         print("Warning: Generated graph is not connected. Shortest path may not exist.")
        
    #     pos = nx.circular_layout(G)
    #     nx.draw(G, ax=self.axes, pos=pos, with_labels=True)

    #     # Add random weights to edges
    #     for u, v in G.edges:
    #         G.edges[u, v]["weight"] = rng.integers(5, 15)
        
    #     # Check if start and end nodes are valid
    #     if start not in G.nodes or end not in G.nodes:
    #         print("Error: Start or end node is not valid.")
    #         return

    #     try:
    #         # Find shortest path
    #         path = nx.shortest_path(G, source=start, target=end, weight="weight")
    #         short_path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]

    #         # Highlight shortest path edges
    #         nx.draw_networkx_edges(
    #             G,
    #             edgelist=short_path,
    #             pos=pos,
    #             ax=self.axes,
    #             width=4.5,
    #             edge_color="b",
    #         )

    #         # Highlight nodes in the path
    #         nx.draw_networkx_nodes(G, pos=pos, ax=self.axes, node_color='w')
    #         nx.draw_networkx_nodes(
    #             G,
    #             pos=pos,
    #             nodelist=path,
    #             ax=self.axes,
    #             node_shape='o',
    #             node_color='lightblue',
    #             edgecolors='y',
    #         )
    #     except nx.NetworkXNoPath:
    #         print("Error: No path exists between the start and end nodes.")
    #         return

    #     # Store the graph for further reference
    #     self.nodes.append(G)
    #     print("Network plotted successfully.")


    # def network(self, nodes, edges, start, end):
    #     try:
    #         # Input validation
    #         if not isinstance(nodes, int) or nodes <= 0:
    #             raise ValueError("Invalid number of nodes")
    #         if not isinstance(edges, int) or edges < 0:
    #             raise ValueError("Invalid number of edges")
    #         if not isinstance(start, int) or start < 0 or start >= nodes:
    #             raise ValueError("Invalid start node")
    #         if not isinstance(end, int) or end < 0 or end >= nodes:
    #             raise ValueError("Invalid end node")

    #         # Graph creation
    #         if edges > nodes * (nodes - 1) // 2:
    #             raise ValueError("Too many edges for the given number of nodes")

    #         rng = default_rng(12345)
    #         G = nx.gnm_random_graph(nodes, edges, seed=rng)
    #         pos = nx.circular_layout(G)

    #         # Shortest path calculation
    #         try:
    #             path = nx.shortest_path(G, start, end, weight="weight")
    #         except nx.NetworkXNoPath:
    #             print("No path found between the start and end nodes")
    #             return

    #         # Plotting
    #         if self.axes is not None:
    #             self.axes.clear()
    #         nx.draw(G, ax=self.axes, pos=pos, with_labels=True)

    #         # Add weight to each edge
    #         for u, v in G.edges:
    #             G.edges[u, v]["weight"] = rng.integers(5, 15)

    #         # Show shortest path
    #         short_path = [tuple(path[0:2]), tuple(path[1:3]), tuple(path[2:4])]
    #         nx.draw_networkx_edges(
    #             G,
    #             edgelist=short_path,
    #             pos=pos,
    #             ax=self.axes,
    #             width=4.5,
    #             edge_color="b",
    #         )
    #         nx.draw_networkx_nodes(G, pos=pos, ax=self.axes, node_color='w')
    #         nx.draw_networkx_nodes(G, pos=pos, nodelist=path, ax=self.axes, node_shape='o', node_color='lightblue', edgecolors='y')

    #         self.nodes.append(G)

    #     except Exception as e:
    #         print(f"An error occurred: {e}")

            
    # def network(self, nodes, edges, start, end):
    #     rng = default_rng(12345)
    #     G = nx.gnm_random_graph(nodes, edges, seed=rng)
    #     pos = nx.circular_layout(G)

    #     nx.draw(G, ax=self.axes, pos=pos, with_labels=True)

    #     # add weight to each edge so that some routes are preferable
    #     for u, v in G.edges:
    #         G.edges[u,v]["weight"] = rng.integers(5, 15)
    #     path = nx.shortest_path(G, start, end, weight="weight") 
    #     # print(path)
    #     short_path=([tuple(path[0:2]), tuple(path[1:3]), tuple(path[2:4])])

    #     # show shortest path
    #     nx.draw_networkx_edges(
    #         G, 
    #         edgelist=short_path, 
    #         pos=pos, 
    #         ax=self.axes, 
    #         width=4.5, 
    #         edge_color="b",
    #         )
    #     nx.draw_networkx_nodes(G, pos=pos, ax=self.axes, node_color='w')
    #     nx.draw_networkx_nodes(G, pos=pos, nodelist=path, ax=self.axes, node_shape='o', node_color='lightblue', edgecolors='y')


    #     self.nodes.append(G)

        ###################################

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
