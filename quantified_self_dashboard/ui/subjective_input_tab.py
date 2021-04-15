import wx
import wx.adv

from common.constants import SubjectiveMeasurementType
from wx.lib.masked import NumCtrl

class SubjectiveInputTab(wx.Panel):

    def __init__(self, parent, subjective_input_callback_wrapper):
        self.__subjective_input_callback_wrapper = subjective_input_callback_wrapper
        self.__display_name = "Subjective Input"

        wx.Panel.__init__(self, parent)

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        self.input_grid_sizer = wx.GridSizer(rows=self.__subjective_input_callback_wrapper.get_number_of_needed_dynamic_input_rows(), cols=2, hgap=5, vgap=20)

        self.__prepare_calendar()
        self.__prepare_buttons()
        self.__prepare_input_fields()

        top_sizer.Add(self.cal, 0, )
        top_sizer.Add(self.select_btn, 0, 0)
        top_sizer.Add(self.input_grid_sizer, 0, wx.EXPAND)
        top_sizer.Add(self.save_btn, 0, 0)

        top_sizer.SetSizeHints(self)
        self.SetSizer(top_sizer)


    @property
    def display_name(self):
        return self.__display_name


    def __prepare_input_fields(self):

        self.__input_fields = dict()

        for name, input_type in self.__subjective_input_callback_wrapper.get_subjective_input_structure():
            
            # add name
            name_text_field = wx.StaticText(self, -1, name)
            self.input_grid_sizer.Add(name_text_field)

            # add input field
            if input_type == SubjectiveMeasurementType.bool:
                input_field = wx.CheckBox(self, -1)
            elif input_type == SubjectiveMeasurementType.percentage:
                input_field = NumCtrl(self, -1)
                input_field.SetBounds(min=0, max=100)
            elif input_type == SubjectiveMeasurementType.number:
                input_field = NumCtrl(self, -1)

            self.input_grid_sizer.Add(input_field)
            self.__input_fields[name] = (input_type, input_field)

        self.disable_input_fields()
    

    def __prepare_buttons(self):

        self.select_btn = wx.Button(self, -1, "Select Date")
        self.select_btn.Bind(wx.EVT_BUTTON, self.on_select_btn_click)
        
        self.save_btn = wx.Button(self, -1, "Save")
        self.save_btn.Bind(wx.EVT_BUTTON, self.on_save_btn_click)
        self.save_btn.Disable()


    def __prepare_calendar(self):
        
        self.cal = wx.adv.GenericCalendarCtrl(self, -1, wx.DateTime().Today(), style = wx.adv.CAL_MONDAY_FIRST)
        self.cal.Bind(wx.adv.EVT_CALENDAR_MONTH,           self.on_change_month)
        self.cal.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED,     self.on_cal_sel_changed)

        self.__missing_input_days = self.__subjective_input_callback_wrapper.get_missing_subjective_data_days()
        self.__highlight_month_days()


    def __highlight_month_days(self):

        for i in range(1, 32):
            self.cal.ResetAttr(i)

        date = self.cal.GetDate()
        self.__current_year = date.GetYear()
        self.__current_month = date.GetMonth() + 1

        for date_str in self.__missing_input_days:
            year, month, day = map(int, date_str.split('-'))
            if month == self.__current_month and year == self.__current_year:
                self.cal.SetHoliday(day)
            

    def on_change_month(self, evt):
        date = evt.GetDate()
        if date.GetMonth()+1 != self.__current_month or date.GetYear() != self.__current_year:
            self.__highlight_month_days()


    def on_cal_sel_changed(self, evt):
        date = evt.GetDate()
        if date.GetMonth()+1 != self.__current_month or date.GetYear() != self.__current_year:
            self.__highlight_month_days()


    def on_select_btn_click(self, evt):
        date = self.cal.GetDate()
        selected_year = date.GetYear()
        selected_month = date.GetMonth()+1
        selected_day = date.GetDay()

        selected_date_is_missing_input = False
        for date_str in self.__missing_input_days:
            year, month, day = map(int, date_str.split('-'))
            if year == selected_year and selected_month == selected_month and day == selected_day:
                selected_date_is_missing_input = True
                break

        if selected_date_is_missing_input:
            self.enable_input_fields()
            self.save_btn.Enable()


    def on_save_btn_click(self, evt):
        date = self.cal.GetDate()
        year, month, day = date.GetYear(), date.GetMonth()+1, date.GetDay()

        date_str = "{}-{:02d}-{:02d}".format(year, month, day)
        self.__missing_input_days.remove(date_str)
        self.__highlight_month_days()

        current_input_data = dict()
        for name, tupl in self.__input_fields.items():
            _, input_field = tupl
            value = input_field.GetValue()
            current_input_data[name] = value
        self.__subjective_input_callback_wrapper.add_subjective_input(date_str, current_input_data)

        self.disable_input_fields()
        self.save_btn.Disable()


    def enable_input_fields(self):
        for name, tupl in self.__input_fields.items():
            _, input_field = tupl
            input_field.Enable()

    def disable_input_fields(self):
        for name, tupl in self.__input_fields.items():
            input_type, input_field = tupl
            if input_type == SubjectiveMeasurementType.bool:
                input_field.SetValue(False)
            elif input_type == SubjectiveMeasurementType.percentage:
                input_field.SetValue(0)
            elif input_type == SubjectiveMeasurementType.number:
                input_field.SetValue(0)
            input_field.Disable()

