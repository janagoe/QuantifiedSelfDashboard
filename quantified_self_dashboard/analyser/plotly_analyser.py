import os
import math
import datetime
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
from collections import Counter
import plotly
import plotly.express as px
import plotly.graph_objects as go

from summary.summary_container import SummaryContainer
from common.constants import *
from common.date_helper import all_date_strings_between_dates
from analyser.abstract_plotter import AbstractPlotter
from analyser.transform_measurements import *
from analyser.analysis_type_configurations import *



class PlotlyAnalyser(AbstractPlotter):
    """
    Analysing SummaryContainer data by plotting, using the plotly library.
    """

    _supported_analysis_types = [
        AnalysisType.scores_daily, 
        AnalysisType.scores_weekly, 
        AnalysisType.scores_monthly, 
        AnalysisType.scores_weekdays, 

        AnalysisType.sleep_durations_daily, 
        AnalysisType.sleep_durations_weekly, 
        AnalysisType.sleep_durations_monthly, 
        AnalysisType.sleep_durations_weekdays, 

        AnalysisType.bedtimes_daily,
        AnalysisType.bedtimes_weekly,
        AnalysisType.bedtimes_monthly,
        AnalysisType.bedtimes_weekdays,

        AnalysisType.recovery_indicators_daily,
        AnalysisType.recovery_indicators_weekly,
        AnalysisType.recovery_indicators_monthly,
        AnalysisType.recovery_indicators_weekdays,

        AnalysisType.sleep_score_distribution,
        AnalysisType.readiness_score_distribution,
        AnalysisType.activity_score_distribution,
    ]


    def _analyse(self, start: str, end: str, analysis_type: AnalysisType, *args):
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

        # summary_type_measurement_tuples
        if analysis_type not in analysis_type_summary_type_measurement_tuples.keys():
            raise AttributeError()
        summary_type_measurement_tuples = analysis_type_summary_type_measurement_tuples[analysis_type]

        # peridicity
        if analysis_type in analysis_type_periodicity.keys():
            periodicity = analysis_type_periodicity[analysis_type]
        else:
            periodicity = default_periodicity

        # plot type
        if analysis_type in analysis_type_plot_type.keys():
            plot_type = analysis_type_plot_type[analysis_type]
        else:
            plot_type = default_plot_type

        # output file name
        output_file_name = "{}_{}_{}_{}".format(analysis_type.name, periodicity.name, start, end)

        # title
        if analysis_type in analysis_type_plot_titles_template.keys():
            title = analysis_type_plot_titles_template[analysis_type].format(start, end)
        else:
            periodicity_str = periodicity.name.title()
            analysis_type_str = analysis_type.name.title()
            title = "{} {} from {} until {}".format(periodicity_str, analysis_type_str, start, end)

        # kwargs
        if analysis_type in analysis_type_plot_kwargs:
            kwargs = analysis_type_plot_kwargs[analysis_type]
        else:
            kwargs = dict()
        kwargs['title'] = title
        kwargs['output_file_name'] = output_file_name


        self.__create_plot(start, end, periodicity, summary_type_measurement_tuples, plot_type, **kwargs)


    def __save(self, fig, file_name):
        """ Saving the plotly figure as an image into the given output file name. """
        path_name = "{}.png".format(os.path.join(self._output_location, file_name))
        fig.write_image(path_name)


    def __create_plot(self, start: str, end: str, periodicity: Periodicity, summary_type_measurement_tuples: List[Tuple[str, str]], plot_type: PlotType, **kwargs):
        """
        Creating the plot, adaptable to all plot types, periodicities and summary_type-measurement_name combinations. 

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

        plot_type : PlotType
            Which kind of plot will be created. Either lines, bar chart, histogram or time periods. 
            Easily extendable.
        """

        dates, plot_data_sets, plot_legends, plot_units = self._get_plot_data_sets(start, end, periodicity, summary_type_measurement_tuples)

        # TODO
        # check if each plot data has same unit, otherwise the scale might get screwd
        # if len(Counter(plot_units).keys()) > 1:
        #     raise ValueError("Different Units")

        fig = self.__create_figure(plot_type, dates, plot_data_sets, plot_legends, plot_units)

        # setting ticks format depending on periodicty
        if periodicity == Periodicity.weekly:
            fig.update_layout(xaxis={'tickformat': "CW%W"})
        elif periodicity == Periodicity.monthly:
            fig.update_layout(xaxis={'tickformat': "%B", 'tickvals': dates})
        elif periodicity == Periodicity.weekdays:
            fig.update_layout(xaxis={'tickformat': "%a", 'tickvals': dates})
        elif periodicity == Periodicity.yearly:
            fig.update_layout(xaxis={'tickformat': "%Y", 'tickvals': dates})

        # setting title
        if 'title' in kwargs.keys():
            title = kwargs['title']
        else:
            title = "Bedtime Plot"
        fig.update_layout(title=title)

        # saving the plot as an image
        if 'output_file_name' in kwargs.keys():
            output_file_name = kwargs['output_file_name']
        else:
            output_file_name = "temp"
        self.__save(fig, output_file_name)


    def __create_figure(self, plot_type, dates, plot_data_sets, plot_legends, plot_units, **kwargs) -> go.Figure:
        """
        Helper method to call the correct plotting method depending on the plot type.
        All parameters will be forwarded to corresponding method. 

        Returns
        -------
        Figure
        """

        plot_type_to_create_figure_func = {
            PlotType.time_period: self.__time_period_figure,
            PlotType.lines: self.__line_figure,
            PlotType.bar_chart: self.__bar_chart_figure,
            PlotType.histogram: self.__histogram_figure,
        }

        create_figure_func = plot_type_to_create_figure_func[plot_type]
        fig = create_figure_func(dates, plot_data_sets, plot_legends, plot_units, **kwargs)

        return fig


    def __time_period_figure(self, dates: pd.DatetimeIndex, plot_data_sets, plot_legends: List[str], plot_units: List[Unit], **kwargs) -> go.Figure:
        """
    	Plotting time periods as a bar chart. 
        A starting time and duration have to be given. 
        The starting time is represented as an offset of the bars.
        The y-axis is representing the times of the day.
        An example would be the time one got to bed and the duration in bed.
        """
        
        start_times = plot_data_sets[0] 
        duration = plot_data_sets[1] 

        fig = go.Figure()
        fig.add_trace(go.Bar(x=dates, y=duration, base=start_times))
        fig.update_layout(xaxis={'title': {'text': 'Dates'}}, yaxis={'title': {'text': 'Time'}})

        # adjusting ticks and ticktext for readable timeformats on the y-axis
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

        # more space for the time text
        fig.update_traces(marker_colorbar_ticklen=10, selector=dict(type='scatter'))

        return fig


    def __line_figure(self, dates: pd.DatetimeIndex, plot_data_sets, plot_legends: List[str], plot_units: List[Unit], **kwargs) -> go.Figure:
        """
        Drawing one or multiple lines in one plot. 
        """
        
        # drawing plotly figure
        fig = go.Figure()
        for data, legend in zip(plot_data_sets, plot_legends):
            fig.add_trace(go.Scatter(x=dates, y=data, name=legend, mode='lines+markers'))
        unit_as_text = UnitsAnnotationText[plot_units[0]]
        fig.update_layout(xaxis={'title': {'text': 'Dates'}}, yaxis={'title': {'text': unit_as_text}})

        fig.update_xaxes(constraintoward="left")

        # setting y-axis start to zero
        if 'yaxis_to_zero' in kwargs.keys():
            tozero_val = kwargs['yaxis_to_zero']
            if tozero_val:
                fig.update_yaxes(rangemode='tozero')

        # setting the legend to identify the different lines
        for i, legend_name in enumerate(plot_legends):
            fig['data'][i]['name'] = legend_name

        return fig


    def __bar_chart_figure(self, dates: pd.DatetimeIndex, plot_data_sets, plot_legends: List[str], plot_units: List[Unit], **kwargs) -> go.Figure:
        """
        Drawing one or multiple bars in one plot. 
        """

        unit_as_text = UnitsAnnotationText[plot_units[0]]
        fig = px.bar(x=dates, y=plot_data_sets, labels={'x': 'Dates', 'value': unit_as_text})

        # setting the legend to identify the different lines
        for i, legend_name in enumerate(plot_legends):
            fig['data'][i]['name'] = legend_name

        return fig


    def __histogram_figure(self, dates: pd.DatetimeIndex, plot_data_sets, plot_legends: List[str], plot_units: List[Unit], **kwargs) -> go.Figure:
        """
        Drawing a histogram of one or more distributions.
        """

        # TODO: customize, this makes only sense for score units
        interval_size = 5
        nbins = 100 / interval_size

        # drawing plotly figure
        fig = go.Figure()
        for data, legend in zip(plot_data_sets, plot_legends):
            fig.add_trace(go.Histogram(x=data, name=legend, histnorm='percent'))

        # setting annotations
        unit_as_text = UnitsAnnotationText[plot_units[0]]
        fig.update_layout(
            barmode='overlay', 
            xaxis={'title': {'text': unit_as_text}}, 
            yaxis={'title': {'text': 'Percent'}}
        )

        # transparency
        fig.update_traces(opacity=0.75)

        # setting range of x-axis for Scores to 0 to 100
        if plot_units[0] == Unit.score:
            fig.update_layout(xaxis={'range': [0, 100]})

        return fig
