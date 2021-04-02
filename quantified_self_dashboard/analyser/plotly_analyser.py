import os
import math
import datetime
from typing import List, Tuple, Union

import numpy as np
from collections import Counter
import plotly
import plotly.express as px

from summary.summary_container import SummaryContainer
from common.constants import *
from common.date_helper import all_date_strings_between_dates
from analyser.abstract_plotter import AbstractPlotter
from analyser.transform_measurements import *


class PlotlyAnalyser(AbstractPlotter):
    """
    Analysing SummaryContainer data by plotting, using the plotly library.
    """


    _supported_analysis_types = [AnalysisType.test, AnalysisType.scores_daily, AnalysisType.sleep_duration, AnalysisType.sleep_durations]


    def _analyse(self, start: str, end: str, periodicity: Periodicity, analysis_type: AnalysisType, *args):
        """
        Implementation of this analyser classes analysis.

        Parameters
        ----------
        start : str
            Analysis start date in YYYY-MM-DD format.

        end : str
            Analysis end date in YYYY-MM-DD format.

        periodicity : Periodicity
            Which timeframes must be considered, e.g. daily, weekly, monthyl, yearly.

        analysis_type : AnalysisType
            The chosen type of anayzis for this method call, must be part of the supported
            analysis types of this Analyser Class.
        """

        if analysis_type == AnalysisType.scores_daily:
            summary_type_measurement_tuples = [(SummaryType.sleep, "score"), (SummaryType.readiness, "score"), (SummaryType.activity, "score")]
            title = "Daily Scores"
            output_file_name = "daily_scores_{}_{}".format(start, end)
            self.__line_plot_multiple_of_same_unit(start, end, Periodicity.daily, summary_type_measurement_tuples, title=title, output_file_name=output_file_name, yaxis_to_zero=True)


        elif analysis_type == AnalysisType.sleep_duration:
            summary_type_measurement_tuples = [(SummaryType.sleep, "total"), (SummaryType.sleep, "duration")]
            title = "Total Sleep Time"
            output_file_name = "daily_sleep_total_time_{}_{}".format(start, end)
            self.__line_plot_multiple_of_same_unit(start, end, Periodicity.daily, summary_type_measurement_tuples, title=title, output_file_name=output_file_name)


        elif analysis_type == AnalysisType.sleep_durations:
            summary_type_measurement_tuples = [(SummaryType.sleep, "total"), (SummaryType.sleep, "deep"), (SummaryType.sleep, "rem"), (SummaryType.sleep, "light")]
            title = "Total Sleep Time"
            output_file_name = "daily_sleep_times_{}_{}".format(start, end)
            self.__line_plot_multiple_of_same_unit(start, end, Periodicity.daily, summary_type_measurement_tuples, title=title, output_file_name=output_file_name, yaxis_to_zero=True)


    def __line_plot_multiple_of_same_unit(self, start: str, end: str, periodicity: Periodicity, summary_type_measurement_tuples: List[Tuple[str, str]], **kwargs):
        """
        Plotting one or multiple lines in one plot. 
        The different measurements should preferably have the same
        unit to not screw the scale of the axis.

        Parameters
        ----------
        start : str
            Analysis start date in YYYY-MM-DD format.

        end : str
            Analysis end date in YYYY-MM-DD format.

        periodicity : Periodicity
            Which timeframes must be considered, e.g. daily, weekly, monthyl, yearly.

        summary_type_measurement_tuples : List[Tuple[str, str]]
            List of Tuples, where each tuple represents the summary type and 
            measurement name which will get plotted.    

        **kwargs:
            Additional keyword arguments.
            
            title : str
                Title of the plot.
            
            output_file_name : str
                Name of the output file.

            yaxis_to_zero : bool
                If set to true, the y-axis will always start from zero.
        """
        
        dates, plot_data_sets, plot_legends, plot_units = self._get_plot_data_sets(start, end, periodicity, summary_type_measurement_tuples)

        # check if each plot data has same unit, otherwise the scale might get screwd
        if len(Counter(plot_units).keys()) > 1:
            raise ValueError("Different Units")
        unit_as_text = UnitsAnnotationText[plot_units[0]]

        # setting title
        if 'title' in kwargs.keys():
            title = kwargs['title']
        else:
            title = "Line Plot"

        # drawing plotly figure
        fig = px.line(x=dates, y=plot_data_sets, title=title, labels={'x': 'Dates', 'value': unit_as_text})

        if plot_units[0] == Unit.time_of_day:
            fig.update_yaxes(type="date")

        fig.update_xaxes(constraintoward="left")

        # setting y-axis start to zero
        if 'yaxis_to_zero' in kwargs.keys():
            tozero_val = kwargs['yaxis_to_zero']
            if tozero_val:
                fig.update_yaxes(rangemode='tozero')

        # setting the legend to identify the different lines
        for i, legend_name in enumerate(plot_legends):
            fig['data'][i]['name'] = legend_name

        # saving the plot as an image
        if 'output_file_name' in kwargs.keys():
            output_file_name = kwargs['output_file_name']
        else:
            output_file_name = "temp"
        self.__save(fig, output_file_name)


    def __save(self, fig, file_name):
        """ Saving the plotly figure as an image into the given output file name. """
        path_name = "{}.png".format(os.path.join(self._output_location, file_name))
        fig.write_image(path_name)




