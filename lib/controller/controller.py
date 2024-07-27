from lib.gui.gui import GUI
from lib.posac.posac_module import PosacModule


class Controller:
    def __init__(self):
        self.gui = GUI()
        self.notebook = self.gui.notebook
        self.bind()

    def bind(self):
        self.gui.navigation.button_run.config(command=self.run_posac)

    def run_process(self):
        self.gui.run_process()

    def _update_properties_from_gui(self):
        self.job_name = self.notebook.general_tab.get_job_name()
        int_vars_num = self.notebook.internal_variables_tab.get_vars_num()
        ext_vars_num = self.notebook.external_variables_tab.get_vars_num()
        self.num_variables = int_vars_num + ext_vars_num
        st = self.notebook.general_tab.get_subject_type()
        self.idata = 0 if st == 'S' else 1
        self.lowfreq = self.notebook.general_tab.get_only_freq()
        self.missing = 0 #todo: self.notebook.general_tab.get_subject_type()
        self.ipower = 1 # todo:
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
        self.map_ = self.notebook.external_variables_ranges_tab.get_external_traits_num()
        self.iextdiag = int(self.notebook.general_tab.get_plot_external_diagram())
        # 11
        self.itable = int(self.notebook.general_tab.get_posac_type() == 'P')
        # 12
        self.initx = 0
        # related to initx
        self.init_approx_format = None;
        self.init_approx = None;
        self.boxstring = None
        # todo: fix all of them
        """
        C                IF INITX=0 OR BLANK  FIRST APPROXIMATION
C                        COMPUTED BY THE PROGRAM
C                IF INITX.NE.0  FIRST APPROXIMATION GIVEN
C                         BY THE USER  (SEE LINE I. BELOW)

        """
        # those ara the technical options
        self.iboxstrng = 0;self.iff = 0;self.form_feed = None;
        self.itrm = self.gui.get_technical_option('max_iterations')
        self.iwrtfls = 0; self.ifshmr = 0; self.shemor_directives=None;
        self.ifrqone = 0
        # C
        vars = self.notebook.internal_variables_tab.get_all_variables_values()
        vars.extend([int(var[0])+int_vars_num]+list(var[1:]) for var in
                    self.notebook.external_variables_tab
                    .get_all_variables_values())
        self.variables_details = [dict(index=var[0],
                                       line=var[1],
                                       width=var[2],
                                       col=var[3],
                                       label=var[4])
                                  for var in vars]
        # todo: fix
        self.min_category = 0
        self.max_category = 0
        self.nd1 = self.gui.get_technical_option('power_weights_low')
        self.nd2 = self.gui.get_technical_option('power_weights_high')
        self.ext_var_ranges = self.notebook.external_variables_ranges_tab.\
            get_all_ranges()
        self.traits = self.notebook.traits_tab.get_traits_values()
        # output
        self.pos_out = self.notebook.output_files_tab.get_posac_out()
        self.ls1_out = self.notebook.output_files_tab.get_lsa1_out()
        self.ls2_out = self.notebook.output_files_tab.get_lsa2_out()
    def run_posac(self):
        self._update_properties_from_gui()
        posac = PosacModule()
        posac.create_files(job_name=self.job_name,
                           num_variables=self.num_variables,
                           idata=self.idata, lowfreq=self.lowfreq,
                           missing=self.missing, ipower=self.ipower,
                           itemdplt=self.itemdplt, nlab=self.nlab,
                           nxt=self.nxt, map_=self.map_, iextdiag=self.iextdiag,
                           itable=self.itable, initx=self.initx,
                           iboxstrng=self.iboxstrng, iff=self.iff,
                           itrm=self.itrm,
                           iwrtfls=self.iwrtfls, ifshmr=self.ifshmr,
                           ifrqone=self.ifrqone,
                           variables_details=self.variables_details,
                           min_category=self.min_category,
                           max_category=self.max_category, nd1=self.nd1,
                           nd2=self.nd2,
                           ext_var_ranges=self.ext_var_ranges,
                           traits=self.traits,
                           init_approx_format=self.init_approx_format,
                           init_approx=self.init_approx,
                           boxstring=self.boxstring,
                           form_feed=self.form_feed,
                           shemor_directives=self.shemor_directives)
        posac.run(self.pos_out, self.ls1_out, self.ls2_out)


if __name__ == '__main__':
    a = Controller()
    a.run_process()
