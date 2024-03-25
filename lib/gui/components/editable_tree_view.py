from __future__ import annotations

import tkinter
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from lib.utils import get_resource
import ttkbootstrap as ttkb

class EditableTreeView(ttk.Treeview):
    def __init__(self, master=None, add_check_box=False,
                 auto_index=True, index=True, index_col_name="Index",
                 sub_index_col=1,
                 **kw):
        super().__init__(master, **kw)
        if not index:
            add_check_box = False
            self["show"] = "headings"
        self._configure_columns(index_col_name=index_col_name, **kw)
        self._configure_style()
        self._indices = [0] if auto_index else []
        self._auto_index = auto_index
        self._cur_focus = None
        self._cur_focus_col = None
        self._entry_popup = None
        self._init_scrollbars(master)
        #
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

    def _configure_style(self):
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
                        padding=(10, 0, 0, 0),
                        # Padding: (left, top, right, bottom)
                        )
        style.configure("Treeview",
                        rowheight=21)  # Adjust the row height as needed
        self.tag_configure('oddrow', background='#F8F5F0')
        self.tag_configure('evenrow', background='white')

    def _configure_columns(self, **kw):
        cols = list(kw.get("columns", []))
        index_col_name = kw.get("index_col_name")
        self.heading("#0", text=index_col_name)
        self.column("#0", width=70, anchor='w', stretch=False)
        for col in cols:
            self.heading(col, text=col, anchor="w")
            self.column(col, width=50, anchor='w')
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
        checkbox_off_image = Image.open(get_resource("checkbox_off.png"))
        checkbox_off_image = checkbox_off_image.resize((15, 15), Image.LANCZOS)
        self._checkbox_off_image = ImageTk.PhotoImage(checkbox_off_image)
        checkbox_on_image = Image.open(get_resource("checkbox_on.png"))
        checkbox_on_image = checkbox_on_image.resize((15, 15), Image.LANCZOS)
        self._checkbox_on_image = ImageTk.PhotoImage(checkbox_on_image)
        self.insert = self._insert_with_checkbox

    def _on_check_click(self, event):
        row_id = self.identify_row(event.y)
        column_id = self.identify_column(event.x)
        # If the click is on the checkbox column and on a valid row
        if column_id == '#0' and row_id:
            # Toggle the checkbox state
            self._checkboxes_states[row_id] = not self._checkboxes_states.get(
                row_id, False)
            image = self._checkbox_on_image if self._checkboxes_states[
                row_id] else self._checkbox_off_image
            # Update the checkbox image
            self.item(row_id, image=image)
            self._reset_sub_index()

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
        if 'text' in kw:
            kw['text'] = "  " + kw['text']
        values = kw['values'] if kw['values'] else ['']*len(self._col_names)
        self._sub_index += 1
        values[self._sub_index_col] = str(self._sub_index)
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
                                self._cur_focus_v_col,
                                self._entry_popup)
            self._cur_focus = None
            self._cur_focus_col = None

    def _on_double_click(self, event):
        row_id = self.identify_row(event.y)
        # get visible column_id
        column_id = self.identify_column(event.x)
        visible_column_name = self._display_columns[int(column_id[
                                                       1:])-1]

        # Set focus and select the row
        self.selection_set(row_id)
        self._cur_focus = row_id
        self._cur_focus_col = column_id
        self._cur_focus_v_col = self._col_names.index(visible_column_name)
        self._cur_focus_v_col_name = visible_column_name

        # Enter edit mode
        self._enter_edit_mode(row_id, column_id)


    def _enter_edit_mode(self, item_id, column_id):
        if self._cur_focus_col in [f"#{i}" for i in self._indices]:
            return
        # get the column alignment
        aligns = dict(w = 'left', c = 'center', e = 'right')
        align = aligns[self.column(column_id)['anchor']]
        self._entry_popup = tk.Entry(self, justify=align)
        self._entry_popup.insert(0, self.set(item_id)[
            self._cur_focus_v_col_name])
        self._entry_popup.select_range(0, tk.END)
        self._entry_popup.bind("<Return>", lambda e: self._on_return(item_id,
                                                                     column_id,
                                                                     self._entry_popup))
        self._entry_popup.bind("<KP_Enter>", lambda e: self._on_return(item_id,
                                                                       column_id,
                                                                       self._entry_popup))
        self._entry_popup.bind("<Escape>",
                               lambda e: self._entry_popup.destroy())
        self._entry_popup.bind("<FocusOut>",
                               lambda e: self._entry_popup.destroy(
                               ))  # Destroy the popup when focus is lost
        x, y, width, height = self.bbox(item_id, column_id)
        self._entry_popup.place(x=x, y=y, anchor="nw", width=width)

    def _on_return(self, item_id, column_id, entry_widget):
        self.set(item_id, column_id, entry_widget.get())
        entry_widget.destroy()
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
        insert_row_above_img = Image.open(get_resource("insert_row_above.png"))
        insert_row_above_img = insert_row_above_img.resize((15, 15),
                                                           Image.LANCZOS)
        self.insert_row_above_img = ImageTk.PhotoImage(insert_row_above_img)
        insert_row_below_img = Image.open(get_resource("insert_row_below.png"))
        insert_row_below_img = insert_row_below_img.resize((15, 15),
                                                           Image.LANCZOS)
        self.insert_row_below_img = ImageTk.PhotoImage(insert_row_below_img)
        delete_row_img = Image.open(get_resource("delete_row.png"))
        delete_row_img = delete_row_img.resize((15, 15), Image.LANCZOS)
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
            raise IndexError(f"Row index {row} out of range {len(self.get_children()) - 1}")
        return self.item(self.get_children()[int(row)]).get('values', [])

    def get_row(self, row):
        if row < 0 :
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
        return [self.set(iid) for iid in self.get_children() if self._checkboxes_states.get(iid, True)]

    # def set(self, row_id, column=None, value=None):
    #     if isinstance(column, str):
    #         column = self._col_names.index(column)
    #     if column and value:
    #         self.item(row_id, values=(self.item(row_id, "values")[:column] +
    #                                   [value] +
    #                                   self.item(row_id, "values")[column + 1:]))
    #     return self.item(row_id, "values")

    def row_ids(self):
        for iid in self.get_children():
            yield iid

    def get_all_values(self):
        return [self.item(iid, "values") for iid in self.get_children()]

    def to_df(self):
        import pandas as pd
        return pd.DataFrame(self.get_all_values(), columns=self['columns'])

    def set_row(self, index, values):
        iid = self.get_children()[index]
        self.item(iid, values=values)

    #####################
    # Add/Remove/Insert #
    #####################
    def _reindex(self):
        """ reindex the treeview """
        for i, iid in enumerate(self.get_children()):
            text = str(i + 1)
            if len(self._indices) == 2: text = "  " + text
            self.item(iid, text=text)
            self.item(iid, tags="oddrow" if i % 2 == 0 else "evenrow")
        if len(self._indices) == 2:
            self._reset_sub_index()

    def remove_row(self, row_index=None):
        """ get the rows id from the row_index and remove it from the
        treeview """
        row_id = self.get_children()[row_index]
        self.delete(row_id)
        if self._auto_index:
            self._reindex()

    def insert_row(self, index, values=[]):
        """ add a row to the treeview """
        if index == -1:
            index = 'end'
        iid = self.insert('', index, text="", values=values,
                          tags = "oddrow" if index % 2 == 0 else "evenrow")
        if self._auto_index:
            self._reindex()
        return iid

    def add_row(self, values):
        """ add a row to the treeview """
        index = len(self.get_children()) + 1
        iid = self.insert('', 'end', text=str(index), values=values,
                          tags = "oddrow" if index % 2 == 0 else "evenrow")
        return iid

    #####################
    # Show/Hide Columns #
    #####################

    def hide_column(self, identifier):
        if isinstance(identifier, int):
            col_name = self._col_names[identifier]
        else:
            col_name = identifier
        self._display_columns.remove(col_name)
        self["displaycolumns"] = self._display_columns

    def show_column(self, col_name=None, index=None):
        if not col_name and not index: raise ValueError("Either col_name or "
                                                        "index must be "
                                                        "provided")
        if index:
            col_name = self._col_names[index]
        if col_name not in self._display_columns:
            self._display_columns.append(col_name)
        self["displaycolumns"] = self._display_columns


if __name__ == '__main__':
    # Setup root window
    root = tk.Tk()
    root.geometry("600x400")
    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True, padx=30, pady=30)

    cols = ("Sel_Var", "Rec_N", "Field_Width",
            "Start_Col", "Label")

    # Treeview table
    tree = EditableTreeView(main_frame,
                            add_check_box=True,
                            index=True,
                            index_col_name="Var_No",
                            columns=cols,
                            displaycolumns="#all",
                            selectmode="browse")

    for i in range(1, 1):
        iid = tree.add_row(values=(f"v{i}", i, 1, 0, f"Label {i}"))  # Set the
        # initial checkbox image

    def callback():
        tree.add_row(["v1", "TEST", "TEST", "TEST", "TEST","123","123"])

    tree.pack(side="left", fill="both", expand=False)
    action_button = tk.Button(root, text="Remove Row", pady=10,
                              background="white",
                              command=callback)
    action_button.pack()
    # print(tree.loc(3))
    # tree.remove_row(0)
    print(len(tree))
    root.mainloop()
""
