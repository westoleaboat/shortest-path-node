"""
shortest-path/views.py: form containing widgets
"""

import tkinter as tk
from tkinter import ttk

from . import widgets as w
from .constants import FieldTypes as FT

import matplotlib
import matplotlib.pyplot
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import networkx as nx
from numpy.random import default_rng

import numpy as np
from itertools import combinations
from matplotlib import animation
from matplotlib.patches import Circle

class NodeForm(tk.Frame):

    def _add_frame(self, label, cols=3):
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame

    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.model = model
        fields = self.model.fields


        self.columnconfigure(0, weight=1)

        networkFrame = self._add_frame(
        'Network'
        )
        
class SimForm(tk.Frame):
    def _add_frame(self, label, cols=3):
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame

    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.model = model
        fields = self.model.fields


        self.columnconfigure(0, weight=1)

        simFrame = self._add_frame(
        'Simulation'
        )


class MyForm(tk.Frame):
    """Input Form for widgets

    - self._vars = Create a dictionary to hold all out variable objects 
    - _add_frame = instance method that add a new label frame. Pass in 
                   label text and optionally a number of columns.

    """

    var_types = {
        FT.string: tk.StringVar,
        FT.string_list: tk.StringVar,
        FT.short_string_list: tk.StringVar,
        FT.iso_date_string: tk.StringVar,
        FT.long_string: tk.StringVar,
        FT.decimal: tk.DoubleVar,
        FT.integer: tk.IntVar,
        FT.boolean: tk.BooleanVar
    }

    def _add_frame(self, label, cols=3):
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame

   

    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.model = model
        fields = self.model.fields

        self._vars = {  # hold all variable objects
            key: self.var_types[spec['type']]()
            for key, spec in fields.items()
        }

        # disable var for Output field
        self._disable_var = tk.BooleanVar()

        # build the form
        self.columnconfigure(0, weight=1)

        pathfinder = self._add_frame('short path')

        w.LabelInput(
          self, 
          'Nodes',
          input_class=ttk.Spinbox,
          var=self._vars['num_nodes'],
          input_args={
            "from_":2, 
            "to":100, 
            "increment":1,
            }

        ).grid(sticky='nswe', row=0, column=0)
        self._vars['num_nodes'].set(20)
        
    
        w.LabelInput(
          self, 
          'Edges',
          input_class=ttk.Spinbox,
          var=self._vars['num_edges'],
          input_args={
            "from_":3, 
            "to":100, 
            "increment":1,
            }

        ).grid(sticky='nswe', row=1, column=0)
        self._vars['num_edges'].set(15)

        w.LabelInput(
          pathfinder, 
          'Start',
          input_class=ttk.Entry,
          var=self._vars['start_node'],
  

        ).grid(sticky='nswe', row=0, column=0)
        self._vars['start_node'].set(7)

        w.LabelInput(
          pathfinder, 
          'End',
          input_class=ttk.Entry,
          var=self._vars['end_node'],

        ).grid(sticky='nswe', row=0, column=2)
        self._vars['end_node'].set(9)

        pathfinder.grid(row=3)
        


        # self._disable_var.set(True)

        # text to display data from form
        self.output_var = tk.StringVar()

        ###########
        # buttons #
        ###########
        # improving inter-object communication was added to bug tracker

        buttons = ttk.Frame(self)  # add on a frame
        buttons.grid(sticky=tk.W + tk.E, row=4)
        # # pass instance methods as callback commands
        self.generatebutton = ttk.Button(
            buttons, text="Generate", command=self._on_generate)
        self.generatebutton.pack(side=tk.RIGHT)
        
        
        # buttons = ttk.Frame(self)  # add on a frame
        # buttons.grid(sticky=tk.W + tk.E, row=4)
        # # pass instance methods as callback commands
        # self.transbutton = ttk.Button(
        #     buttons, text="Text to Binary", command=self._on_trans)
        # self.transbutton.pack(side=tk.RIGHT)

        # self.transbutton = ttk.Button(
        #     buttons, text="Binary to Text", command=self._on_trans, state='disabled')
        # self.transbutton.pack(side=tk.RIGHT)

        # # self.savebutton = ttk.Button(
        # #     buttons, text="Save", command=self.master._on_save)  # on parent
        # # self.savebutton.pack(side=tk.RIGHT)
        # self.resetbutton = ttk.Button(
        #     buttons, text="Reset", command=self.reset)  # on this class
        # self.resetbutton.pack(side=tk.RIGHT)

    # def reset(self):
    #     """Reset entries. Set all variables to empty string"""
    #     # activate widget
    #     self._disable_var.set(False)
    #     # self.set_output_state(tk.NORMAL)

    #     # reset data
    #     for var in self._vars.values():
    #         if isinstance(var, tk.BooleanVar):
    #             # uncheck checkbox
    #             var.set(False)
    #         else:
    #             # set inputs to empty string
    #             var.set('')
    #             # set data label to empty string
    #             # self.output_var.set('')
    #     # disable widget
    #     self._disable_var.set(True)
    #     # self.set_output_state(tk.DISABLED)

    def get(self):
        """Retrieve data from the form so it can be saved or used"""
        data = {}
        for key, variable in self._vars.items():
            try:
                # retrieve from ._vars
                data[key] = variable.get()
            except tk.TclError as e:
                # create error message
                message = f'Error in field: {key}. Data not saved!'
                raise ValueError(message) from e
        # return the data
        return data

    #########################################
    # Disable widget if disable_var not used:
    #
    # def set_output_state(self, state):
    #     output_widget = self._get_widget_by_var(self._vars['Output'])
    #     if output_widget:
    #         output_widget.input.configure(state=state)
    #
    # def _get_widget_by_var(self, var):
    #     """Return the widget associated with a given variable."""
    #     for widget in self.winfo_children():
    #         if isinstance(widget, w.LabelInput) and widget.variable == var:
    #             return widget
    #     return None
    #########################################
    def _on_generate(self):
        self.event_generate('<<GeneratePlot>>')
    

