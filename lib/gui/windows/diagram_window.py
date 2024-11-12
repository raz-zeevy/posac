import os
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import filedialog
from lib.gui.components.form import NavigationButton
import matplotlib
from lib.gui.windows.window import Window
from lib.gui.components.shapes import Line, Circle, DivideAxis, Edge
from lib.utils import get_resource, rreal_size, real_size

G_COLOR = '#a4aab3'
DPI_SAVE = 300
matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

BORDER_WIDTH = 0
OC = 0.00

class DiagramWindow(Window):
    def __init__(self, parent, graph_data_lst: list, **kwargs):
        """
        graph_data: list of dictionaries containing the data to be plotted
        should contain "x", "y", "annotations", "title", "legend",
         "captions", "geom" keys
        """
        super().__init__(**kwargs, geometry=f"{rreal_size(800)}x"
                                            f"{rreal_size(700)}")
        self.title("Posac Solution")
        # self.iconbitmap(get_resource("icon.ico"))
        # sets the geometry of toplevel
        self.graph_data_lst = graph_data_lst
        self.index = 0
        # init
        self.create_navigation()
        self.create_menu()
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side=tk.TOP,
                             fill=tk.BOTH,
                             expand=True)
        self.load_page(self.index)
        # Bind key presses to the respective methods
        self.bind("<Return>", lambda x: self.next_graph())
        self.bind("<Right>", lambda x: self.next_graph())
        self.bind("<BackSpace>", lambda x: self.previous_graph())
        self.bind("<Left>", lambda x: self.previous_graph())
        self.bind("<Escape>", lambda x: self.exit())

    def create_menu(self):
        # create a file menu with save figure command to save the current graph
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save figure ",
                                   command=self.save_figure)
        # add an option to save all figures
        self.file_menu.add_command(label="Save all figures",
                                   command=self.save_all_figures)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit)

    def get_default_fig_file_name(self):
        label = self.graph_data_lst[self.index]["title"]
        clean_label = label.replace(" ", "_")
        default_name = f"{clean_label}.png"
        return default_name

    def save_figure(self):
        default_name = self.get_default_fig_file_name()
        file = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files",
                                                        "*.png")],
                                            initialfile=default_name)
        if file:
            self.figure.savefig(file, dpi=DPI_SAVE)

    def save_all_figures(self):
        dir = filedialog.askdirectory()
        current_page = self.index
        self.load_page(0)
        for i in range (len(self.graph_data_lst)):
            # I don't use the self.get_name because it would cause that
            # some figures would not be saved
            path = os.path.join(dir, "figure_" + str(i + 1) + ".png")
            self.figure.set_size_inches(5, 5)
            self.figure.savefig(path, dpi=DPI_SAVE)
            self.next_graph()
        self.index = current_page
        self.load_page(current_page)

    def init_scrollable_legend(self):
        self.legend_canvas = tk.Canvas(self.main_frame,
                                       borderwidth=BORDER_WIDTH,
                                       background="red",
                                       width=rreal_size(175))
        self.diagram_labels_frame = ttk.Frame(self.legend_canvas,
                                              borderwidth=BORDER_WIDTH,
                                              relief="solid", )
        # Adjust the width as needed
        self.vsb = ttk.Scrollbar(self.main_frame, orient="vertical",
                                 command=self.legend_canvas.yview)
        self.legend_canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.legend_canvas.pack(side="right", fill="both",expand=False)
        self.canvas_frame = self.legend_canvas.create_window((0, 0),
                                                             window=self.diagram_labels_frame,
                                                             anchor="nw")
        self.diagram_labels_frame.bind("<Configure>", self.onFrameConfigure)
        self.legend_canvas.bind('<Configure>', self.FrameWidth)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.legend_canvas.configure(
            scrollregion=self.legend_canvas.bbox("all"))

    def FrameWidth(self, event):
        '''Reset the canvas window to encompass inner frame when resizing'''
        canvas_width = event.width
        self.legend_canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def navigate_control(self):
        if self.index < len(self.graph_data_lst) - 1:
            self.button_next.state(["!disabled"])
        else:
            self.button_next.state(["disabled"])
        if self.index > 0:
            self.button_previous.state(["!disabled"])
        else:
            self.button_previous.state(["disabled"])

    def next_graph(self):
        if self.index < len(self.graph_data_lst) - 1:
            self.index += 1
            self.load_page(self.index)

    def previous_graph(self):
        if self.index > 0:
            self.index -= 1
            self.load_page(self.index)

    def exit(self):
        self.destroy()

    def load_page(self, i):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        self.navigate_control()
        #
        self.diagram_frame = ttk.Frame(self.main_frame)
        self.diagram_frame.pack(side=tk.LEFT,
                                fill=tk.BOTH,
                                expand=True)
        self.plot_scatter(self.graph_data_lst[i])
        if len(self.graph_data_lst[i]["legend"]) > 30:
            self.init_scrollable_legend()
        else:
            self.diagram_labels_frame = ttk.Frame(self.main_frame)
            self.diagram_labels_frame.pack(side=tk.RIGHT,
                                           expand=False,
                                           fill='y',
                                           padx=rreal_size((0, 65)))
        self.diagram_labels_frame.config(
            width=rreal_size(30))
        self.plot_legend(self.graph_data_lst[i])

    def plot_legend(self, graph_data):
        diagram_title_frame = ttk.Frame(self.diagram_labels_frame,
                                        borderwidth=BORDER_WIDTH)
        diagram_title_frame.pack(side=tk.TOP,
                                 fill=tk.X,
                                 expand=False,
                                 pady=real_size((0, 0)))
        diagram_label = ttk.Label(diagram_title_frame,
                                  text=graph_data["title"],
                                  font='Helvetica 11 bold')
        diagram_label.pack(side=tk.TOP,
                           expand=True,
                           fill='x')
        # now create labels for all the variables and their labels, this will
        # be done in a loop and serve like a legend for the diagram
        legend_items_frame = ttk.Frame(self.diagram_labels_frame, )
        legend_items_frame.pack(side=tk.TOP,
                                fill=tk.BOTH,
                                expand=True,
                                pady=(5, 0))
        for item in graph_data["legend"]:
            space = "     " if item["index"] < 10 else "   "
            label = ttk.Label(legend_items_frame,
                              text=f'{item["index"]}{space}{item["value"]}',
                              borderwidth=BORDER_WIDTH,
                              font='Helvetica 11',
                              relief="solid", )
            label.pack(side=tk.TOP, fill=tk.BOTH)

    def plot_scatter(self, graph_data):
        def add_geoms(x, axes, graph_data):
            def add_line(x, axes, line: Line):
                # Create a figure and axis
                start, end = min(x) * 0.5, max(
                    x) * 2  # buffers to ensure it is
                # long enough
                start, end = start - (end - start) * OC, end + (
                        end - start) * OC

                # Plot each line
                x_values, y_values = line.get_points(start, end)
                axes.plot(x_values, y_values, color=G_COLOR)

            def add_circle(axes, circle: Circle):
                # Create a circle patch
                circle_plot = matplotlib.patches.Circle(circle.center,
                                                        circle.radius,
                                                        edgecolor=G_COLOR,
                                                        facecolor='none')
                # Add the circle to the plot
                axes.add_patch(circle_plot)

            def add_divide_axis(axes, divide_axis: DivideAxis):
                x_values, y_values = divide_axis.get_points(1000)
                axes.plot(x_values, y_values, color=G_COLOR)

            def add_edge(axes, edge: Edge):
                x_values, y_values = edge.get_points()
                axes.plot(x_values, y_values, color=G_COLOR)

            if 'geoms' not in graph_data:
                return
            for geom in graph_data["geoms"]:
                if isinstance(geom, Line):
                    add_line(x, axes, geom)
                elif isinstance(geom, Circle):
                    add_circle(axes, geom)
                elif isinstance(geom, DivideAxis):
                    add_divide_axis(axes, geom)
                elif isinstance(geom, Edge):
                    add_edge(axes, geom)
                else:
                    raise ValueError(f"Unknown geometry type: {type(geom)}")

        x = graph_data["x"]
        y = graph_data["y"]
        z = graph_data["annotations"]
        # create a figure and axis
        self.figure = Figure(figsize=rreal_size((6, 6)), dpi=100)
        figure_canvas = FigureCanvasTkAgg(self.figure,
                                          self.diagram_frame)
        axes = self.figure.add_subplot()
        # plot the data
        axes.scatter(x, y, alpha=0)
        # set the title
        caption = ""
        if "caption" in graph_data:
            caption = graph_data["caption"]
        # set the title text to be smaller
        axes.text(0, -0.1, caption, ha='left', va='top',
                  transform=axes.transAxes, fontsize=8)
        self.figure.subplots_adjust(left=0.1,
                                    right=0.95,
                                    top=0.95,
                                    bottom=0.15)
        # create annotations
        annot_offset = (max(y) - min(y)) / 100
        for i, txt in enumerate(z):
            axes.annotate(txt, (x[i], y[i] - annot_offset),
                          ha='center',
                          fontsize=9)
        # add geom
        add_geoms(x, axes, graph_data)
        # Adjust the plot limits to make sure it fits
        start_x, end_x = 0, 100
        start_y, end_y = 0, 100
        x_offset, y_offset = (end_x - start_x) * OC * 0.75, \
                             (end_y - start_y) * OC * 0.75
        axes.set_xlim([start_x - x_offset, end_x + x_offset])
        axes.set_ylim([start_y - y_offset, end_y + y_offset])
        figure_canvas.get_tk_widget().pack(side=tk.TOP)

    def create_navigation(self):
        # Navigation Buttons Frame
        frame_navigation = ttk.Frame(self)
        # pack the navigation at the bottom of the screen but above the help
        # bar
        frame_navigation.pack(side=ttk.BOTTOM, fill='x', padx=10,
                              pady=(0, 40))
        center_frame = ttk.Frame(frame_navigation)
        center_frame.pack(pady=5, expand=False)
        self.button_previous = NavigationButton(center_frame,
                                                text="Previous",
                                                command=self.previous_graph, )
        self.button_previous.pack(side=ttk.LEFT, padx=20)
        self.button_next = NavigationButton(center_frame, text="Next",
                                            command=self.next_graph, )
        self.button_next.pack(side=ttk.LEFT, padx=20, )
        self.button_exit = NavigationButton(center_frame, text="Exit",
                                            bootstyle='secondary',
                                            command=self.exit, )
        self.button_exit.pack(side=ttk.LEFT, padx=20)
