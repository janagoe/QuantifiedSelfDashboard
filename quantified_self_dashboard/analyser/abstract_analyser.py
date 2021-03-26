from typing import List
from summary.summary_container import SummaryContainer
from common.constants import *
import os


class AbstractAnalyzer:

    _supported_analysis_types = []

    def __init__(self, output_path: List[str], container: SummaryContainer):
        self._container = container
        self._output_location = os.path.join(os.getcwd(), *output_path)

    def __check_parameters(self, start_date, end_date, periodicity, analysis_type, *args):
        # check start before end

        # eck all dates inside of summary container

        if not periodicity in [PERIODICITY_DAILY, PERIODICITY_WEEKLY, PERIODICITY_MONTHLY]:
            raise ValueError("Invalid Analysis Periodicity Parameter")

        if not analysis_type in self._supported_analysis_types:
            raise ValueError("Invalid Analysis Type Parameter")

    def _analyse(self, start_date: str, end_date: str, periodicity, analysis_type, *args):
        # here each subclass implementation starts
        raise NotImplementedError("Abstract Class")

    def analyze(self, start_date: str, end_date: str, periodicity, analysis_type, *args):
        self.__check_parameters(start_date, end_date, periodicity, analysis_type, *args)
        self._analyse(start_date, end_date, periodicity, analysis_type, *args)


