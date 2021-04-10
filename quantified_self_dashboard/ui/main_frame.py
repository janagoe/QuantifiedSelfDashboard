import wx
from ui.main_tab import MainTab
from ui.subjective_input_tab import SubjectiveInputTab
from ui.analysis_tab import AnalysisTab

class MainFrame(wx.Frame):

    def __init__(self, subjective_input_callback_wrapper):
        wx.Frame.__init__(self, None, title="Quantified-Self Dashboard", size=(500, 500))

        p = wx.Panel(self)
        self.nb = wx.Notebook(p)

        # tabs
        main_tab = MainTab(self.nb)
        subjective_input_tab = SubjectiveInputTab(self.nb, subjective_input_callback_wrapper)
        analysis_tab = AnalysisTab(self.nb)

        self.nb.AddPage(subjective_input_tab, subjective_input_tab.display_name)
        self.nb.AddPage(main_tab, main_tab.display_name)
        self.nb.AddPage(analysis_tab, analysis_tab.display_name)

        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
