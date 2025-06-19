import os
import ttkbootstrap as ttk
import tkinter as tk
from lib.__version__ import VERSION
from lib.gui.windows.window import Window
from lib.utils import get_resource
from lib.help.help_window.screens import ScreensGenerator
from lib.help.help_window.style import *
from lib.utils import *



# Help Contents
s_CONTENTS = 'contents'
TABLE_PRE_PAD = " " * 3


class HelpWindow(Window):
    def __init__(self, parent, section=None, **kwargs):
        """
        graph_data: list of dictionaries containing the data to be plotted
        should contain "x", "y", "annotations", "title", "legend",
         "captions", "geom" keys
        """
        super().__init__(**kwargs, geometry=DEFAULT_GEOMETRY)


    def setup_window(self, section=None, **kwargs):
        """Initialize the help window."""
        self.title(f"POSAC For Windows ({VERSION}) Help")
        self.iconbitmap(get_resource("icons/help.ico"))
        # sets the geometry of toplevel
        self.center_window()
        # set the content
        self.col_width = DEFAULT_COL_WIDTH
        # History
        self.history = []
        self.history_index = 0
        # init
        self.init_menu()
        self.init_main_frame()
        # Bind key presses to the respective methods
        self.bind("<BackSpace>", lambda x: None)
        self.bind("<Right>", lambda x: self.next_section())
        self.bind("<BackSpace>", lambda x: self.back_section())
        self.bind("<Left>", lambda x: self.back_section())
        self.bind("<Escape>", lambda x: self.exit())
        #
        section = section if section else s_CONTENTS
        self.screen_generator = ScreensGenerator(self)
        self.start_on(section)
        # self.showcase_fonts()

    def center_window(self):
        self.update_idletasks()  # Update "requested size" from geometry manager
        # Calculate x and y coordinates for the Tk root window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = (screen_width / 2) - (size[0] / 2)
        y = 0
        self.geometry("+%d+%d" % (x, y))

    def start_on(self, section_name):
        self.history.append(section_name)
        self.switch_to_section(section_name)

    def init_main_frame(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Create text widget with enhanced styling
        self.text_widget = tk.Text(
            self.main_frame,
            bd=0,
            wrap='word',
            borderwidth=0,
            highlightthickness=0,
            bg=BACKGROUND,
            font=text_font,
            spacing1=3,      # Space before paragraphs
            spacing2=2,      # Space between lines in same paragraph
            spacing3=5,      # Space after paragraphs
            padx=15,
            pady=10
        )

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar FIRST so it can claim its required width
        scrollbar.pack(side="right", fill="y")
        self.text_widget.pack(side="left", expand=True, fill='both')

        # Configure enhanced text styles
        self.text_widget.tag_config(H1, font=h1_font, foreground=H1_FOREGROUND, spacing3=3)
        self.text_widget.tag_config(H2, font=h2_font, foreground=H2_FOREGROUND, spacing1=2, spacing3=3)
        self.text_widget.tag_config(TEXT, font=text_font, foreground=TXT_FOREGROUND, spacing3=3)
        self.text_widget.tag_config(TEXT_SMALL, font=text_small_font, foreground=TXT_FOREGROUND)
        self.text_widget.tag_config(TEXT_BOLD, font=text_bold_font, foreground=TXT_FOREGROUND)
        self.text_widget.tag_config(TEXT_STRONG, font=text_strong_font, foreground=STRONG_FOREGROUND)
        self.text_widget.tag_config(ROW_LEFT, font=row_left_font, foreground=ROW_LEFT_FOREGROUND)
        self.text_widget.tag_config(ROW_RIGHT, font=row_right_font, foreground=ROW_RIGHT_FOREGROUND)

    def init_menu(self):
        self.menu = tk.Menu(self)
        self.menu.add_command(label="Contents", command=lambda:
        self.process_click(LINK_PREFIX + s_CONTENTS))
        self.menu.add_command(label="Back", command=self.back_section)
        self.menu.add_command(label="Next", command=self.next_section)
        self.menu.add_command(label="Exit", command=self.exit)
        self.config(menu=self.menu)

    def next_section(self):
        if self.history_index == len(self.history) - 1:
            return
        else:
            self.history_index += 1
            self.switch_to_section(self.history[self.history_index])

    def back_section(self):
        if self.history_index == 0:
            return
        else:
            self.history_index -= 1
            self.switch_to_section(self.history[self.history_index])

    #######

    def on_click(self, event):
        # Get the index of the mouse click
        index = self.text_widget.index(f"@{event.x},{event.y}")
        # Check if the click was on a tagged word
        for tag in self.text_widget.tag_names(index):
            if tag.startswith(LINK_PREFIX):
                print(f"You clicked on the entry: {tag}")
                self.process_click(tag)
                break

    def process_click(self, tag):
        # Here you can define what to do for each entry
        dest = tag[len(LINK_PREFIX):]
        # Navigation
        if dest == self.history[self.history_index]: return
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        self.history_index += 1
        self.history.append(dest)
        # Switch page
        self.switch_to_section(dest)

    def on_enter(self, event):
        self.text_widget.config(cursor="hand2")

    def on_leave(self, event):
        self.text_widget.config(cursor="")

    def exit(self):
        self.destroy()

    #####################

    def add_link(self, txt, tag):
        link_tag = f'clickable_{tag}'
        self.text_widget.insert('end', txt, link_tag)

    def add_txt(self, txt, tag='text'):
        self.text_widget.insert('end', txt, tag)

    def add_strong(self, txt):
        """Add strong (bold) text"""
        self.text_widget.insert('end', txt, TEXT_STRONG)

    def add_paragraph(self, txt, tag='text'):
        self.text_widget.insert('end', txt + "\n", tag)

    def add_heading(self, txt, tag='h1'):
        if tag == H1:
            self.text_widget.insert('end', txt + "\n", tag)
        else:
            self.text_widget.insert('end', "\n" + txt + "\n", tag)

    def add_line_break(self):
        self.text_widget.insert('end', "\n")

    def add_row(self, left, right, left_link=None, offset=0):
        """Enhanced row rendering with better formatting"""
        # Add some padding
        self.add_txt("  ")

        # Add left column (label) with special formatting
        if left_link:
            self.add_link(left, left_link)
        else:
            self.add_txt(left, ROW_LEFT)

        # Calculate padding for alignment
        base_padding = 25  # Base padding for alignment
        left_length = len(left)
        padding_needed = max(3, base_padding - left_length + offset)
        padding = " " * padding_needed

        self.add_txt(padding)
        self.add_txt(right + "\n", ROW_RIGHT)

    def add_bullet(self, txt):
        """Add bullet point text"""
        self.text_widget.insert('end', "  • ", TEXT)  # Use safe bullet character
        self.text_widget.insert('end', txt, TEXT)

    def switch_to_section(self, section_name):
        if self.history_index < len(self.history) - 1:
            self.menu.entryconfig("Next", state="normal")
        else:
            self.menu.entryconfig("Next", state="disabled")
        if self.history_index > 0:
            self.menu.entryconfig("Back", state="normal")
        else:
            self.menu.entryconfig("Back", state="disabled")
        print(self.history, self.history_index)
        #
        self.text_widget.config(state='normal')
        self.text_widget.delete('1.0', 'end')
        self.screen_generator.section(section_name)
        self.text_widget.config(state='disabled')
        self.bind_links()

    def bind_links(self):
        for tag in self.text_widget.tag_names():
            if tag.startswith("clickable_"):
                self.text_widget.tag_config(tag, font=link_font, foreground=LINK_FOREGROUND)
                self.text_widget.tag_bind(tag, '<Button-1>', self.on_click)
                self.text_widget.tag_bind(tag, '<Enter>', self.on_enter)
                self.text_widget.tag_bind(tag, '<Leave>', self.on_leave)

    ##########################