class NodeNetwork(tk.Frame):
    '''Draw default Node'''
    def __init__(self, parent):
        super().__init__(parent)
        self.figure = Figure(figsize=(6,4), dpi=100)
        self.canvas_tkagg = FigureCanvasTkAgg(self.figure, master=self)
        canvas = self.canvas_tkagg.get_tk_widget()
        canvas.pack(fill='both', expand=True)
        # Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas_tkagg, self)
        # Axes
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.axes.set_xlabel('x_axis')
        self.axes.set_ylabel('y_axis')
        self.axes.set_title('Network Node')
        self.nodes = list()
        # self.node_labels = list()

    def draw_default(self, nodes, edges):#:, start, end):#, min_nodes, max_nodes):
        rng = default_rng(12345)
        G = nx.gnm_random_graph(nodes, edges, seed=rng)
        pos = nx.circular_layout(G)

        nx.draw(G, ax=self.axes, pos=pos, with_labels=True)

        # add weight to each edge so that some routes are preferable
        for u, v in G.edges:
            G.edges[u,v]["weight"] = rng.integers(5, 15)


###### PARTICLE SIMULATION
class Particle:
    """A class representing a two-dimensional particle."""

    def __init__(self, x, y, vx, vy, radius=0.01, styles=None):
        """Initialize the particle's position, velocity, and radius.

        Any key-value pairs passed in the styles dictionary will be passed
        as arguments to Matplotlib's Circle patch constructor.

        """

        self.r = np.array((x, y))
        self.v = np.array((vx, vy))
        self.radius = radius
        self.mass = self.radius**2

        self.styles = styles
        if not self.styles:
            # Default circle styles
            self.styles = {'edgecolor': 'b', 'fill': False}

    # For convenience, map the components of the particle's position and
    # velocity vector onto the attributes x, y, vx and vy.
    @property
    def x(self):
        return self.r[0]
    @x.setter
    def x(self, value):
        self.r[0] = value
    @property
    def y(self):
        return self.r[1]
    @y.setter
    def y(self, value):
        self.r[1] = value
    @property
    def vx(self):
        return self.v[0]
    @vx.setter
    def vx(self, value):
        self.v[0] = value
    @property
    def vy(self):
        return self.v[1]
    @vy.setter
    def vy(self, value):
        self.v[1] = value

    def overlaps(self, other):
        """Does the circle of this Particle overlap that of other?"""

        return np.hypot(*(self.r - other.r)) < self.radius + other.radius

    def draw(self, ax):
        """Add this Particle's Circle patch to the Matplotlib Axes ax."""

        circle = Circle(xy=self.r, radius=self.radius, **self.styles)
        ax.add_patch(circle)
        return circle

    def advance(self, dt):
        """Advance the Particle's position forward in time by dt."""

        self.r += self.v * dt

