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
        self.traits_tab_num = 5

    def _bind(self):
        self.navigation.button_next.config(command=self.next_tab_clicked)
        self.navigation.button_previous.config(command=self.prev_tab_clicked)
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
        # this is a hack to prevent the event from being called when not needed
        if self.cur_page == -1: return
        self.cur_page = self.notebook.index(self.notebook.select())
        self._update_buttons()

    def set_page(self, page):
        if page < self.min_page or page > self.max_page:
            return
        while self.cur_page != page:
            if self.cur_page < page:
                self.next_page()
            else:
                self.prev_page()

    def next_tab_clicked(self):
        # check if the user is on traits page and the current trait is not
        # the last trait:
        # next_trait
        # else:
        # next_page()
        if self.cur_page == self.traits_tab_num and \
                self.gui.notebook.traits_tab._current_trait < \
                len(self.gui.notebook.traits_tab._traits):
            self.gui.notebook.traits_tab.select_trait(
                self.gui.notebook.traits_tab._current_trait + 1)
        else:
            self.next_page()

    def prev_tab_clicked(self):
        # check if the user is on traits page and the current trait is not
        # the first trait:
        # prev_trait
        # else:
        # prev_page()
        if self.cur_page == self.traits_tab_num and \
                self.gui.notebook.traits_tab._current_trait > 1:
            self.gui.notebook.traits_tab.select_trait(
                self.gui.notebook.traits_tab._current_trait - 1)
        else:
            self.prev_page()


    def next_page(self):
        # if on traits page and
        if self.cur_page == self.max_page:
            return
        if self.cur_page == -1:
            self.show_notebook()
        if self.cur_page == self.ex_vrs_tbs[0] - 1 and \
                not self.notebook.exist_external_variables():
            self.cur_page += len(self.ex_vrs_tbs) + 1
        else:
            self.cur_page += 1
        self._update_buttons()
        self.notebook.select(self.cur_page)

    def prev_page(self):
        if self.cur_page == self.min_page:
            return
        if self.cur_page == self.ex_vrs_tbs[-1] + 1 and \
                not self.notebook.exist_external_variables():
            self.cur_page -= len(self.ex_vrs_tbs) + 1
        else:
            self.cur_page -= 1
        self._update_buttons()
        if self.cur_page > self.min_page:
            self.notebook.select(self.cur_page)
        else:
            self.show_first_page()

    def show_notebook(self):
        self.gui.start_page.pack_forget()
        self.gui.notebook_frame.pack(expand=True, fill='both', padx=30,
                                    pady=0, )

    def show_first_page(self):
        self.gui.notebook_frame.pack_forget()
        self.gui.start_page.pack(expand=True, fill='both')