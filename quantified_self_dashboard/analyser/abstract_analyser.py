import os
from typing import List
from summary.summary_container import SummaryContainer
from common.constants import AnalysisType, Periodicity


class AbstractAnalyser:
    """ 
    Abstract Analyser class, providing wrapper methods for many different 
    analyser types.
    """

    # Analysis Types supported by this analyser 
    _supported_analysis_types: List[AnalysisType] = []


    def __init__(self, output_path: List[str], container: SummaryContainer):
        """
        Parameters
        ----------
        output_path : List[str]
            Path where output images/files can be saved.

        container : SummaryContainer
            Where the analyser can get its analysis data from.
        """
        self._container = container
        self._output_location = os.path.join(os.getcwd(), *output_path)


    def analyse(self, start: str, end: str, periodicity: Periodicity, analysis_type: AnalysisType, *args):
        """
        Parameters
        ----------
        start : str
            Analysis start date in YYYY-MM-DD format.

        end : str
            Analysis end date in YYYY-MM-DD format.

        periodicity : Periodicity
            Which timeframes must be considered, e.g. daily, weekly, monthyl, yearly.

        analysis_type : AnalysisType
            The chosen type of anayzis for this method call.
        """
        self.__check_parameters(start, end, periodicity, analysis_type, *args)
        self._analyse(start, end, periodicity, analysis_type, *args)
    

    def __check_parameters(self, start: str, end: str, periodicity: Periodicity, analysis_type: AnalysisType, *args):
        """
        Parameters
        ----------
        start : str
            Analysis start date must be in YYYY-MM-DD format and before the end date.

        end : str
            Analysis end date must be in YYYY-MM-DD format and after the start date.

        periodicity : Periodicity
            Which timeframes must be considered, e.g. daily, weekly, monthyl, yearly.

        analysis_type : AnalysisType
            The chosen type of anayzis for this method call, must be part of the supported
            analysis types of this Analyser Class.
        """

        if not analysis_type in self._supported_analysis_types:
            raise ValueError("Invalid AnalysisType Parameter")

        # TODO: check if all dates are given in the summary container
        # TODO: check if start is before end
        # TODO: check if dates have valid format


    def _analyse(self, start_date: str, end_date: str, periodicity: str, analysis_type, *args):
        """
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

        # here each subclass implementation starts
        raise NotImplementedError("Abstract Class")



