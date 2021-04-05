import os
import math
import datetime
from typing import List, Tuple, Union

import numpy as np

from summary.summary_container import SummaryContainer
from common.constants import *
from common.date_helper import *
# from common.date_helper import all_date_strings_between_dates, get_day_before
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
            trans_func, raw_data_type, trans_output_type, _, trans_unit, measurement_title, one_day_offset = measurement_transform
            if one_day_offset:
                # in some cases the oura api is storing the measurements 
                # of the night from day 1 to day 2 in the day 1 summary
                # but here it might be better to display them on day 2
                start = get_day_before(start)
                end = get_day_before(end)
        else:
            raise ValueError("No transformation available")

        raw_values_are_numberical = raw_data_type in [int, float]
        transformed_values_are_numerical = trans_output_type in [int, float]

        # retrieving the data as a np.array or list
        if raw_values_are_numberical:
            raw_data = self._container.get_values(start, end, summary_type, measurement_name)
            vfunc = np.vectorize(trans_func)
            daily_plot_data = vfunc(raw_data)
        else:
            # datetime values and strings cannot be stored in normal np arrays
            # using python lists instead
            raw_data = self._container.get_values(start, end, summary_type, measurement_name, output_as_np_array=False)
            daily_plot_data = list(map( trans_func, raw_data ))

        # averaging depending on the given periodicty
        if periodicity == Periodicity.daily:
            plot_data = daily_plot_data
        else:
            if transformed_values_are_numerical:
                plot_data = self.__transform_daily_values_to_averaged_by_periodictiy(start, end, periodicity, daily_plot_data)
            else:
                raise NotImplementedError()
        
        return plot_data, measurement_title, trans_unit


    def __transform_daily_values_to_averaged_by_periodictiy(self, start: str, end: str, periodicity: Periodicity, daily_data: Union[np.array, List]) -> np.array:
        """
        Averaging the daily values into averaged values depending on the periodicity.
        For e.g. the weekly periodicity the values of each week get averaged into one value.

        Parameters
        ----------
        start : str
            Analysis start date in YYYY-MM-DD format.

        end : str
            Analysis end date in YYYY-MM-DD format.

        periodicity : Periodicity
            Which timeframes must be considered. Periodicity.daily may not be called here.

        daily_data : Union[np.array, List]
            Raw daily data.

        Returns
        --------
        np.array 
            of the averaged values
        """

        if periodicity == Periodicity.daily:
            raise AttributeError()

        dates = all_date_strings_between_dates(start, end)

        # defining functions to transform datetime objects into unique identifiers 
        # and so sort those chronologically
        if periodicity == Periodicity.weekly:
            date_obj_to_identifier_func = lambda date_obj: (date_obj.year, date_obj.isocalendar()[1])
            identifier_sorting = lambda identifier: identifier[0] * 100 + identifier[1] 
        elif periodicity == Periodicity.monthly:
            date_obj_to_identifier_func = lambda date_obj: (date_obj.year, date_obj.month)
            identifier_sorting = lambda identifier: identifier[0] * 100 + identifier[1] 
        elif periodicity == Periodicity.weekdays:
            date_obj_to_identifier_func = lambda date_obj: date_obj.isocalendar()[2]
            identifier_sorting = lambda identifier: identifier 
        elif periodicity == Periodicity.yearly:
            date_obj_to_identifier_func = lambda date_obj: date_obj.year
            identifier_sorting = lambda identifier: identifier 

        # partioning by week
        buckets = dict()
        for index, date_str in enumerate(dates):
            date_obj = simple_string_to_datetime(date_str)
            identifier = date_obj_to_identifier_func(date_obj)

            if identifier not in buckets.keys():
                buckets[identifier] = []
            
            day_value = daily_data[index]
            buckets[identifier].append(day_value)

        # averaging daily values into one weekly value
        averaged_values = dict()
        for identifier, daily_values in buckets.items():
            averaged_value = np.average(daily_values)
            averaged_values[identifier] = averaged_value

        # transforming dict into list in chronological order
        weekly_data = np.zeros(len(averaged_values.keys()))
        mapped_averaged_value_tuples = map(lambda k: (identifier_sorting(k), averaged_values[k]), averaged_values.keys())
        sorted_averaged_value_tuples = sorted(mapped_averaged_value_tuples, key=lambda s: s[0])
        average_values_sorted_by_identifiers = list(map(lambda t: t[1], sorted_averaged_value_tuples))
        
        return np.asarray(average_values_sorted_by_identifiers)
