from typing import List, Tuple
from summary.summary_container import SummaryContainer
from common.constants import *
from common.date_helper import *
import os
from analyser.abstract_analyser import AbstractAnalyzer
from analyser.transform_measurements import *
from collections import Counter
import plotly.express as px
import numpy as np


class PlotlyAnalyzer(AbstractAnalyzer):

    _supported_analysis_types = ["test"]

    def __init__(self, output_path: List[str], container: SummaryContainer):
        super().__init__(output_path, container)
        print(self._output_location)

    def _analyse(self, start_date: str, end_date: str, periodicity, analysis_type, *args):

        # self.__plot_multiple_of_same_unit(start_date, end_date, PERIODICITY_DAILY, "Crazy Shit", "test", [(SLEEP, "total"), (SLEEP, "rem")])

        self.__plot_multiple_of_same_unit(start_date, end_date, PERIODICITY_DAILY, "Crazy Shit", "test", [(SLEEP, "rmssd")])


    def __plot_multiple_of_same_unit(self, start_date, end_date, periodicity, title: str, file_name: str, summary_type_measurement_tuples: List[Tuple[str, str]]):

        dates = all_date_strings_between_dates(start_date, end_date)

        plot_data_sets = []
        plot_legends = []
        plot_units = []

        for summary_type, measurement_name in summary_type_measurement_tuples:
            plot_data, plot_legend_name, plot_unit = self.__get_plottable_data(start_date, end_date, periodicity, summary_type, measurement_name)

            plot_data_sets.append(plot_data)
            plot_legends.append(plot_legend_name)
            plot_units.append(plot_unit)

        # check if each plot data has same unit
        # otherwise the scale might be screwd
        if len(Counter(plot_units).keys()) > 1:
            raise ValueError("Different Units")

        fig = px.line(x=dates, y=plot_data_sets, title=title, labels={'x': 'Dates', 'y': plot_units[0]})

        for i, legend_name in enumerate(plot_legends):
            fig['data'][i]['name'] = legend_name

        self.__save(fig, file_name)


    def __get_plottable_data(self, start_date: str, end_date: str, periodicity, summary_type: str, measurement_name: str) -> Tuple[np.array, str, str]:
        
        if periodicity == PERIODICITY_DAILY:
            raw_data = self._container.get_np_array(start_date, end_date, summary_type, measurement_name)
        elif periodicity == PERIODICITY_WEEKLY:
            raise NotImplementedError()
        elif periodicity == PERIODICITY_MONTHLY:
            raise NotImplementedError()

        plot_data = raw_data
        measurement_title = "{} {}".format(summary_type, measurement_name)

        summary_transform = summary_type_transform[summary_type]
        if measurement_name in summary_transform.keys():
            measurement_transform = summary_transform[measurement_name]

            trans_func, orig_type, trans_type, orig_unit, trans_unit, measurement_title = measurement_transform

            vfunc = np.vectorize(trans_func)
            plot_data = vfunc(raw_data)

        return plot_data, measurement_title, trans_unit



    def __save(self, fig, file_name):
        path_name = "{}.png".format(os.path.join(self._output_location, file_name))
        fig.write_image(path_name)


