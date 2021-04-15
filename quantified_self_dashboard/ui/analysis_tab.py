import wx
import wx.adv


class AnalysisTab(wx.Panel):

    def __init__(self, parent, callback_wrapper):
        self.__display_name = "Analysis"
        self.__callback_wrapper = callback_wrapper
        wx.Panel.__init__(self, parent)

        top_sizer = wx.BoxSizer(wx.VERTICAL)

        self.calendar_heading_sizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=300)
        self.calendar_sizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=20)

        self.__prepare_calendar()
        self.__prepare_choice_and_submission()

        top_sizer.Add(self.calendar_heading_sizer, 0, 0)
        top_sizer.Add(self.calendar_sizer, 0, wx.EXPAND)

        top_sizer.SetSizeHints(self)
        self.SetSizer(top_sizer)




    
    def __prepare_calendar(self):

        # headings    
        start_text_field = wx.StaticText(self, -1, "Start")
        end_text_field = wx.StaticText(self, -1, "End")

        self.calendar_heading_sizer.Add(start_text_field)
        self.calendar_heading_sizer.Add(end_text_field)

        # calendars themselves
        starting_year, starting_month, starting_day = map(int, self.__callback_wrapper.get_starting_date().split('-'))
        starting_datetime = wx.DateTime(year=starting_year, month=starting_month, day=starting_day)
        self.__current_start_date = starting_datetime
        self.__current_end_date = wx.DateTime().Today()

        self.start_cal = wx.adv.GenericCalendarCtrl(self, -1, self.__current_start_date, style = wx.adv.CAL_MONDAY_FIRST)
        self.start_cal.Bind(wx.adv.EVT_CALENDAR_MONTH,           self.on_change_sel_start_date)
        self.start_cal.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED,     self.on_change_month_start_date)

        self.end_cal = wx.adv.GenericCalendarCtrl(self, -1, self.__current_end_date, style = wx.adv.CAL_MONDAY_FIRST)
        self.end_cal.Bind(wx.adv.EVT_CALENDAR_MONTH,           self.on_change_sel_end_date)
        self.end_cal.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED,     self.on_change_month_end_date)

        self.calendar_sizer.Add(self.start_cal)
        self.calendar_sizer.Add(self.end_cal)

        self.__highlight_available_month_days_start_cal()
        self.__highlight_available_month_days_end_cal()


    def __prepare_choice_and_submission(self):
        

        # self.analyse_btn = wx.Button(self, -1, "Analyse")
        # self.analyse_btn.Bind(wx.EVT_BUTTON, self.on_analyse_btn_click)
        pass



    def on_change_sel_start_date(self, evt):
        self.__current_start_date = evt.GetDate()

    def on_change_sel_end_date(self, evt):
        self.__current_end_date = evt.GetDate()

    def on_change_month_start_date(self, evt):
        self.__current_start_date = evt.GetDate()
        self.__highlight_available_month_days_start_cal()

    def on_change_month_end_date(self, evt):
        self.__current_end_date = evt.GetDate()
        self.__highlight_available_month_days_end_cal()
    
    def __highlight_available_month_days_start_cal(self):
        for i in range(1, 32):
            self.start_cal.ResetAttr(i)

        date = self.start_cal.GetDate()
        self.__current_start_year = date.GetYear()
        self.__current_start_month = date.GetMonth() + 1

        for date_str in self.__callback_wrapper.get_available_dates():
            year, month, day = map(int, date_str.split('-'))
            if month == self.__current_start_month and year == self.__current_start_year:
                self.start_cal.SetHoliday(day)
    
    def __highlight_available_month_days_end_cal(self):
        for i in range(1, 32):
            self.end_cal.ResetAttr(i)

        date = self.end_cal.GetDate()
        self.__current_end_year = date.GetYear()
        self.__current_end_month = date.GetMonth() + 1

        for date_str in self.__callback_wrapper.get_available_dates():
            year, month, day = map(int, date_str.split('-'))
            if month == self.__current_end_month and year == self.__current_end_year:
                self.end_cal.SetHoliday(day)


    @property
    def display_name(self):
        return self.__display_name

    def on_analyse_btn_click(self):
        pass
