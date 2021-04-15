import wx
from ui.main_tab import MainTab
from ui.subjective_input_tab import SubjectiveInputTab
from ui.analysis_tab import AnalysisTab
from ui.callback_wrappers import *

class MainFrame(wx.Frame):

    def __init__(self, subjective_input_callback_wrapper, main_tab_callback_wrapper, analysis_tab_callbak_wrapperr):
        wx.Frame.__init__(self, None, title="Quantified-Self Dashboard")

        self.panel = wx.Panel(self)
        self.nb = wx.Notebook(self.panel)

        # tabs
        main_tab = MainTab(self.nb, main_tab_callback_wrapper)
        subjective_input_tab = SubjectiveInputTab(self.nb, subjective_input_callback_wrapper)
        analysis_tab = AnalysisTab(self.nb, analysis_tab_callbak_wrapperr)

        self.nb.AddPage(subjective_input_tab, subjective_input_tab.display_name)
        self.nb.AddPage(main_tab, main_tab.display_name)
        self.nb.AddPage(analysis_tab, analysis_tab.display_name)

        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)

        best_nb_width, best_nb_height = self.nb.GetBestSize()
        best_panel_width, best_panel_height = self.panel.GetBestSize()

        best_width = max(best_nb_width, best_panel_width)
        best_height = max(best_nb_height, best_panel_height)

        self.SetSize((best_width * 2, best_height * 1.25))
        self.SetSize((500, 500))


