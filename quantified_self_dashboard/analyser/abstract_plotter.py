import os
import math
import datetime
from typing import List, Tuple, Union

import numpy as np

from summary.summary_container import SummaryContainer
from common.constants import *
from common.date_helper import all_date_strings_between_dates, get_day_before
from analyser.abstract_analyser import AbstractAnalyser
from analyser.transform_measurements import *


class AbstractPlotter(AbstractAnalyser):
    """
    Analysing SummaryContainer data by plotting, using the plotly library.
    """


    def _get_plot_data_sets(self, start: str, end: str, periodicity: Periodicity, summary_type_measurement_tuples: List[Tuple[str, str]]) -> Tuple[List[str], List[Union[np.array, List]], List[str], List[Unit]]:
        """
        Wrapper to get the all data needed for plotting
        when needing multiple summary_type-measurement_name combinations.

        Parameters
        ----------
        start : str
            Analysis start date in YYYY-MM-DD format.

        end : str
            Analysis end date in YYYY-MM-DD format.

        periodicity : Periodicity
            Which timeframes must be considered, e.g. daily, weekly, monthyl, yearly.

        summary_type_measurement_tuples : str
            List of Tuples, where each tuple represents the summary type and 
            measurement name which will get plotted.

        Returns
        --------
        Tuple of multiple lists:
            List of all date strings,
            List of np.arrays or rists of plottalbe data,
            List of titles of name of the measurements,
            List of units of the measurements
        """

        # x-axis
        dates = all_date_strings_between_dates(start, end)

        # y-axis
        plot_data_sets, plot_legends, plot_units = [], [], []

        # receiving all plot sets from the summary container as numpy arrays
        for summary_type, measurement_name in summary_type_measurement_tuples:
            plot_data, plot_legend_name, plot_unit = self._get_plottable_data(start, end, periodicity, summary_type, measurement_name)

            plot_data_sets.append(plot_data)
            plot_legends.append(plot_legend_name)
            plot_units.append(plot_unit)

        return dates, plot_data_sets, plot_legends, plot_units


    def _get_plottable_data(self, start: str, end: str, periodicity: Periodicity, summary_type: str, measurement_name: str) -> Tuple[Union[np.array, List], str, Unit]:
        """
        Retrieving the raw data form the summary container, 
        transforming the data into a better format.
        Also returning the title of the summary_type-measurement_combination 
        and the resulting unit.

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

        # getting transformation and other information for this summary type and measurement name
        summary_transform = summary_type_transform[summary_type]
        if measurement_name in summary_transform.keys():
            measurement_transform = summary_transform[measurement_name]
            trans_func, _, _, _, trans_unit, measurement_title, one_day_offset = measurement_transform
            if one_day_offset:
                # in some cases the oura api is storing the measurements 
                # of the night from day 1 to day 2 in the day 1 summary
                # but here it might be better to display them on day 2
                start = get_day_before(start)
                end = get_day_before(end)
        else:
            raise ValueError("No transformation available")


        # retrieving the data as a np.array or list
        data_as_np_array = (trans_unit != Unit.time_of_day)
        if data_as_np_array:
            raw_data = self._container.get_values(start, end, summary_type, measurement_name)
            vfunc = np.vectorize(trans_func)
            plot_data = vfunc(raw_data)
        else:
            # datetime values and strings cannot be stored in normal np arrays
            # using python lists instead
            raw_data = self._container.get_values(start, end, summary_type, measurement_name, output_as_np_array=False)
            plot_data = list(map( trans_func, raw_data ))


        # averaging depending on teh given periodicty
        if periodicity == Periodicity.daily:
            pass
        elif periodicity == Periodicity.weekly:
            raise NotImplementedError()
        elif periodicity == Periodicity.monthly:
            raise NotImplementedError()
        elif periodicity == Periodicity.weekday_averages:
            raise NotImplementedError()
        elif periodicity == Periodicity.yearly:
            raise NotImplementedError()
        # TODO: weekly, monthly and yearly averaging


        return plot_data, measurement_title, trans_unit





