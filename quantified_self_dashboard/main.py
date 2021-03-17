
import configparser
import json
from summary.summary import *
from summary.summary_container import SummaryContainer
from connector import oura_api_connector, gui_input_connector
from common.date_helper import *


from ast import literal_eval

if __name__ == '__main__':

            
    config = configparser.ConfigParser()
    config.read("config.ini")
    access_token = config["oura.auth"].get('access-token')

    subj_conf = config['subective.summary.data']
    subjective_tracking_items = list(subj_conf.items())

    conn_oura = oura_api_connector.OuraApiConnector(access_token)
    conn_sub = gui_input_connector.GuiInputConnector(subjective_tracking_items)

    s = SummaryContainer()
    succ = s.load([conn_oura, conn_sub], "2021-03-04", "2021-03-10")

    summaries = s.get_summaries_within_timerange(SLEEP, "2021-03-05", "2021-03-07")
    summaries += s.get_summaries_within_timerange(READINESS, "2021-03-05", "2021-03-07")
    summaries += s.get_summaries_within_timerange(ACTIVITY, "2021-03-05", "2021-03-07")
    summaries += s.get_summaries_within_timerange(BEDTIME, "2021-03-05", "2021-03-07")
    summaries += s.get_summaries_within_timerange(SUBJECTIVE, "2021-03-05", "2021-03-07")

    for i in summaries:
        print(i)
