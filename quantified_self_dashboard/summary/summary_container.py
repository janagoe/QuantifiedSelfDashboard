from typing import List, Union
import datetime
import numpy as np

from summary.summary import Summary, get_summary_class_from_type
from common.constants import SummaryType, SUMMARY_DATE
from common.date_helper import all_date_strings_between_dates, is_date_within_range, datetime_to_simple_iso
from connector.abstract_connector import AbstractConnector


class SummaryContainer:
    """
    Container for Summary objects,
    needed for making plots or saving data. 
    """

    # list of all summary types which this container is able to hold
    __possible_summaries = [SummaryType.sleep, SummaryType.readiness, SummaryType.activity, SummaryType.bedtime, SummaryType.subjective]


    def __init__(self, starting_date: str, containing_sleep=False, containing_readiness=False, containing_activity=False, containing_bedtime=False, containing_subjective=False):
        """
        Making preparations to load summaries.

        Additional keyword arguments.
        ----------------------------
        containing_sleep : bool
            Whether this container is supposed to hold sleep summaries or not.
            
        containing_readiness : bool
            Whether this container is supposed to hold readiness summaries or not.
            
        containing_activity : bool
            Whether this container is supposed to hold activity summaries or not.
            
        containing_bedtime : bool
            Whether this container is supposed to hold bedtime summaries or not.
            
        containing_subjective : bool
            Whether this container is supposed to hold subjective summaries or not.
        """

        self.__starting_date = starting_date

        self.__api_connectors = []
        self.__storage_connectors = []
        self.__user_connectors = []

        # order is relevant here
        containing = [ 
            containing_sleep, 
            containing_readiness, 
            containing_activity, 
            containing_bedtime, 
            containing_subjective
        ] 

        self.__prepare_attributes(containing)


    def add_storage_connector(self, conn):
        self.__storage_connectors.append(conn)

    def add_user_connector(self, conn):
        self.__user_connectors.append(conn)

    def add_api_connector(self, conn):
        self.__api_connectors.append(conn)

    def __prepare_attributes(self, containing: List[bool]):
        """
        Preparing dynamic attributes depending on the containing summary types for loading.

        In e.g. the __sleep_container attribute the loaded sleep summaries will be stored as a list.
        The __required_dates_sleep is a helper list for the loading process and initially
        filled with all dates from the starting date until today.
        For each contained summary type these two attributes will be created.

        Parameters
        ----------
        containing : List[bool]
            List of which summary types this container is supposed to hold.
        """

        self.__contained_summaries = []

        # Lists of the dynamic attribute names
        self.__summary_container_attribute_names = []
        self.__summary_required_dates_attribute_names = []

        # checking which summary types we want to use this container for
        for summary_str, summary_contained in zip(self.__possible_summaries, containing):
            if summary_contained: 
                self.__contained_summaries.append(summary_str)

        # creating attribute names for summary types
        for summary_str in self.__contained_summaries:

            # e.g. __sleep_container and __required_dates_sleep
            container_attribute_name = "__{}_container".format(summary_str)
            attribute_helper_name = "__required_dates_{}".format(summary_str) 

            self.__summary_container_attribute_names.append(container_attribute_name)
            self.__summary_required_dates_attribute_names.append(attribute_helper_name)
   
        # setting the container attributes
        for container_attribute_name in self.__summary_container_attribute_names:
            setattr(self, container_attribute_name, [])   

        # filling the required dates helper atrributes with all dates from the starting date until today
        self.__dates = all_date_strings_between_dates(self.__starting_date, datetime_to_simple_iso(datetime.datetime.today()))
        for required_date_attribute_name in self.__summary_required_dates_attribute_names:
            setattr(self, required_date_attribute_name, self.__dates)   


    def __load_via_connector(self, connector: AbstractConnector):
        """
        Trying to load as many of the required summaries as possible from the given connector.
        It has to be considered which summary types the connector is supporting. 

        Loading summaries from the required dates attributes.
        Adding the loaded summaries into the container attributes and updating the required dates.

        Parameters
        ----------
        connector : AbstractConnector
            Connector to load the summaries from with in method call.
        """

        # summary types which this container contains and the connector supports
        common_summary_types = list(set.intersection(set(self.__contained_summaries), set(connector.supported_summary_types)))

        for summary_type, container_attr, required_dates_attr in zip(self.__contained_summaries, self.__summary_container_attribute_names, self.__summary_required_dates_attribute_names):
            if summary_type not in common_summary_types:
                continue
            
            # still required dates from the previous connector
            required_dates_for_summary_type = getattr(self, required_dates_attr)
            if len(required_dates_for_summary_type) == 0:
                continue

            # summary object constructor
            summary_class = get_summary_class_from_type(summary_type)


            # required dates which could not be loaded by this connector
            still_required_dates = []

            # summary objects loaded by this connector
            new_summary_objects = []

            # previously loaded objects
            old_summary_objects = getattr(self, container_attr)

            # trying to load the summaries
            for date in required_dates_for_summary_type:
                summary_date_obj = summary_class()
                success = summary_date_obj.load(connector, date)
                if not success:
                    still_required_dates.append(date)
                else:
                    new_summary_objects.append(summary_date_obj)
            
            # updating required dates for the connector
            setattr(self, required_dates_attr, still_required_dates)

            # adding newly loaded objects
            setattr(self, container_attr, new_summary_objects + old_summary_objects)
        

    def preload(self):
        for storage_conn in self.__storage_connectors:
            storage_conn.preload()

        # TODO add threads
        for api_conn in self.__api_connectors:
            api_conn.preload(everything=True)


    def load(self) -> bool: 
        """
        Trying to load all required data from the start until end date,
        by making use of all given available connectors.

        Returns
        -------
        bool
            whether all dates could get loaded or not
        """

        

        # letting each connector try to load as many of the required summaries
        for conn in self.__storage_connectors + self.__api_connectors + self.__user_connectors:
            self.__load_via_connector(conn)

        # sorting by date
        # assuming the dates are ordered lexicographically
        for summary_type in self.__contained_summaries:
            container_attr_name = self.__get_container_attribute_name(summary_type)
            container_of_type = getattr(self, container_attr_name)
            sorted_container = sorted(container_of_type, key=lambda s: s.summary_date)
            setattr(self, container_attr_name, sorted_container)


    def __get_container_attribute_name(self, summary_type: SummaryType) -> str:
        """ Helper method to get the container attribute name of the summary type """
        for sum_type, cont_attr in zip(self.__contained_summaries, self.__summary_container_attribute_names):
            if sum_type == summary_type:
                return cont_attr
        return None
    

    def get_summary_of_date(self, summary_type: SummaryType, date: str) -> Union[Summary, None]:
        """ Returns the summary object with the given summary type and date if its contained. """
        cont_attr_name = self.__get_container_attribute_name(summary_type)
        if cont_attr_name:
            container_of_type = getattr(self, cont_attr_name)
            filtered = list(filter(lambda s: s.summary_date == date, container_of_type))
            if len(filtered) > 0:
                return filtered[0]
        return None


    def get_summaries_within_timerange(self, summary_type: SummaryType, start: str, end: str) -> Union[List[Summary], None]:
        """ Returns a List of all summary objects with the given summary type within the timerange if contained. """
        cont_attr_name = self.__get_container_attribute_name(summary_type)
        if cont_attr_name:
            container_of_type = getattr(self, cont_attr_name)
            filtered = list(filter(lambda s: is_date_within_range(s.summary_date, start, end), container_of_type))
            if len(filtered) > 0:
                return filtered
        return None


    
    def get_dict_of_bundles(self) -> dict[int, dict]:
        """
        Building and returning a dictionary which is containing dictionaries for each date. 
        Each inner dictionarys keys are the attributes of all summary objects.
        The keys of the outer dictionary are indices.
        """

        data = dict()
        for index, date in enumerate(self.__dates):
            bundle = self.get_summary_bundle_of_date(date)
            data[index] = bundle
        return data

    def get_summary_bundle_of_date(self, date: str) -> dict:
        """
        Building and returning a dictionary which is containing
        the data from all contained summary types of that date.
        The keys in the dictionary are the attributes of the summary objects.
        """

        date_summaries = []
        for summary_type in self.__contained_summaries:
            date_summary = self.get_summary_of_date(summary_type, date)
            if date_summary:
                date_summaries.append(date_summary)
        
        bundle = dict()
        bundle[SUMMARY_DATE] = date
        for summary in date_summaries:
            summary_type = summary.summary_type
            
            # every attribute we stored in the summary
            for attr in summary.measurement_attributes: 
                if attr == SUMMARY_DATE:
                    continue
                bundle_attr_name = "{}_{}".format(summary_type.name, attr)
                bundle[bundle_attr_name] = getattr(summary, attr)

        return bundle


    def get_values(self, start: str, end: str, summary_type: SummaryType, measurement_name: str, output_as_np_array=True) -> Union[np.array, List]:
        """
        Creating a one dimensional numpy array with one entry for each date from start to end.
        The array is containing the values of the given summary type and measurement.
        If a summary object is not contained, the content will be NaN.
        """

        dates = all_date_strings_between_dates(start, end)
        if output_as_np_array:
            values = np.empty(len(dates))
            values[:] = np.NaN
        else: # output as python list
            values = [None] * len(dates)

        summaries = self.get_summaries_within_timerange(summary_type, start, end)
        summary_iter = iter(summaries)

        current_summary = next(summary_iter)
        always_attribute_error = True

        for index, date in enumerate(dates):
            if current_summary.summary_date == date:

                # value might not be available for that date
                try:
                    value = getattr(current_summary, measurement_name)
                    values[index] = value
                    always_attribute_error = False
                except AttributeError:
                    pass

                # iterator might be at end
                try:
                    current_summary = next(summary_iter)
                except StopIteration:
                    return values

        if always_attribute_error:
            raise AttributeError("No {}-{} avalable in summary objects".format(summary_type.name, measurement_name))

        return values

    def get_missing_subjective_data_days(self) -> List[str]:
        given_dates = []
        for summary_obj in getattr(self, self.__get_container_attribute_name(SummaryType.subjective)):
            date = summary_obj.summary_date
            given_dates.append(date)
        
        missing_dates = sorted(set(self.__dates) - set(given_dates))
        return missing_dates