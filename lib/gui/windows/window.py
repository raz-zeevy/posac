import ttkbootstrap as ttk
from lib.gui.const import p_ICON
from lib.utils import get_resource


class Window(ttk.Toplevel):
    def __init__(self, **kwargs):
        geom = None
        if "geometry" in kwargs:
            geom = kwargs.pop("geometry")
        super().__init__(**kwargs)
        self.iconbitmap(get_resource(p_ICON))
        if geom: self.geometry(geom)
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.center_window()
    def center_window(self):
        self.update_idletasks()  # Update "requested size" from geometry manager
        # Calculate x and y coordinates for the Tk root window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = (screen_width / 2) - (size[0] / 2)
        y = 20
        self.geometry("+%d+%d" % (x, y))
    def on_closing(self):
        self.destroy()