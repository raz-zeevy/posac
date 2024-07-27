class Navigator:
    def __init__(self, gui):
        self.gui = gui
        self.cur_page = 0
        self.notebook = self.gui.notebook
        self.navigation = self.gui.navigation
        self._bind()
        #
        self.max_page = len(self.gui.notebook.tabs()) - 1
        self.min_page = -1
        self.ex_vrs_tbs = [4, 5]

    def _bind(self):
        self.navigation.button_next.config(command=self.next_page)
        self.navigation.button_previous.config(command=self.prev_page)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_switch)
        self.gui.menu.entryconfig("Options",
                                           command=self.gui.show_options_window)
    def _update_buttons(self):
        if self.cur_page == self.min_page:
            self.navigation.button_previous.config(state="disabled")
        else:
            self.navigation.button_previous.config(state="normal")
        if self.cur_page == self.max_page:
            self.navigation.button_next.config(state="disabled")
        else:
            self.navigation.button_next.config(state="normal")

    def on_tab_switch(self, event):
        self.cur_page = self.notebook.index(self.notebook.select())
        self._update_buttons()

    def set_page(self, page):
        if page < self.min_page or page > self.max_page:
            return
        self.cur_page = page
        self.notebook.select(self.cur_page)

    def next_page(self):
        if self.cur_page == self.max_page:
            return
        if self.cur_page == self.ex_vrs_tbs[0] - 1 and \
                not self.notebook.exist_external_variables():
            self.cur_page += len(self.ex_vrs_tbs) + 1
        else:
            self.cur_page += 1
        self._update_buttons()
        self.notebook.select(self.cur_page)

    def prev_page(self):
        if self.cur_page == self.ex_vrs_tbs[-1] + 1 and \
                not self.notebook.exist_external_variables():
            self.cur_page -= len(self.ex_vrs_tbs) + 1
        else:
            self.cur_page -= 1
        self._update_buttons()
        if self.cur_page > self.min_page:
            self.notebook.select(self.cur_page)
        else:
            return
