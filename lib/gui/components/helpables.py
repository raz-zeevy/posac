import tkinter as tk
from tkinter import Label, Frame
from abc import ABC
from tkinter import ttk
import ttkbootstrap as ttkb

def absolute_x(widget):
    if widget == widget.winfo_toplevel():
        return 0
    return widget.winfo_x() + absolute_x(widget.nametowidget(widget.winfo_parent()))


def absolute_y(widget):
    if widget == widget.winfo_toplevel():
        return 0
    return widget.winfo_y() + absolute_y(widget.nametowidget(widget.winfo_parent()))


class Helpable(ABC):
    """
    HelpMixin class is an abstract class that provides a help text when the
    user presses the F1 key. The help text is shown in a Frame widget below
    the entry widget.
    """
    BG_COLOR = '#FEFAE0'
    TITLE_COLOR = 'blue'
    SHADOW_BG_COLOR = '#A3A3A3'
    TITLE_FONT = ("Arial", 13, "bold")
    root = None

    @classmethod
    def init(cls, root):
        cls.root = root
        cls.style = ttkb.Style()
        cls.style.configure('Shadow.TFrame',
                            background=cls.SHADOW_BG_COLOR)

    def __init__(self, help_title="Help Title",
                 help_text="Help Text",
                 **kwargs):
        if not self.root:
            raise UserWarning("HelpMixin.init(root) must be called before creating any Helpable widgets.")
        self.title_font = self.TITLE_FONT
        self.help_title = help_title
        self.help_text = help_text
        self.help_frame = None
        self.shadow_frame = None
        super().__init__(**kwargs)
        # if not help_text: return
        self.bind("<FocusIn>", self._bind_help)
        self.bind("<FocusOut>", self._unbind_help)

    def help_style(self, **kwargs):
        """
        Set the style of the help text.
        :param kwargs: bg_color, title_color, shadow_bg_color, title_font
        :return:
        """
        self.BG_COLOR = kwargs.get('bg_color', self.BG_COLOR)
        self.TITLE_COLOR = kwargs.get('title_color', self.TITLE_COLOR)
        self.SHADOW_BG_COLOR = kwargs.get('shadow_bg_color', self.SHADOW_BG_COLOR)
        self.TITLE_FONT = kwargs.get('title_font', self.TITLE_FONT)
        self.style.configure('Help.TFrame', background=self.BG_COLOR)
        self.style.configure('Shadow.TFrame', background=self.SHADOW_BG_COLOR)
        self.style.configure('Help.TLabel', background=self.BG_COLOR,
                         foreground=self.TITLE_COLOR)
        self.style.configure('HelpText.TLabel', background=self.BG_COLOR)

    def _bind_help(self, event=None):
        self.bind("<F1>", self._show_help)

    def _unbind_help(self, event=None):
        self.unbind("<F1>")

    def _show_help(self, event=None):
        print(f"showing: {self.help_title}")
        if self.help_frame and self.help_frame.winfo_exists():
            self._destroy()
        self._show_help_frame()
        self.master.bind_all("<Button-1>", self._click_outside)

    def _show_help_frame(self):
        self.root.update_idletasks()
        self.root.update()
        widget_x = absolute_x(self)
        widget_y = absolute_y(self)
        widget_width = self.winfo_width()
        widget_height = self.winfo_height()
        available_width = max(200, widget_width)  # Ensure a minimum width for the help frame
        available_width = 200

        print(f"widget_x: {widget_x}, widget_y: {widget_y}, widget_width: {widget_width}, widget_height: {widget_height}")

        bg_color = self.BG_COLOR

        # Create main help frame
        self.help_frame = ttk.Frame(self.root, border=1,
                                    relief="raised", padding=4)
        help_frame_x = min(widget_x, self.root.winfo_width() - available_width)
        help_frame_y = min(widget_y + widget_height + 5, self.root.winfo_height() - self.help_frame.winfo_height())
        self.help_frame.place(x=help_frame_x, y=help_frame_y, width=available_width)

        title_label = ttkb.Label(self.help_frame, text=self.help_title
                                , anchor="w", font=self.TITLE_FONT,
                                 bootstyle="primary")
        title_label.pack(fill="x", padx=5, pady=(5, 0))

        text_label = ttk.Label(self.help_frame,
                               text=self.help_text,
                               wraplength=available_width, justify="left")
        text_label.pack(fill="x", padx=5, pady=5)

        self.update_idletasks()  # Ensure geometry is up-to-date again
        help_frame_height = self.help_frame.winfo_height()

        # Create shadow frame after help frame is fully laid out
        self.shadow_frame = ttk.Frame(self.root, style='Shadow.TFrame',
                                    relief="flat")
        self.shadow_frame.place(x=help_frame_x + 5,
                                y=help_frame_y + 5,
                                width=available_width+5,
                                height=help_frame_height)

        print(f"Help frame created at ({help_frame_x}, {help_frame_y})")
        print(f"Shadow frame created at ({widget_x + 5}, {widget_y + widget_height + 10})")

        def ensure_visibility():
            self.help_frame.lift()
            print(f"Help frame width: {self.help_frame.winfo_width()}, height: {self.help_frame.winfo_height()}")
            print(f"Shadow frame width: {self.shadow_frame.winfo_width()}, height: {self.shadow_frame.winfo_height()}")
            print(f"Help frame visible at ({absolute_x(self.help_frame)}, {absolute_y(self.help_frame)})")

        self.master.after_idle(ensure_visibility)

    def _click_outside(self, event):
        # Check if the click was outside the help frame
        if self.help_frame and self.help_frame.winfo_exists():
            x1 = self.help_frame.winfo_rootx()
            y1 = self.help_frame.winfo_rooty()
            x2 = x1 + self.help_frame.winfo_width()
            y2 = y1 + self.help_frame.winfo_height()
            if not (x1 <= event.x_root <= x2 and y1 <= event.y_root <= y2):
                self._destroy()
                if self.shadow_frame and self.shadow_frame.winfo_exists():
                    self.shadow_frame.destroy()
                self.master.unbind_all("<Button-1>")

    def _destroy(self):
        self.help_frame.destroy()
        self.shadow_frame.destroy()


