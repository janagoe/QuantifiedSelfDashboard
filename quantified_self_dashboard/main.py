
import configparser
import json
from summary.summary import *
from summary.summary_container import SummaryContainer
from connector import oura_api_connector
from common.date_helper import *

if __name__ == '__main__':

            
    config = configparser.ConfigParser()
    config.read("config.ini")
    access_token = config["auth"].get('access-token')

    conn = oura_api_connector.OuraApiConnector(access_token)

    s = SummaryContainer(containing_subjective=False)
    succ = s.load([conn], "2021-03-04", "2021-03-10")

    summaries = s.get_summaries_within_timerange(SLEEP, "2021-03-05", "2021-03-07")
    summaries += s.get_summaries_within_timerange(READINESS, "2021-03-05", "2021-03-07")
    summaries += s.get_summaries_within_timerange(ACTIVITY, "2021-03-05", "2021-03-07")
    summaries += s.get_summaries_within_timerange(BEDTIME, "2021-03-05", "2021-03-07")

    for i in ss:
        print(i)
