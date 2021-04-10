import wx

class MainTab(wx.Panel):

    def __init__(self, parent):
        self.__display_name = "Main"

        wx.Panel.__init__(self, parent)

        self.load_btn = wx.Button(self, -1, "Load")
        self.load_btn.Bind(wx.EVT_BUTTON, self.on_load_btn_click)



    @property
    def display_name(self):
        return self.__display_name

    
    def on_load_btn_click(self, event):
        print("on_load_btn_click")
        