class Simulation(tk.Frame):
    """A class for a simple hard-circle molecular dynamics simulation.

    The simulation is carried out on a square domain: 0 <= x < 1, 0 <= y < 1.

    """

    ParticleClass = Particle

    # def __init__(self, parent, n, radius=0.01, styles=None):
    def __init__(self, parent, n, radius, styles=None):
        super().__init__(parent)
    
        """Initialize the simulation with n Particles with radii radius.

        radius can be a single value or a sequence with n values.

        Any key-value pairs passed in the styles dictionary will be passed
        as arguments to Matplotlib's Circle patch constructor when drawing
        the Particles.

        """
    
        self.init_particles(n, radius, styles)
        self.dt = 0.01
        # self.radii = np.random.random(nparticles)*0.03+0.02
        # self.radius = np.random.random(nparticles)*0.03+0.02
    def place_particle(self, rad, styles):
        # Choose x, y so that the Particle is entirely inside the
        # domain of the simulation.
        x, y = rad + (1 - 2*rad) * np.random.random(2)
        # Choose a random velocity (within some reasonable range of
        # values) for the Particle.
        vr = 0.1 * np.sqrt(np.random.random()) + 0.05
        vphi = 2*np.pi * np.random.random()
        vx, vy = vr * np.cos(vphi), vr * np.sin(vphi)
        particle = self.ParticleClass(x, y, vx, vy, rad, styles)
        # Check that the Particle doesn't overlap one that's already
        # been placed.
        for p2 in self.particles:
            if p2.overlaps(particle):
                break
        else:
            self.particles.append(particle)
            return True
        return False

    def init_particles(self, n, radius, styles=None):
        """Initialize the n Particles of the simulation.

        Positions and velocities are chosen randomly; radius can be a single
        value or a sequence with n values.

        """

        try:
            iterator = iter(radius)
            assert n == len(radius)
        except TypeError:
            # r isn't iterable: turn it into a generator that returns the
            # same value n times.
            def r_gen(n, radius):
                for i in range(n):
                    yield radius
            radius = r_gen(n, radius)

        self.n = n
        self.particles = []
        for i, rad in enumerate(radius):
            # Try to find a random initial position for this particle.
            while not self.place_particle(rad, styles):
                pass

    def change_velocities(self, p1, p2):
        """
        Particles p1 and p2 have collided elastically: update their
        velocities.

        """
        
        m1, m2 = p1.mass, p2.mass
        M = m1 + m2
        r1, r2 = p1.r, p2.r
        d = np.linalg.norm(r1 - r2)**2
        v1, v2 = p1.v, p2.v
        u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
        u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
        p1.v = u1
        p2.v = u2

    def handle_collisions(self):
        """Detect and handle any collisions between the Particles.

        When two Particles collide, they do so elastically: their velocities
        change such that both energy and momentum are conserved.

        """ 

        # We're going to need a sequence of all of the pairs of particles when
        # we are detecting collisions. combinations generates pairs of indexes
        # into the self.particles list of Particles on the fly.
        pairs = combinations(range(self.n), 2)
        for i,j in pairs:
            if self.particles[i].overlaps(self.particles[j]):
                self.change_velocities(self.particles[i], self.particles[j])

    def handle_boundary_collisions(self, p):
        """Bounce the particles off the walls elastically."""

        if p.x - p.radius < 0:
            p.x = p.radius
            p.vx = -p.vx
        if p.x + p.radius > 1:
            p.x = 1-p.radius
            p.vx = -p.vx
        if p.y - p.radius < 0:
            p.y = p.radius
            p.vy = -p.vy
        if p.y + p.radius > 1:
            p.y = 1-p.radius
            p.vy = -p.vy

    def apply_forces(self):
        """Override this method to accelerate the particles."""
        pass

    def advance_animation(self):
        """Advance the animation by dt, returning the updated Circles list."""

        for i, p in enumerate(self.particles):
            p.advance(self.dt)
            self.handle_boundary_collisions(p)
            self.circles[i].center = p.r
        self.handle_collisions()
        self.apply_forces()
        self.canvas_tkagg.draw()
        return self.circles

    def advance(self):
        """Advance the animation by dt."""
        for i, p in enumerate(self.particles):
            p.advance(self.dt)
            self.handle_boundary_collisions(p)
        self.handle_collisions()
        self.apply_forces()

    def init(self):
        """Initialize the Matplotlib animation."""

        self.circles = []
        for particle in self.particles:
            self.circles.append(particle.draw(self.axes))
        return self.circles

    def animate(self, i):
        """The function passed to Matplotlib's FuncAnimation routine."""

        self.advance_animation()
        return self.circles

    def setup_animation(self):
        self.figure = Figure(figsize=(6,4), dpi=100)
        self.axes = self.figure.add_subplot(1, 1, 1)
        self.canvas_tkagg = FigureCanvasTkAgg(self.figure, master=self)
        canvas = self.canvas_tkagg.get_tk_widget()
        canvas.pack(fill='both', expand=True)
        # Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas_tkagg, self)

        for s in ['top','bottom','left','right']:
            self.axes.spines[s].set_linewidth(2)

        # Axes
        self.axes.set_aspect('equal', 'box')
        self.axes.set_title('Particle Collision Simulation')
        self.axes.set_xlim(0, 1)
        self.axes.set_ylim(0, 1)  
        self.axes.xaxis.set_ticks([])
        self.axes.yaxis.set_ticks([])


    def save_or_show_animation(self, anim, save, filename='collision.mp4'):
        if save:
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=10, bitrate=1800)
            anim.save(filename, writer=writer)
        else:
            # matplotlib.pyplot.show()
            self.canvas_tkagg.draw()

    def do_animation(self, save=False, interval=1, filename='collision.mp4'):
        """Set up and carry out the animation of the molecular dynamics.

        To save the animation as a MP4 movie, set save=True.
        """

        self.setup_animation()
        anim = animation.FuncAnimation(self.figure, self.animate,
                init_func=self.init, frames=800, interval=interval, blit=True)
        self.save_or_show_animation(anim, save, filename)


