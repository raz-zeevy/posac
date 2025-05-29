import logging
import subprocess
import warnings
from pathlib import Path

from lib.controller.graph_generator import generate_graphs, generate_posacsep_graphs
from lib.controller.session import Session
from lib.controller.sessions_history import SessionsHistory
from lib.controller.validator import Validator
from lib.gui.gui import GUI
from lib.posac.posac_module import PosacModule
from lib.utils import (
    IS_PROD,
    P_POSACSEP_TABLE_PATH,
    POSAC_SEP_PATH,
    DataLoadingException,
)

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self):
        # Setup logging
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        self.gui = GUI(self)
        self.notebook = self.gui.notebook
        self.history = SessionsHistory(callback=self.update_history)

        # Initialize error reporter
        # self.error_reporter = ErrorReporter.get_instance(self.gui, self)
        # # Install Tkinter exception handler
        # install_tk_exception_handler(self.gui.root)
        self.bind()
        self.restart_session()
        self.gui.navigator.prev_page()

    def bind(self):
        #
        self.gui.menu.view_menu.entryconfig(
            "POSAC/LSA Diagrams", command=self.show_diagram_window
        )
        # Run
        self.gui.navigation.button_run.config(command=self.run_posac)
        self.gui.icon_menu.m_button_run.config(command=self.run_posac)
        # Add Escape key binding
        self.gui.root.bind("<Escape>", lambda e: self.on_close())
        # Save
        self.gui.menu.file_menu.entryconfig("Save", command=self.show_save_session)
        self.gui.icon_menu.m_button_save.configure(command=self.show_save_session)
        self.gui.menu.file_menu.entryconfig(
            "Save As..", command=self.show_save_as_session
        )
        # Open
        self.gui.icon_menu.m_button_open.configure(command=self.show_open_session)
        self.gui.menu.file_menu.entryconfig("Open", command=self.show_open_session)
        # New
        self.gui.icon_menu.m_button_new.configure(
            command=lambda: self.show_save_changes_dialogue(
                callback=self.restart_session
            )
        )
        self.gui.menu.file_menu.entryconfig(
            "New",
            command=lambda: self.show_save_changes_dialogue(
                callback=self.restart_session
            ),
        )
        # Data file
        self.bind_submenu(
            self.gui.menu.data_file_menu,
            file=None,
            file_getter=self.notebook.general_tab.get_data_file,
            excel=True,
        )
        # Undo
        self.gui.icon_menu.m_button_undo.configure(command=self.gui.notebook.undo)
        # Redo
        self.gui.icon_menu.m_button_redo.configure(command=self.gui.notebook.redo)
        # Help (work that on click it sends the key F1 event as if the user pressed F1)
        self.gui.icon_menu.m_button_help.configure(
            command=lambda: self.gui.root.event_generate("<KeyPress-F1>")
        )
        self.gui.menu.help_menu.entryconfig(
            "About Posac", command=self.gui.show_about_window
        )
        self.gui.menu.help_menu.entryconfig(
            "Report Error", command=self.report_manual_error
        )
        # Exit
        self.gui.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.gui.notebook.output_files_tab.exit_button.config(command=self.on_close)
        self.gui.start_page.exit_button.config(command=self.on_close)
        # Override the default showwarning method with your custom one
        if IS_PROD():
            warnings.showwarning = self.custom_show_warning

    def run_process(self):
        try:
            self.gui.run_process()
        except Exception as e:
            if IS_PROD():
                self.gui.show_warning("Error", f"An error occurred: {e}")
            else:
                raise e

    ##############
    # Controller #
    # State      #
    ##############

    def get_state(self):
        return {"controller": {"save_path": self.save_path}}

    def load_state(self, state: dict):
        self.update_save_path(state["controller"]["save_path"])

    def reset_state(self):
        self.update_save_path("")

    def update_save_path(self, path):
        self.save_path = path
        self.gui.set_save_title(self.save_path)

    ##############
    # Save Load  #
    # & New      #
    ##############

    def update_history(self):
        """
        this function gets at most 4 last sessions path's and updates
        the menu under file section with the paths and bind them with load_path
        :return:
        """
        paths = self.history.get_n(4)
        self.gui.menu.update_history_menu(paths)
        # Bind each path to the corresponding menu item using its index
        menu_start_index = (
            self.gui.menu.file_menu.index("end") - len(paths) + 1
        )  # Start index of the new paths
        for i, path in enumerate(paths):
            self.gui.menu.file_menu.entryconfig(
                menu_start_index + i, command=lambda p=path: self.load_session(p)
            )

    def restart_session(self):
        Session.reset(self)
        self.update_history()

    def save_session(self, path):
        session = Session(self)
        self.history.add(str(path))
        session.save(path)

    def load_session(self, path):
        self.history.add(path)
        session = Session(path=path)
        session.load(self)

    ##############
    # Open Files
    # & Windows  #
    ##############

    def open_file(self, file, notepad=False, word=False, excel=False, file_getter=None):
        if file_getter:
            file = file_getter()
        if not file:
            self.gui.show_warning("error", "Please specify a file to open.")
            return
        try:
            if notepad:
                subprocess.run(["notepad", file], check=True)
            elif word:
                subprocess.run(["start", "winword", file], shell=True, check=True)
            elif excel:
                subprocess.run(["start", "excel", file], shell=True, check=True)
            else:
                raise UserWarning("Please specify a program to open the file with")
        except FileNotFoundError:
            self.gui.show_warning(
                "error", f"Unable to open {file}. Application not found."
            )
        except subprocess.CalledProcessError as e:
            self.gui.show_warning("error", f"Failed to open {file}: {e}")

    def show_diagram_window(self):
        logger.debug("Attempting to show diagram window")
        graph_data_lst = generate_graphs(self)
        logger.debug(f"Generated {len(graph_data_lst)} graphs")
        self.gui.show_diagram_window(graph_data_lst)
        logger.debug("Diagram window displayed")

    def show_posacsep_diagram_window(self, item):
        graph_data_lst = generate_posacsep_graphs(self, item)
        self.gui.show_diagram_window(graph_data_lst)

    def show_save_session(self):
        if not self.save_path:
            self.show_save_as_session()
        else:
            self.save_session(self.save_path)

    def show_save_as_session(self):
        default_file_name = Path(self.gui.notebook.general_tab.get_data_file()).stem
        save_file = self.gui.save_session_dialogue(default_file_name)
        if save_file:
            self.update_save_path(save_file)
            self.save_session(save_file)

    def show_save_session_and_callback(self, callback):
        self.show_save_session()
        callback()

    def show_save_changes_dialogue(self, callback):
        self.gui.show_msg(
            "Would you like to save your current session before starting a new one?",
            title="Save Session?",
            yes_command=lambda: self.show_save_session_and_callback(callback),
            no_command=callback,
        )

    def show_open_session(self):
        session_file = self.gui.open_session_dialogue()
        if session_file:
            try:
                self.load_session(session_file)
            except Exception as e:
                if IS_PROD():
                    self.gui.show_warning(
                        "error", f"Failed to open session file {session_file}"
                    )
                else:
                    raise e

    def custom_show_warning(
        self, message, category, filename, lineno, file=None, line=None
    ):
        # Convert the warning message to a string and display it using your GUI
        warning_msg = f"{message}"
        # Assuming you have a GUI instance available as `self.gui`
        self.gui.show_warning("Warning", warning_msg)

    def on_close(self):
        # Prompt the user with a message box
        if IS_PROD():
            result = self.gui.show_msg(
                "Do you want to save the current session before exiting?",
                title="Exit",
                yes_command=self.show_save_session,
                buttons=["Yes:primary", "No:secondary", "Cancel:secondary"],
            )
            if result == "Yes":
                self.show_save_session()
                self.gui.root.destroy()  # Close the application after saving
            elif result == "No":
                self.gui.root.destroy()  # Close the application without saving
            else:
                pass  # Do nothing (cancel the close operation)
        else:
            self.gui.root.destroy()

    ################
    # Enable Views #
    ################

    def bind_submenu(self, menu, file, excel=False, file_getter=None):
        menu.entryconfig(
            "Notepad",
            command=lambda: self.open_file(file, notepad=True, file_getter=file_getter),
        )
        menu.entryconfig(
            "Word",
            command=lambda: self.open_file(file, word=True, file_getter=file_getter),
        )
        if "Excel" in [
            menu.entrycget(i, "label") for i in range(menu.index("end") + 1)
        ]:
            menu.entryconfig(
                "Excel",
                command=lambda: self.open_file(
                    file, excel=True, file_getter=file_getter
                ),
            )

    def enable_view_output(self):
        self.bind_submenu(self.gui.menu.posac_output_menu, file=self.pos_out)
        self.bind_submenu(self.gui.menu.lsa1_output_menu, file=self.ls1_out)
        self.bind_submenu(self.gui.menu.lsa2_output_menu, file=self.ls2_out)
        self.bind_submenu(
            self.gui.menu.posacsep_table_menu, file=self.posacsep_table_path
        )
        self.bind_submenu(self.gui.menu.posac_axes_menu, file=self.posac_axes_out)
        posac_axes = self.gui.get_technical_options("posac_axes") == "Yes"
        if posac_axes:
            self.bind_submenu(self.gui.menu.posacsep_table_menu, file=POSAC_SEP_PATH)
        self.gui.menu.add_posacsep_items(self.int_vars_num)
        for i in range(1, self.int_vars_num + 1):
            self.gui.menu.posacsep.entryconfig(
                f"Item {i}",
                command=lambda i=i: self.show_posacsep_diagram_window(i),
            )
        self.gui.enable_view_results(posac_axes)

    ###################
    # POSAC execution #
    ###################

    def _update_properties_from_gui(self):
        self.data_file = self.notebook.general_tab.get_data_file()
        self.job_name = self.notebook.general_tab.get_job_name()
        self.int_vars_num = self.notebook.internal_variables_tab.get_vars_num()
        self.lines_per_case = self.notebook.general_tab.get_lines_per_case()
        self.recoding_operations = self.notebook.internal_recoding_tab.get_operations()
        ext_vars_num = self.notebook.external_variables_tab.get_vars_num()
        self.num_variables = self.int_vars_num + ext_vars_num
        st = self.notebook.general_tab.get_subject_type()
        self.idata = 0 if st == "S" else 1
        self.lowfreq = self.notebook.general_tab.get_only_freq()
        self.missing = 0  # todo: self.notebook.general_tab.get_subject_type()
        self.ipower = 1  # todo:
        """
        C                IF IPOWER=0 OR BLANK POWER OF THE BALANCING
C                  WEIGHTS ARE : ND1=4 FOR INCOMPARABLES
C                          ND2=4 FOR   COMPARABLES
C                IF IPOWER.NE.0  ND1 AND ND2 HAVE TO BE
C                          SPECIFIED (SEE LINE E. BELOW)
        """
        #### 6
        self.itemdplt = int(self.notebook.general_tab.get_plot_item_diagram())
        self.nlab = self.num_variables
        self.nxt = ext_vars_num
        self.map_ = self.notebook.get_external_traits_num()
        self.iextdiag = int(self.notebook.general_tab.get_plot_external_diagram())
        # 11
        self.itable = int(self.notebook.general_tab.get_posac_type() == "P")
        # 12
        self.initx = 0
        # related to initx
        self.init_approx_format = None
        self.init_approx = None
        self.boxstring = None
        # todo: fix all of them
        """
        C                IF INITX=0 OR BLANK  FIRST APPROXIMATION
C                        COMPUTED BY THE PROGRAM
C                IF INITX.NE.0  FIRST APPROXIMATION GIVEN
C                         BY THE USER  (SEE LINE I. BELOW)

        """
        # technical options and posac-axes
        self.iboxstrng = 0
        self.iff = 0
        self.form_feed = None
        self.itrm = self.gui.get_technical_options("max_iterations")
        self.iwrtfls = 0
        self.ifshmr = self.gui.get_technical_options("posac_axes") == "Yes"
        self.shemor_directives_key = self.gui.get_technical_options("set_selection")
        self.record_length = self.gui.get_technical_options("record_length")
        self.ifrqone = 0
        self.posac_axes_out = self.gui.get_technical_options("posac_axes_out")
        # C
        vars = self.notebook.internal_variables_tab.get_all_variables_values()
        vars.extend(
            [int(var[0]) + self.int_vars_num] + list(var[1:])
            for var in self.notebook.external_variables_tab.get_all_variables_values()
        )
        self.variables_details = [
            dict(index=var[0], line=var[1], width=var[2], col=var[3], label=var[4])
            for var in vars
        ]
        # todo: fix
        self.min_category = 0
        self.max_category = 0
        self.nd1 = self.gui.get_technical_options("power_weights_low")
        self.nd2 = self.gui.get_technical_options("power_weights_high")
        # External Variables Ranges
        self.ext_var_ranges = (
            self.notebook.external_variables_ranges_tab.get_all_ranges_values()
        )
        # Traits
        self.traits = self.notebook.traits_tab.get_traits_values()
        # output
        self.pos_out = self.notebook.output_files_tab.get_posac_out()
        self.ls1_out = self.notebook.output_files_tab.get_lsa1_out()
        self.ls2_out = self.notebook.output_files_tab.get_lsa2_out()
        self.posacsep_table_path = P_POSACSEP_TABLE_PATH
        # posacsep
        self.posacsep = self.notebook.posacsep_tab.get_values()

    def run_posac(self):
        # Validate before running
        validation_errors = Validator.validate_for_run(self)

        if validation_errors:
            error_message = "Please fix the following errors:\n\n"
            error_message += "\n".join(f"• {error}" for error in validation_errors)
            self.gui.show_warning("Validation Error", error_message)
            return

        # Continue with existing run code
        self._update_properties_from_gui()
        posac = PosacModule()
        try:
            posac.create_files(
                data_file=self.data_file,
                lines_per_var=self.lines_per_case,
                recoding_operations=self.recoding_operations,
                job_name=self.job_name,
                num_variables=self.num_variables,
                idata=self.idata,
                lowfreq=self.lowfreq,
                missing=self.missing,
                ipower=self.ipower,
                itemdplt=self.itemdplt,
                nlab=self.nlab,
                nxt=self.nxt,
                map_=self.map_,
                iextdiag=self.iextdiag,
                itable=self.itable,
                initx=self.initx,
                iboxstrng=self.iboxstrng,
                iff=self.iff,
                itrm=self.itrm,
                iwrtfls=self.iwrtfls,
                ifshmr=self.ifshmr,
                ifrqone=self.ifrqone,
                variables_details=self.variables_details,
                min_category=self.min_category,
                max_category=self.max_category,
                nd1=self.nd1,
                nd2=self.nd2,
                ext_var_ranges=self.ext_var_ranges,
                traits=self.traits,
                init_approx_format=self.init_approx_format,
                init_approx=self.init_approx,
                boxstring=self.boxstring,
                form_feed=self.form_feed,
                shemor_directives_key=self.shemor_directives_key,
                record_length=self.record_length,
            )
        except DataLoadingException as e:
            if IS_PROD():
                self.gui.show_warning("Data Loading Error", str(e))
                return
            else:
                raise e
        except Exception as e:
            if IS_PROD():
                self.gui.show_warning("Posac Error", str(e))
                return
            else:
                raise e
        try:
            technical_options = self.gui.get_technical_options()
            if technical_options["posac_axes"] == "Yes":
                # The .pax file path is passed as the last parameter
                posac_axes_out = technical_options["posac_axes_out"]
                # ... run SSHEMOR with posac_axes_out as %6
            else:
                posac_axes_out = ""
            posac.run(
                self.pos_out,
                self.ls1_out,
                self.ls2_out,
                self.posacsep,
                posac_axes_out=posac_axes_out,
            )
            self.gui.show_msg(
                "POSAC analysis completed successfully!\n Press View in menu to see results",
                title="POSAC",
            )
        except Exception as e:
            self.gui.show_msg(
                f"An error occurred during POSAC analysis: {e}", title="Error"
            )
            return
        self.enable_view_output()

    def report_manual_error(self):
        """Allow users to manually report an issue"""
        from tkinter import messagebox

        # Ask for confirmation
        confirm = messagebox.askquestion(
            "Report Issue",
            "This will create an error report with the current application state.\n\n"
            "Use this to report issues that don't cause the application to crash.\n\n"
            "Would you like to continue?",
            icon="warning",
        )

        if confirm == "yes":
            # Create a manual error report
            exception_info = {
                "type": "ManualReport",
                "message": "User-initiated error report",
                "traceback": "No traceback available - this is a manual report.",
            }

            # Use the error reporter to generate the report
            self.error_reporter.report_error(exception_info)

            # Show confirmation
            messagebox.showinfo(
                "Report Submitted",
                "Thank you for your report. You can continue using the application.",
                icon="info",
            )

if __name__ == '__main__':
    a = Controller()
    a.open_file(r"C:\Users\Raz_Z\Desktop\shmuel-project\shared\KEDDIR2.DAT",
                excel=True)
