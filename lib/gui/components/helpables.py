import tkinter as tk
from tkinter import Label, Frame
from abc import ABC
from tkinter import ttk
from typing import Callable
import ttkbootstrap as ttkb

from lib.utils import real_size, rreal_size

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
    def init(cls, root, fallback_help : Callable=None):
        cls.root = root
        cls.style = ttkb.Style()
        cls.style.configure('Shadow.TFrame',
                            background=cls.SHADOW_BG_COLOR)
        cls.fallback_help = fallback_help

    def __init__(self, help_title="",
                 help_text="",
                 help : dict = None,
                 **kwargs):
        if not self.root:
            raise UserWarning("Helpable.init(root) must be called before creating any Helpable widgets.")
        self.title_font = self.TITLE_FONT
        self.help_title = help_title
        self.help_text = help_text
        if help:
            self.help_title = help['help_title']
            self.help_text = help['help_text']
        self.help_frame = None
        self.shadow_frame = None
        super().__init__(**kwargs)

        # Directly bind F1 to the widget/frame
        self.bind("<F1>", self._show_help)

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

    def _show_help(self, event=None):
        if not self.help_title and not self.help_text:
            print("no help title or text, using fallback help")
            self.fallback_help()
            return
        print(f"showing: {self.help_title}")
        if self.help_frame and self.help_frame.winfo_exists():
            self._destroy()
        self._show_help_frame()
        self.master.bind_all("<Button-1>", self._click_outside)
        self.master.bind_all("<Escape>", self._close_help)

    def _close_help(self, event=None):
        """Close help window and clean up bindings"""
        if self.help_frame and self.help_frame.winfo_exists():
            self._destroy()
            self.master.unbind_all("<Button-1>")
            self.master.unbind_all("<Escape>")

    def _show_help_frame(self):
        # Get the toplevel window that contains this widget
        toplevel = self.winfo_toplevel()

        toplevel.update_idletasks()
        toplevel.update()
        widget_x = absolute_x(self)
        widget_y = absolute_y(self)
        widget_width = self.winfo_width()
        widget_height = self.winfo_height()

        # Fixed reasonable width with real_size adjustments
        available_width = rreal_size(300)
        max_height = rreal_size(300)  # Maximum height before adding scrollbar
        padding = real_size(4)
        shadow_offset = real_size(5)

        # Create main help frame on the correct toplevel window
        self.help_frame = ttk.Frame(toplevel, border=1,
                                  relief="raised", padding=padding)

        # Create a canvas with scrollbar for the content
        canvas = tk.Canvas(self.help_frame,
                         width=available_width-rreal_size(20),
                         highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.help_frame, orient="vertical",
                                command=canvas.yview)
        content_frame = ttk.Frame(canvas)

        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add the title and text to the content frame
        title_label = ttkb.Label(content_frame, text=self.help_title,
                              anchor="w", font=self.TITLE_FONT,
                              bootstyle="primary")
        title_label.pack(fill="x", padx=real_size(5),
                        pady=(real_size(5), 0))

        text_label = ttk.Label(content_frame,
                             text=self.help_text,
                             wraplength=available_width - rreal_size(30),
                             justify="left")
        text_label.pack(fill="x", padx=real_size(5),
                       pady=real_size(5))

        # Create window for the content frame
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Update geometry and add scrollbar if needed
        content_frame.update_idletasks()
        content_height = content_frame.winfo_reqheight()
        canvas_height = min(content_height, max_height)

        canvas.configure(height=canvas_height)
        canvas.configure(scrollregion=canvas.bbox("all"))

        # Pack the canvas and scrollbar if needed
        canvas.pack(side="left", fill="both", expand=True)
        needs_scrollbar = content_height > max_height
        if needs_scrollbar:
            scrollbar.pack(side="right", fill="y")

        # Position the help frame - use toplevel dimensions
        help_frame_x = min(widget_x, toplevel.winfo_width() - available_width - rreal_size(10))
        help_frame_y = widget_y + widget_height + shadow_offset

        # Adjust y position if too close to bottom
        if help_frame_y + canvas_height > toplevel.winfo_height():
            help_frame_y = max(rreal_size(10), widget_y - canvas_height - shadow_offset)

        self.help_frame.place(x=help_frame_x, y=help_frame_y)

        # Create shadow frame with adjusted width for non-scrollbar case
        shadow_width = available_width + shadow_offset
        if not needs_scrollbar:
            shadow_width -= shadow_offset  # Reduce shadow width when no scrollbar

        # Create shadow frame on the correct toplevel window
        self.shadow_frame = ttk.Frame(toplevel, style='Shadow.TFrame',
                                    relief="flat")
        self.shadow_frame.place(x=help_frame_x + shadow_offset,
                              y=help_frame_y + shadow_offset,
                              width=shadow_width,
                              height=canvas_height)

        # Ensure help frame stays on top
        self.help_frame.lift()

        # Add mouse wheel binding with smooth scrolling
        def _on_mousewheel(event):
            delta = -1 * (event.delta / 120)
            canvas.yview_scroll(int(delta), "units")

        # Add keyboard navigation
        def _on_key(event):
            if event.keysym == "Up":
                canvas.yview_scroll(-1, "units")
            elif event.keysym == "Down":
                canvas.yview_scroll(1, "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Up>", _on_key)
        canvas.bind_all("<Down>", _on_key)

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


class HelpableFrame(tk.Frame, Helpable):
    def __init__(self, master=None, help_title="Help Title", help_text="Help Text", help=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        Helpable.__init__(self, help_title=help_title, help_text=help_text, help=help)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Complex Example with Helpable Widgets")
    Helpable.init(root)
    root.geometry("600x400")

    main_app = ExampleUse(root)
    main_app.pack(fill='both', expand=True)
    root.mainloop()