# if __name__ == '__main__':
#     nparticles = 20
#     radii = np.random.random(nparticles)*0.03+0.02
#     styles = {'edgecolor': 'C0', 'linewidth': 2, 'fill': None}
#     sim = Simulation(nparticles, radii, styles)
#     sim.do_animation(save=False)

###### END PARTICLE SIMULATION





################ EXAMPLE PLOT LOGIC ##################
#
# class LineChartView(tk.Canvas):
#   """A generic view for plotting a line chart"""

#   margin = 20
#   colors = [
#     'red', 'orange', 'yellow', 'green',
#     'blue', 'purple', 'violet',
#     # add more for more complex plots
#   ]

#   def __init__(
#     self, parent, data, plot_size,
#     x_field, y_field, plot_by_field
#   ):
#     self.data = data
#     self.x_field = x_field
#     self.y_field = y_field
#     self.plot_by_field = plot_by_field

#     # calculate view size
#     self.plot_width, self.plot_height = plot_size
#     view_width = self.plot_width + (2 * self.margin)
#     view_height = self.plot_height + (2 * self.margin)

#     super().__init__(
#       parent, width=view_width,
#       height=view_height, background='lightgrey'
#     )
#     # Draw chart
#     self.origin = (self.margin, view_height - self.margin)
#     # X axis
#     self.create_line(
#       self.origin,
#       (view_width - self.margin, view_height - self.margin)
#     )
#     # Y axis
#     self.create_line(
#       self.origin, (self.margin, self.margin), width=2
#     )
#     # X axis label
#     self.create_text(
#       (view_width // 2, view_height - self.margin),
#       text=x_field, anchor='n'
#     )
#     # Y axis label
#     self.create_text(
#       (self.margin, view_height // 2),
#       text=y_field, angle=90, anchor='s'
#     )
#     self.plot_area = tk.Canvas(
#       self, background='#555',
#       width=self.plot_width, height=self.plot_height
#     )
#     self.create_window(
#       self.origin, window=self.plot_area, anchor='sw'
#     )

