import wx


class AnalysisTab(wx.Panel):

    def __init__(self, parent):
        self.__display_name = "Analysis"
        wx.Panel.__init__(self, parent)
        wx.StaticText(self, -1, self.__display_name, (0, 0))

    @property
    def display_name(self):
        return self.__display_name

