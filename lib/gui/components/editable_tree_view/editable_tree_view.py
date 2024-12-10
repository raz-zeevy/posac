from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from .utils.utils import rreal_size, real_size

p_CHECKBOX_ON = "assets/checkbox_on.png"

p_CHECKBOX_OFF = "assets/checkbox_off.png"

p_DELETE_ROW_IMG = "assets/delete_row.png"

"""
It's not possible in the current impolemention to have checkbox without index
that's why the method set_index() is for.
"""

# Default Paths
p_INSERT_ROW_BELOW_IMG = "assets/insert_row_below.png"
p_INSERT_ROW_ABOVE_IMG = "assets/insert_row_above.png"
#

def get_image(path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(current_dir, path)
    return Image.open(img_path)

class EditableTreeView(ttk.Treeview):
    # Style Constants
    CHECK_BOX_SIZE = (15, 15)
    CELL_RIGHT_PADDING = 5
    ROW_HEIGHT = 20

    def __init__(self, master=None, add_check_box=False,
                 disable_sub_menu = False,
                 disable_cols_edit = [],
                 auto_index=True, index=True, index_col_name="Index",
                 sub_index_col=1,
                 cell_right_padding=CELL_RIGHT_PADDING,
                 row_height=ROW_HEIGHT,
                 check_box_size=CHECK_BOX_SIZE,
                 check_box_callback: callable = None,
                 validation_callback : callable = None,
                 **kw):
        """

        :param master:
        :param add_check_box:
        :param auto_index:
        :param index:
        :param index_col_name:
        :param sub_index_col:
        :param cell_right_padding:
        :param row_height:
        :param check_box_size:
        :param validation_callback (callable): foo(value, col_index,
        row_values) -> bool
        :param kw:
        """
        kw['columns'] = list(kw.get("columns", []))
        super().__init__(master, **kw)
        if not index:
            add_check_box = False
            self["show"] = "headings"
        self._configure_columns(index_col_name=index_col_name, **kw)
        self._configure_style(cell_right_padding=cell_right_padding,
                              row_height=row_height,
                              check_box_size=check_box_size)
        self._indices = [0] if auto_index else []
        self._auto_index = auto_index
        self._cur_focus = None
        self._cur_focus_col = None
        self._entry_popup = None
        self._checkbox_mode = add_check_box
        self._init_scrollbars(master)
        self.disable_cols_edit = disable_cols_edit
        self.validation_callback = validation_callback
        self.check_box_callback = check_box_callback
        #
        if not disable_sub_menu:
            self.bind("<Button-3>",
                      self._on_right_click)  # Button-3 is the right-click button
        self._build_context_menu()
        # Load the unchecked checkbox image
        if add_check_box:
            self._init_checkbox(sub_index_col)
        # Bindings
        self.bind("<Double-1>", self._on_double_click)
        self.bind("<Button-1>", self._on_click)

    ############
    # Built-in #
    ############

    def __len__(self):
        return len(self.get_children())

    def _configure_style(self,
                         cell_right_padding=CELL_RIGHT_PADDING,
                         row_height=ROW_HEIGHT,
                         check_box_size=CHECK_BOX_SIZE):
        style = ttk.Style()
        # style.configure("Treeview", foreground='black',background="#ffc61e")
        # style.theme_use('classic')
        style.map("Treeview.Heading",
                  background=[('pressed', '!focus', '#D9EBF9'),
                              ('active', '#BCDCF4'),
                              ('!disabled', '#325D88')
                              ],
                  foreground=[('pressed', '!focus', 'black'),
                              ('active', 'black'),
                              ('!disabled', 'white')
                              ])
        style.map('Treeview', background=[('selected', '#0078D7')], )
        style.map('Treeview', background=[('selected', '#8E8C84')], )
        # Configure Treeview Heading style for border and padding
        style.configure("Treeview.Heading",
                        # background="white",
                        # foreground="white",
                        bordercolor="black",
                        borderwidth=1,
                        padding=(rreal_size(cell_right_padding), rreal_size(3), 0, rreal_size(3)),
                        # Padding: (left, top, right, bottom)
                        )
        style.configure("Treeview",
                        rowheight=rreal_size(row_height),  # Adjust the row height as needed
                        )
        # style.configure("Treeview.Cell",
        #                 padding=(CELL_RIGHT_PADDING, 0, 0, 0),  # Adjust the row height as needed
        #                 )
        self.tag_configure('evenrow', background='#F8F5F0')
        self.tag_configure('oddrow', background='white')
        self.check_box_size = check_box_size

    def _configure_columns(self, **kw):
        cols = list(kw.get("columns", []))
        index_col_name = kw.get("index_col_name")
        self.heading("#0", text=index_col_name)
        self.column("#0", width=rreal_size(70), anchor='w', stretch=False)
        for col in cols:
            self.heading(col, text=col, anchor="w")
            self.column(col, width=60, anchor='w')
            self.column(col, stretch=False)
        self._display_columns = cols.copy()
        self._col_names = cols.copy()

    def _init_scrollbars(self, master):
        # Create the scrollbars within the master frame
        self._vsb = ttk.Scrollbar(master, orient="vertical",
                                  command=self.yview)
        self._hsb = ttk.Scrollbar(master, orient="horizontal",
                                  command=self.xview)

        self.configure(yscrollcommand=self._vsb.set,
                       xscrollcommand=self._hsb.set)
        # Position the scrollbars relative to the treeview
        self._vsb.pack(side="right", fill="y")
        self._hsb.pack(side="bottom", fill="x")
        # Bind the scrollbars to the treeview
        self.pack(side="left", fill="both", expand=True)
        self._vsb.place(in_=self, relx=1.0, rely=0, relheight=1.0, anchor='ne')
        self._hsb.place(in_=self, relx=0, rely=1.0, relwidth=1.0, anchor='sw')

    ############
    # Checkbox #
    ############

    def _init_checkbox(self, sub_index_col):
        self._sub_index_col = sub_index_col - 1
        if self._auto_index:
            self._indices.append(sub_index_col)
        self._sub_index = 0
        self._checkboxes_states = {}
        self.bind("<ButtonRelease-1>", self._on_check_click)
        self.bind("<Motion>", self._on_motion)
        checkbox_off_image = get_image(p_CHECKBOX_OFF)
        checkbox_off_image = checkbox_off_image.resize(rreal_size(self.CHECK_BOX_SIZE),
                                                       Image.LANCZOS)
        self._checkbox_off_image = ImageTk.PhotoImage(checkbox_off_image)
        checkbox_on_image = get_image(p_CHECKBOX_ON)
        checkbox_on_image = checkbox_on_image.resize(rreal_size(self.CHECK_BOX_SIZE),
                                                     Image.LANCZOS)
        self._checkbox_on_image = ImageTk.PhotoImage(checkbox_on_image)
        self.insert = self._insert_with_checkbox

    def _on_check_click(self, event):
        row_id = self.identify_row(event.y)
        column_id = self.identify_column(event.x)
        # If the click is on the checkbox column and on a valid row
        if column_id == '#0' and row_id:
            # Toggle the checkbox state
            self._toggle_checkbox(row_id)

    def _toggle_checkbox(self, row_id):
        self._checkboxes_states[row_id] = not self._checkboxes_states.get(
            row_id, False)
        image = self._checkbox_on_image if self._checkboxes_states[
            row_id] else self._checkbox_off_image
        # Update the checkbox image
        self.item(row_id, image=image)
        self._reset_sub_index()
        if self.check_box_callback:
            self.check_box_callback(row_id, self._checkboxes_states[row_id])

    def _reset_sub_index(self):
        index = 0
        for i, iid in enumerate(self.get_children()):
            values = list(self.item(iid, "values"))
            if self._checkboxes_states.get(iid, True):
                index += 1
                values[self._sub_index_col] = index
            else:
                values[self._sub_index_col] = ""
            self.item(iid, values=values)
        self._sub_index = index

    def _on_motion(self, event):
        region = self.identify_region(event.x, event.y)
        if region == "tree":
            column_id = self.identify_column(event.x)
            if column_id == '#0':
                self.master.config(cursor="hand2")
            else:
                self.master.config(cursor="")
        else:
            self.master.config(cursor="")

    def _insert_with_checkbox(self, parent, index, iid=None, **kw):
        """
        insert a row on checkbox mode. The first column governs the state of
        the checkbox
        :param parent:
        :param index:
        :param iid:
        :param kw:
        :return:
        """
        if 'text' in kw:
            kw['text'] = "  " + kw['text']
        values = kw['values'] if kw['values'] else [''] * len(self._col_names)
        self._sub_index += 1
        values.insert(self._sub_index_col, str(self._sub_index))
        kw['values'] = values
        kw['image'] = self._checkbox_on_image
        iid = super().insert(parent, index, iid, **kw)
        self._checkboxes_states[iid] = True  # Set the initial checkbox state
        return iid

    ############
    # Handlers #
    ############

    def _on_click(self, event):
        row_id = self.identify_row(event.y)
        column_id = self.identify_column(event.x)

        # Clear focus if clicking on a different row or column
        if row_id != self._cur_focus or column_id != self._cur_focus_col:
            if self._entry_popup:
                self._on_return(self._cur_focus,
                                f"#{self._cur_focus_v_col+1}",
                                self._entry_popup)
            self._cur_focus = None
            self._cur_focus_col = None

    def _on_double_click(self, event):
        row_id = self.identify_row(event.y)
        if not row_id: return
        # Destroy the former entry popup if it exists. crucial to avoid
        # multiple entry popups that can occur because of
        # tkinter lagging
        if self._entry_popup:
            self._entry_popup.destroy()
        # get visible column_id
        column_id = self.identify_column(event.x)
        if self.col_num(column_id) in self.disable_cols_edit:
            return
        visible_column_name = self._display_columns[int(column_id[
                                                        1:]) - 1]

        # Set focus and select the row
        self.selection_set(row_id)
        self._cur_focus = row_id
        self._cur_focus_col = column_id
        self._cur_focus_v_col = self._col_names.index(visible_column_name)
        self._cur_focus_v_col_name = visible_column_name

        # Enter edit mode
        self._enter_edit_mode(row_id, column_id)

    def _enter_edit_mode(self, item_id, column_id):
        """Enter edit mode for a cell in the treeview.
        
        This method creates a popup entry widget for editing the cell's value.
        It handles all event bindings and ensures validation happens exactly once
        per edit operation.
        
        Args:
            item_id: The ID of the row being edited
            column_id: The ID of the column being edited
        """
        if self._cur_focus_col in [f"#{i}" for i in self._indices]:
            return
        
        # Configure entry widget
        aligns = dict(w='left', c='center', e='right')
        align = aligns[self.column(column_id)['anchor']]
        self._entry_popup = tk.Entry(self, justify=align)
        self._entry_popup.insert(0, self.set(item_id)[self._cur_focus_v_col_name])
        self._entry_popup.select_range(0, tk.END)
        self._entry_popup.focus_set()
        
        # Add flag to prevent multiple validations for a single edit
        self._validating = False
        
        def handle_edit(event=None):
            """Handle edit completion from any event (Return, FocusOut, etc.).
            
            Uses a flag to ensure validation only happens once, even if multiple
            events fire in quick succession (e.g., Return followed by FocusOut).
            """
            if not self._validating:
                self._validating = True
                self._on_return(item_id, column_id, self._entry_popup)
                self._validating = False
        
        # Bind all edit completion events to the same handler
        # This ensures consistent behavior regardless of how the edit is completed
        self._entry_popup.bind("<Return>", handle_edit)
        self._entry_popup.bind("<KP_Enter>", handle_edit)
        self._entry_popup.bind("<Escape>", lambda e: self._on_escape())
        self._entry_popup.bind("<FocusOut>", handle_edit)
        
        # Position the entry widget over the cell
        x, y, width, height = self.bbox(item_id, column_id)
        self._entry_popup.place(x=x, y=y, anchor="nw", width=rreal_size(width), height=rreal_size(height))
        
    def _on_return(self, item_id,
                   column_id,
                   entry_widget):
        """
        This function is called when the user hits the Enter key
        """
        if entry_widget:
            if self.validation_callback:
                valid = self.validation_callback(entry_widget.get(),
                                                 int(column_id[1:]),
                                                 list(self.set(item_id).values()))
                if not valid:
                    self._on_escape()
                    return
            self.set(item_id, column_id, entry_widget.get())
        self._on_escape()
        
    def _on_escape(self):
        if self._entry_popup:
            # Unbind all events before destroying to prevent double triggers
            self._entry_popup.unbind("<Return>")
            self._entry_popup.unbind("<KP_Enter>")
            self._entry_popup.unbind("<Escape>")
            self._entry_popup.unbind("<FocusOut>")
            self._entry_popup.destroy()
        self._entry_popup = None
        
    def _on_right_click(self, event):
        # Select row under mouse
        iid = self.identify_row(event.y)
        if iid:
            self.selection_set(iid)
            self.context_menu.post(event.x_root, event.y_root)

    ################
    # Context Menu #
    ################

    def _build_context_menu(self):
        insert_row_above_img = get_image(p_INSERT_ROW_ABOVE_IMG)
        insert_row_above_img = insert_row_above_img.resize((rreal_size(15), rreal_size(15)),
                                                           Image.LANCZOS)
        self.insert_row_above_img = ImageTk.PhotoImage(insert_row_above_img)
        insert_row_below_img = get_image(p_INSERT_ROW_BELOW_IMG)
        insert_row_below_img = insert_row_below_img.resize((rreal_size(15), rreal_size(15)),
                                                           Image.LANCZOS)
        self.insert_row_below_img = ImageTk.PhotoImage(insert_row_below_img)
        delete_row_img = get_image(p_DELETE_ROW_IMG)
        delete_row_img = delete_row_img.resize(rreal_size((15, 15)), Image.LANCZOS)
        self.delete_row_img = ImageTk.PhotoImage(delete_row_img)
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Insert Row Before",
                                      command=self._on_insert_row_before,
                                      image=self.insert_row_above_img,
                                      compound="left"
                                      )
        self.context_menu.add_command(label="Insert Row After",
                                      command=self._on_insert_row_after,
                                      image=self.insert_row_below_img,
                                      compound="left"
                                      )
        self.context_menu.add_command(label="Delete Row",
                                      command=self._on_delete_row,
                                      image=self.delete_row_img,
                                      compound="left"
                                      )

    def _on_insert_row_before(self):
        selected_item = self.selection()
        if selected_item:
            self.insert_row(int(self.index(selected_item)))

    def _on_insert_row_after(self):
        selected_item = self.selection()
        if selected_item:
            self.insert_row(int(self.index(selected_item) + 1))

    def _on_delete_row(self):
        selected_item = self.selection()
        if selected_item:
            self.remove_row(self.index(selected_item))

    #####################
    # Getters & Setters #
    #####################

    def loc(self, row):
        if not self.get_children() and row == -1:
            return []
        if row > len(self.get_children()) - 1:
            raise IndexError(
                f"Row index {row} out of range {len(self.get_children()) - 1}")
        return self.item(self.get_children()[int(row)]).get('values', [])

    def get_row(self, row):
        if row < 0:
            row = len(self) + row
        if row < 0 or row >= len(self):
            raise IndexError(f"Index {row} is out of range."
                             f"table length is {len(self)}.")
        return self.set(self.get_children()[row])

    def rows(self):
        for iid in self.get_children():
            yield self.set(iid)

    def checked_rows(self):
        for iid in self.get_children():
            if self._checkboxes_states.get(iid, True):
                yield self.set(iid)

    def get_checked_rows(self):
        return [self.set(iid) for iid in self.get_children() if
                self._checkboxes_states.get(iid, True)]
    def row_ids(self):
        for iid in self.get_children():
            yield iid

    def get_all_values(self):
        return [self.item(iid, "values") for iid in self.get_children()]

    def get_check_rows_values(self):
        return [self.item(iid, "values") for iid in self.get_children() if
                self._checkboxes_states.get(iid, True)]

    def get_check_rows_indices(self):
        return [i+1 for i, iid in enumerate(self.get_children()) if
         self._checkboxes_states.get(iid, True)]

    def to_df(self):
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("Pandas is not installed. Please install it "
                              "using pip install pandas")
        return pd.DataFrame(self.get_all_values(), columns=self['columns'])

    def set_row(self, index : int, values : list):
        if index < 0:
            index = len(self.get_children()) + index
        if index >= len(self.get_children()):
            raise IndexError(f"Index {index} is out of range. "
                             f"Table length is {len(self)}.")
        if len(values) != len(self._col_names):
            raise ValueError(
                f"Values length {len(values)} does not match the number of "
                f"columns {len(self._col_names)}")
        iid = self.get_children()[index]
        self.item(iid, values=values)

    #####################
    # Add/Remove/Insert #
    #####################
    def _reindex(self):
        """
        This method is used to reindex the treeview.
        - It iterates over all the children of the treeview.
        - Updates the text of each item with its index (1-based).
        - Sets the tag of each item to 'oddrow' or 'evenrow' based on its
            index for alternate row coloring.
        - If the treeview is configured with a checkbox column,
            it resets the sub-index of the checkboxes.
        """
        for i, iid in enumerate(self.get_children()):
            text = str(i + 1)
            if len(self._indices) == 2: text = "  " + text
            self.item(iid, text=text)
            self.item(iid, tags="oddrow" if (i+1) % 2 == 0 else "evenrow")
        if len(self._indices) == 2:
            self._reset_sub_index()

    def remove_row(self, row_index):
        """ get the rows id from the row_index and remove it from the
        treeview """
        if not self.get_children():
            return
        row_id = self.get_children()[row_index]
        self.delete(row_id)
        if self._auto_index:
            self._reindex()
        # removes the entry popup if its row is removed
        if self._entry_popup and self._cur_focus == row_id:
            self._on_escape()

    def insert_row(self, index, values=[]):
        """ add a row to the treeview """
        if index == -1:
            index = 'end'
        iid = self.insert('', index, text="", values=values,
                          tags="oddrow" if index % 2 == 0 else "evenrow")
        if self._auto_index:
            self._reindex()
        return iid

    def add_row(self, values = [], check=True):
        """ add a row to the treeview """
        index = len(self.get_children()) + 1
        iid = self.insert('', 'end', text=str(index), values=values,
                          tags="oddrow" if index % 2 == 0 else "evenrow")
        if not check and self._checkbox_mode:
            self._toggle_checkbox(iid)
        return iid

    def clear_rows(self):
        n = len(self.get_children())
        for _ in range(n):
            self.remove_row(-1)

    #####################
    # Show/Hide Columns #
    #####################

    def hide_column(self, identifier):
        if isinstance(identifier, int):
            col_name = self._col_names[identifier]
        else:
            col_name = identifier
        if col_name not in self._display_columns:
            return
        self._display_columns.remove(col_name)
        self["displaycolumns"] = self._display_columns

    def show_column(self, col_name=None, index=None):
        if not col_name and not index: raise ValueError("Either col_name or "
                                                        "index must be "
                                                        "provided")
        if index is not None:
            col_name = self._col_names[index]
        if col_name not in self._display_columns:
            col_i = self.get_col_display_i(col_name)
            self._display_columns.insert(col_i, col_name)
        self["displaycolumns"] = self._display_columns

    def get_col_display_i(self, col_name):
        col_i = self._col_names.index(col_name)
        for i, col in enumerate(self._display_columns):
            if self._col_names.index(col) > col_i:
                return i
        return -1

    ############
    # Checkbox #
    ############

    def toggle_checkbox(self, row_id):
        self._toggle_checkbox(row_id)

    #########
    # Utils #
    #########

    @staticmethod
    def col_num(col_id):
        """Returns the col number (0...n) from col_id"""
        return int(col_id[1:]) - 1

    #########
    # Style #
    #########

    @staticmethod
    def configure_style(check_box_size=CHECK_BOX_SIZE,
                        cell_right_padding=CELL_RIGHT_PADDING,
                        row_height=ROW_HEIGHT):
        EditableTreeView.ROW_HEIGHT = row_height
        EditableTreeView.CELL_RIGHT_PADDING = cell_right_padding
        EditableTreeView.CHECK_BOX_SIZE = check_box_size


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Editable Treeview")
    root.geometry("800x500")
    root.config(bg='white')

    tree = EditableTreeView(root, columns=["Name", "Family", "Age"],
                            show="headings", index_col_name="Index", index=True)
    tree.pack(fill="both", expand=True)
    tree.add_row(["John", "Doe", 30])
    tree.add_row(["John", "Doe", 30])
    tree.add_row(["John", "Doe", 30])
    tree.add_row(["John", "Doe", 30])
    tree.add_row(["John", "Doe", 30])
    root.mainloop()