#     # Draw legend and lines
#     plot_names = sorted(set([
#       row[self.plot_by_field]
#       for row in self.data
#     ]))

#     color_map = list(zip(plot_names, self.colors))

#     for plot_name, color in color_map:
#       dataxy = [
#         (row[x_field], row[y_field])
#         for row in data
#         if row[plot_by_field] == plot_name
#       ]
#       self._plot_line(dataxy, color)

#     self._draw_legend(color_map)


#   def _plot_line(self, data, color):
#     """Plot a line described by data in the given color"""

#     max_x = max([row[0] for row in data])
#     max_y = max([row[1] for row in data])
#     x_scale = self.plot_width / max_x
#     y_scale = self.plot_height / max_y
#     coords = [
#       (round(x * x_scale), self.plot_height - round(y * y_scale))
#       for x, y in data
#     ]
#     self.plot_area.create_line(
#       *coords, width=4, fill=color, smooth=True
#     )

#   def _draw_legend(self, color_map):
#     # determine legend
#     for i, (label, color) in enumerate(color_map):
#       self.plot_area.create_text(
#         (10, 10 + (i * 20)),
#         text=label, fill=color, anchor='w'
#       )


# class YieldChartView(tk.Frame):

#   def __init__(self, parent, x_axis, y_axis, title):
#     super().__init__(parent)
#     self.figure = Figure(figsize=(6, 4), dpi=100)
#     self.canvas_tkagg = FigureCanvasTkAgg(self.figure, master=self)
#     canvas = self.canvas_tkagg.get_tk_widget()
#     canvas.pack(fill='both', expand=True)
#     self.toolbar = NavigationToolbar2Tk(self.canvas_tkagg, self)
#     self.axes = self.figure.add_subplot(1, 1, 1)
#     self.axes.set_xlabel(x_axis)
#     self.axes.set_ylabel(y_axis)
#     self.axes.set_title(title)
#     self.scatters = list()
#     self.scatter_labels = list()

#   def draw_scatter(self, data2, color, label):
#     x, y, size = zip(*data2)
#     scaled_size = [(s ** 2)//2 for s in size]
#     scatter = self.axes.scatter(
#       x, y, scaled_size,
#       c=color, label=label, alpha=0.5
#     )
#     self.scatters.append(scatter)
#     self.scatter_labels.append(label)
#     self.axes.legend(self.scatters, self.scatter_labels)



      

