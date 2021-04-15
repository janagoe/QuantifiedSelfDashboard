import wx

class MainTab(wx.Panel):

    def __init__(self, parent, callback_wrapper):
        self.__display_name = "Main"
        self.__callback_wrapper = callback_wrapper

        wx.Panel.__init__(self, parent)

        self.save_btn = wx.Button(self, -1, "Save Changes")
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save_btn_click)

    @property
    def display_name(self):
        return self.__display_name
    
    def on_save_btn_click(self, event):
        self.__callback_wrapper.save_session()