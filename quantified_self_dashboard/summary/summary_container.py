from summary.summary import *
from common.date_helper import all_date_strings_between_dates, is_date_within_range
from common.constants import *
from typing import List
from connector.abstract_connector import AbstractConnector
import numpy as np


class SummaryContainer:
    """
    Container for Summary objects,
    needed for making plots or saving data. 
    """

    __possible_summaries = [SLEEP, READINESS, ACTIVITY, BEDTIME, SUBJECTIVE]


    def __init__(self, containing_sleep=True, containing_readiness=True, containing_activity=True, containing_bedtime=True, containing_subjective=True):
        contained = [containing_sleep, containing_readiness, containing_activity, containing_bedtime, containing_subjective]
        self.__prepare_attributes(contained)

    def __prepare_attributes(self, contained: List[bool]):
        self.__contained_summaries = []
        self.__summary_container_attribute_names = []
        self.__summary_required_dates_attribute_names = []

        # checking which summary types we want to use this container for
        for summary_str, summary_contained in zip(self.__possible_summaries, contained):
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

    def __load_via_connector(self, connector):

        common_summary_types = list(set.intersection(set(self.__contained_summaries), set(connector.supported_summary_types)))

        for summary_type, container_attr, required_dates_attr in zip(self.__contained_summaries, self.__summary_container_attribute_names, self.__summary_required_dates_attribute_names):
            if summary_type not in common_summary_types:
                continue
            
            required_dates_for_summary_type = getattr(self, required_dates_attr)
            summary_class = get_summary_class_from_str(summary_type)

            still_required_dates = []
            new_summary_objects = []
            old_summary_objects = getattr(self, container_attr)

            for date in required_dates_for_summary_type:
                summary_date_obj = summary_class()
                success = summary_date_obj.load(connector, date)
                if not success:
                    still_required_dates.append(date)
                else:
                    new_summary_objects.append(summary_date_obj)
            
            setattr(self, required_dates_attr, still_required_dates)
            setattr(self, container_attr, new_summary_objects + old_summary_objects)
        

    def load(self, connectors: List[AbstractConnector], start: str, end: str): 
        dates = all_date_strings_between_dates(start, end)
        if not len(dates) > 0:
            raise AttributeError()

        # in beginning all dates are required for all summary types
        for required_dates_attr in self.__summary_required_dates_attribute_names:
            setattr(self, required_dates_attr, dates)

        # letting each connector try to load everything required
        for conn in connectors:
            self.__load_via_connector(conn)

        # sort by date
        # assuming the dates are ordered lexicographically aswell
        for summary_type in self.__contained_summaries:
            container_attr_name = self.__get_container_attribute_name(summary_type)
            container_of_type = getattr(self, container_attr_name)
            sorted_container = sorted(container_of_type, key=lambda s: s.summary_type)
            setattr(self, container_attr_name, sorted_container)

        # checking if all required dates got loaded
        for req_attr in self.__summary_required_dates_attribute_names:
            req_dates = getattr(self, req_attr)
            if len(req_dates) > 0:
                print("Not all summaries were able to load. Is the access token set?")
                return False

        self.__dates = dates
        return True

    def __get_container_attribute_name(self, summary_type: str):
        for sum_type, cont_attr in zip(self.__contained_summaries, self.__summary_container_attribute_names):
            if sum_type == summary_type:
                return cont_attr
        return None
    
    def get_summary_of_date(self, summary_type: str, date: str):
        cont_attr_name = self.__get_container_attribute_name(summary_type)
        if cont_attr_name:
            container_of_type = getattr(self, cont_attr_name)
            filtered = list(filter(lambda s: s.summary_date == date, container_of_type))
            if len(filtered) > 0:
                return filtered[0]
            return None
        return None

    def get_summaries_within_timerange(self, summary_type: str, start: str, end: str):
        container_of_type = getattr(self, self.__get_container_attribute_name(summary_type))
        filtered = list(filter(lambda s: is_date_within_range(s.summary_date, start, end), container_of_type))
        if len(filtered) > 0:
            return filtered
        return None

    def get_summary_bundle_of_date(self, date: str) -> dict():
        date_summaries = []
        for summary_type in self.__contained_summaries:
            date_summary = self.get_summary_of_date(summary_type, date)
            if date_summary:
                date_summaries.append(date_summary)
        
        bundle = dict()
        bundle['summary_date'] = date
        for summary in date_summaries:
            summary_type = summary.summary_type
            
            # every attribute we stored in the summary
            for attr in summary.measurement_attributes: 
                if attr == 'summary_date':
                    continue
                bundle_attr_name = "{}_{}".format(summary_type, attr)
                bundle[bundle_attr_name] = getattr(summary, attr)

        return bundle

    def get_dict_of_bundles(self) -> dict:
        data = dict()
        for index, date in enumerate(self.__dates):
            bundle = self.get_summary_bundle_of_date(date)
            data[index] = bundle
        return data

    def get_np_array(self, start, end, summary_type, attr_type) -> np.array:
        dates = all_date_strings_between_dates(start, end)
        value_array = np.empty(len(dates))
        value_array[:] = np.NaN

        summaries = self.get_summaries_within_timerange(summary_type, start, end)
        # assumption: summaries are ordered by date

        summary_iter = iter(summaries)

        current_summary = next(summary_iter)
        for index, date in enumerate(dates):
            if current_summary.summary_date == date:
                value = getattr(current_summary, attr_type)
                value_array[index] = value
                try:
                    current_summary = next(summary_iter)
                except StopIteration:
                    return value_array

        return value_array


    def __iter__(self):
        self.__current_iter_date_index = 0
        return self

    def __next__(self):
        if self.__current_iter_date_index < len(self.__dates):
            current_date = self.__dates[self.__current_iter_date_index]
            self.__current_iter_date_index += 1
            return self.get_summary_bundle_of_date(current_date)
        else:
            raise StopIteration()

