"""
shortest-path/application.py: root window class
"""
import tkinter as tk
from tkinter import ttk
from . import views as v
from . import models as m

# graph
import networkx as nx
from numpy.random import default_rng

class Application(tk.Tk):  # subclase from Tk instead of Frame
    """Application root window.
    It needs to contain:
        - A title label
        - An instance of MyForm class (call and place form in GUI)

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = m.DrawNetwork(self)
        # Add form with widgets
        self.myform = v.MyForm(self, self.model)
        self.nodeform = v.NodeForm(self, self.model)
        # self.nodeform = v.MyForm(self, self.model)

        # window title
        self.title('Shortest Path NetworkX')
        self.columnconfigure(0, weight=0)

        # header
        ttk.Label(  # parent is self. self is our Tk instance inside this class
            self, text='Shortest Path',
            font=("TkDefaultFont, 18")
        ).grid(row=0)


        self.myform.grid(row=1, padx=10, sticky=tk.W + tk.E)
        self.nodeform.grid(row=1, column=2, padx=10, sticky=tk.W + tk.E, columnspan=3)
        self.myform.bind('<<GeneratePlot>>', self._on_generate)


        # data_nodes = self.model.nodes()
        # data_seeds= self.model.seeds()
        # data_network = self.model.network()


        def show_node_network(self, *_):
            chart = v.NodeNetwork(
                self.nodeform,
            )
            # chart.pack(fill='both', expand=True)
            chart.grid(row=1, column=3, columnspan=3)
            # data = data_network
            # chart.draw_network(20, 40, 7, 20)
            chart.draw_default(20, 15)#, 7, 9)#, 7, 20)
            
        show_node_network(self)
    


        ############# EXAMPLE PLOTS #############
        # def show_mychart(self, *_):
        #     # data = self.model.nodes()
        #     data = data_nodes
        #     # popup = tk.Toplevel()
        #     # chart = v.YieldChartView(
        #     chart = v.LineChartView(
        #         self.myform, data, (800,400),
        #         'Day','Average Height (cm)','lab_id'
        #     )
        #     chart.pack(fill='both', expand=True)
        #
        # show_mychart(self)

        # def show_yield_chart(self, *_):
        #     # popup = tk.Toplevel()
        #     chart = v.YieldChartView(
        #     self.myform,
        #     'Average plot humidity', 'Average plot temperature',
        #     'Yield as a product of humidity and temperature'
        #     )
        #     chart.pack(fill='both', expand=True)
        #     # data = self.model.get_yield_by_plot()
        #     data = data_seeds
        #     seed_colors = {
        #     'AXM477': 'red', 'AXM478': 'yellow',
        #     'AXM479': 'green', 'AXM480': 'blue'
        #     }
        #     for seed, color in seed_colors.items():
        #         seed_data = [
        #         (x['avg_humidity'], x['avg_temperature'], x['yield'])
        #         for x in data if x['seed_sample'] == seed
        #         ]
        #     chart.draw_scatter(seed_data, color, seed)
        #
        # show_yield_chart(self)
        #
        ############### END EXAMPLES ############
    
            

    def _on_generate(self, *_):
        # print('click')

        data = self.myform.get()
        print(data)
        
        def print_new(self, *_):
            '''Generate New Plot'''
            chart= m.DrawNetwork(self.nodeform)
            chart.grid(row=1,column=3, columnspan=3)
            chart.network(data['num_nodes'], data['num_edges'],data['start_node'], data['end_node'])
        print_new(self)

    

if __name__ == "__main__":
    # create instance of our application and start its mainloop
    app = Application()
    app.mainloop()
