import os
from typing import List, Tuple

import numpy as np
from collections import Counter
import plotly.express as px

from summary.summary_container import SummaryContainer
from common.constants import *
from common.date_helper import all_date_strings_between_dates
from analyser.abstract_analyser import AbstractAnalyser
from analyser.transform_measurements import *


class PlotlyAnalyser(AbstractAnalyser):
    """
    Analysing SummaryContainer data by plotting, using the plotly library.
    """


    _supported_analysis_types = [AnalysisType.test]


    def __init__(self, output_path: List[str], container: SummaryContainer):
        """
        Parameters
        ----------
        output_path : List[str]
            Path where output images/files can be saved.

        container : SummaryContainer
            Where the analyser can get its analysis data from.
        """
        super().__init__(output_path, container)
        

    def _analyse(self, start: str, end: str, periodicity, analysis_type, *args):
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

        # TODO: implementing switch-case-like structure for all different supported analysis types
        self.__plot_multiple_of_same_unit(start, end, Periodicity.daily, [(SummaryType.sleep, "rmssd")])


    def __plot_multiple_of_same_unit(self, start: str, end: str, periodicity: Periodicity, summary_type_measurement_tuples: List[Tuple[str, str]], **kwargs):
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
        """

        # x-axis
        dates = all_date_strings_between_dates(start, end)

        plot_data_sets, plot_legends, plot_units = [], [], []

        # receiving all plot sets from the summary container as numpy arrays
        for summary_type, measurement_name in summary_type_measurement_tuples:
            plot_data, plot_legend_name, plot_unit = self.__get_plottable_data(start, end, periodicity, summary_type, measurement_name)

            plot_data_sets.append(plot_data)
            plot_legends.append(plot_legend_name)
            plot_units.append(plot_unit)

        # check if each plot data has same unit, otherwise the scale might get screwd
        if len(Counter(plot_units).keys()) > 1:
            raise ValueError("Different Units")

        if 'title' in kwargs.keys():
            title = kwargs['title']
        else:
            title = "Line Plot"

        unit_as_text = UnitsAnnotationText[plot_units[0]]

        # drawing plotly figure
        fig = px.line(x=dates, y=plot_data_sets, title=title, labels={'x': 'Dates', 'y': unit_as_text})

        # setting the legend to identify the different lines
        for i, legend_name in enumerate(plot_legends):
            fig['data'][i]['name'] = legend_name

        # saving the plot as an image
        if 'output_file_name' in kwargs.keys():
            output_file_name = kwargs['output_file_name']
        else:
            output_file_name = "temp"
        self.__save(fig, output_file_name)


    def __get_plottable_data(self, start: str, end: str, periodicity: Periodicity, summary_type: str, measurement_name: str) -> Tuple[np.array, str, Unit]:
        """
        Retrieving the data form the summary container, 
        transforming the data into a better format,
        and getting

        Parameters
        ----------
        start : str
            Analysis start date in YYYY-MM-DD format.

        end : str
            Analysis end date in YYYY-MM-DD format.

        periodicity : Periodicity
            Which timeframes must be considered, e.g. daily, weekly, monthyl, yearly.

        summary_type : str
            Type of summary to plot the measurement name of.

        measurement_name : str
            Name of the measurement.

        Returns
        --------
        Tuple
            np.array of data to plot, 
            title of name of the measurement,
            unit of the measurement
        """

        if periodicity == Periodicity.daily:
            raw_data = self._container.get_np_array(start, end, summary_type, measurement_name)
        elif periodicity == Periodicity.weekly:
            raise NotImplementedError()
        elif periodicity == Periodicity.monthly:
            raise NotImplementedError()
        elif periodicity == Periodicity.yearly:
            raise NotImplementedError()

        # TODO: weekly, monthly and yearly averaging

        # data, if no transformation is possible
        plot_data = raw_data
        measurement_title = "{} {}".format(summary_type, measurement_name)
        trans_unit = Unit.undefined

        # transforming the raw data if possible
        # e.g. seconds into hours
        summary_transform = summary_type_transform[summary_type]
        if measurement_name in summary_transform.keys():

            measurement_transform = summary_transform[measurement_name]
            trans_func, _, _, _, trans_unit, measurement_title = measurement_transform

            # applying the transformation function to the entire np.array
            vfunc = np.vectorize(trans_func)
            plot_data = vfunc(raw_data)

        return plot_data, measurement_title, trans_unit


    def __save(self, fig, file_name):
        """ Saving the plotly figure as an image into the given output file name. """
        path_name = "{}.png".format(os.path.join(self._output_location, file_name))
        fig.write_image(path_name)


