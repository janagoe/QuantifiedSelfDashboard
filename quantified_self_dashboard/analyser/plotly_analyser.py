import os
import math
import datetime
from typing import List, Tuple, Union

import numpy as np
from collections import Counter
import plotly
import plotly.express as px
import plotly.graph_objects as go

from summary.summary_container import SummaryContainer
from common.constants import *
from common.date_helper import all_date_strings_between_dates
from analyser.abstract_plotter import AbstractPlotter
from analyser.transform_measurements import *


class PlotlyAnalyser(AbstractPlotter):
    """
    Analysing SummaryContainer data by plotting, using the plotly library.
    """

    _supported_analysis_types = [
        AnalysisType.scores_daily, 
        AnalysisType.sleep_durations, 
        AnalysisType.sleep_score_distribution,
        AnalysisType.readiness_score_distribution,
        AnalysisType.activity_score_distribution,
        AnalysisType.bedtimes_daily
    ]


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


        elif analysis_type == AnalysisType.sleep_durations:
            summary_type_measurement_tuples = [(SummaryType.sleep, "deep"), (SummaryType.sleep, "rem"), (SummaryType.sleep, "light"), (SummaryType.sleep, "awake")]
            title = "Sleep Times"
            output_file_name = "daily_sleep_times_{}_{}".format(start, end)
            self.__bar_plot_multiple_of_same_unit(start, end, Periodicity.daily, summary_type_measurement_tuples, title=title, output_file_name=output_file_name, yaxis_to_zero=True)


        elif analysis_type == AnalysisType.sleep_score_distribution:
            title = "Sleep Score Distribution from {} until {}".format(start, end)
            output_file_name = "sleep_score_distribution_{}_{}".format(start, end)
            self.__histogram_plot_multiple_of_same_unit(start, end, Periodicity.daily, [(SummaryType.sleep, "score")], title=title, output_file_name=output_file_name)


        elif analysis_type == AnalysisType.readiness_score_distribution:
            title = "Readiness Score Distribution from {} until {}".format(start, end)
            output_file_name = "readiness_score_distribution_{}_{}".format(start, end)
            self.__histogram_plot_multiple_of_same_unit(start, end, Periodicity.daily, [(SummaryType.readiness, "score")], title=title, output_file_name=output_file_name)


        elif analysis_type == AnalysisType.activity_score_distribution:
            title = "Activity Score Distribution from {} until {}".format(start, end)
            output_file_name = "activity_score_distribution_{}_{}".format(start, end)
            self.__histogram_plot_multiple_of_same_unit(start, end, Periodicity.daily, [(SummaryType.activity, "score")], title=title, output_file_name=output_file_name)


        elif analysis_type == AnalysisType.bedtimes_daily:
            title = "Daily Bedtimes from {} until {}".format(start, end)
            output_file_name = "daily_bedtimes_{}_{}".format(start, end)
            self.__bedtimes_plot(start, end, Periodicity.daily, [(SummaryType.sleep, "bedtime_start_delta"), (SummaryType.sleep, "duration")], title=title, output_file_name=output_file_name)


    def __save(self, fig, file_name):
        """ Saving the plotly figure as an image into the given output file name. """
        path_name = "{}.png".format(os.path.join(self._output_location, file_name))
        fig.write_image(path_name)


    def __bedtimes_plot(self, start: str, end: str, periodicity: Periodicity, summary_type_measurement_tuples: List[Tuple[str, str]], **kwargs):
        
        dates, plot_data_sets, plot_legends, plot_units = self._get_plot_data_sets(start, end, periodicity, summary_type_measurement_tuples)

        evening_times = plot_data_sets[0]
        duration = plot_data_sets[1]

        # setting title
        if 'title' in kwargs.keys():
            title = kwargs['title']
        else:
            title = "Bedtime Plot"

        fig = go.Figure()
        fig.add_trace(go.Bar(x=dates, y=duration, base=evening_times))
        fig.update_layout(title=title, xaxis={'title': {'text': 'Dates'}}, yaxis={'title': {'text': 'Time'}})

        tickvals = list(range(0, 48, 1))
        ticktext = []
        for tickval in tickvals:
            hours = math.floor(tickval)
            minutes = (tickval - hours) * 60
            if hours >= 24:
                hours -= 24
            text = "{:02d}:{:02d}".format(hours, minutes)
            ticktext.append(text)

        fig.update_yaxes(tickmode='array')
        fig.update_yaxes(tickvals=tickvals)
        fig.update_yaxes(ticktext=ticktext)

        fig.update_traces(marker_colorbar_ticklen=10, selector=dict(type='scatter'))

        # saving the plot as an image
        if 'output_file_name' in kwargs.keys():
            output_file_name = kwargs['output_file_name']
        else:
            output_file_name = "temp"
        self.__save(fig, output_file_name)


    def __bar_plot_multiple_of_same_unit(self, start: str, end: str, periodicity: Periodicity, summary_type_measurement_tuples: List[Tuple[str, str]], **kwargs):
        
        dates, plot_data_sets, plot_legends, plot_units = self._get_plot_data_sets(start, end, periodicity, summary_type_measurement_tuples)

        # check if each plot data has same unit, otherwise the scale might get screwd
        if len(Counter(plot_units).keys()) > 1:
            raise ValueError("Different Units")
        unit_as_text = UnitsAnnotationText[plot_units[0]]

        # setting title
        if 'title' in kwargs.keys():
            title = kwargs['title']
        else:
            title = "Bar Chart"

        # drawing plotly figure
        fig = px.bar(x=dates, y=plot_data_sets, title=title, labels={'x': 'Dates', 'value': unit_as_text})

        # setting the legend to identify the different lines
        for i, legend_name in enumerate(plot_legends):
            fig['data'][i]['name'] = legend_name

        # saving the plot as an image
        if 'output_file_name' in kwargs.keys():
            output_file_name = kwargs['output_file_name']
        else:
            output_file_name = "temp"
        self.__save(fig, output_file_name)



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
        fig = go.Figure()
        for data, legend in zip(plot_data_sets, plot_legends):
            fig.add_trace(go.Scatter(x=dates, y=data, name=legend, mode='lines+markers'))
        fig.update_layout(title=title, xaxis={'title': {'text': 'Dates'}}, yaxis={'title': {'text': unit_as_text}})

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


    def __histogram_plot_multiple_of_same_unit(self, start: str, end: str, periodicity: Periodicity, summary_type_measurement_tuples: List[Tuple[str, str]], **kwargs):

        dates, plot_data_sets, plot_legends, plot_units = self._get_plot_data_sets(start, end, periodicity, summary_type_measurement_tuples)

        # check if each plot data has same unit, otherwise the scale might get screwd
        if len(Counter(plot_units).keys()) > 1:
            raise ValueError("Different Units")
        unit_as_text = UnitsAnnotationText[plot_units[0]]

        # setting title
        if 'title' in kwargs.keys():
            title = kwargs['title']
        else:
            title = "Histogram"

        # TODO: customize
        interval_size = 2
        nbins = 100 / 5

        # drawing plotly figure
        fig = go.Figure()
        for data, legend in zip(plot_data_sets, plot_legends):
            fig.add_trace(go.Histogram(x=data, name=legend, histnorm='percent'))
        fig.update_layout(
            barmode='overlay', 
            title=title, 
            xaxis={'title': {'text': unit_as_text}}, 
            yaxis={'title': {'text': 'Percent'}}
        )
        fig.update_traces(opacity=0.75)

        # setting range of x-axis for Scores to 0 to 100
        if plot_units[0] == Unit.score:
            fig.update_layout(xaxis={'range': [0, 100]})

        # saving the plot as an image
        if 'output_file_name' in kwargs.keys():
            output_file_name = kwargs['output_file_name']
        else:
            output_file_name = "temp"
        self.__save(fig, output_file_name)