class HelpableEntry(Helpable, tk.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)


class HelpableCombobox(Helpable, ttk.Combobox):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)


class ExampleUse(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        # Pack
        id_location_frame = tk.Frame(self)
        id_location_frame.pack(fill='x', padx=(10, 0), pady=10)

        self.id_location = Label(id_location_frame, text="If data are identidies subjects or Profiles and Frequencies, where in record 1 are the id label/frequencies located? (columns from-to)", wraplength=400, bg=Helpable.BG_COLOR)
        self.id_location.pack(side=tk.LEFT, padx=(0, 30))

        id_location_right = tk.Frame(id_location_frame)
        id_location_right.pack(side=tk.RIGHT, padx=(0, 100))

        from_label = Label(id_location_right, text="From", bg=Helpable.BG_COLOR)
        from_label.pack(side=tk.LEFT, padx=(0, 5))

        self.id_location_from_entry = HelpableEntry(id_location_right, width=5, help_title="ID Location From", help_text="Enter the starting column for ID location.")
        self.id_location_from_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.id_location_from_entry.insert(0, "0")

        self.test_entry = HelpableEntry(self, help_title="Test Help", help_text="Enter your test here.")
        self.test_entry.pack()

        to_label = Label(id_location_right, text="To", bg=Helpable.BG_COLOR)
        to_label.pack(side=tk.LEFT, padx=(0, 5))

        self.id_location_to_entry = HelpableEntry(id_location_right, width=5, help_title="ID Location To", help_text="Enter the ending column for ID location.")
        self.id_location_to_entry.pack(side=tk.LEFT)
        self.id_location_to_entry.insert(0, "0")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Complex Example with Helpable Widgets")
    Helpable.init(root)
    root.geometry("600x400")

    main_app = ExampleUse(root)
    main_app.pack(fill='both', expand=True)
    root.mainloop()
