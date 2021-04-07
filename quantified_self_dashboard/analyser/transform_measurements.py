import math
import datetime
from typing import Callable
from common.constants import *


identity = lambda x: x
seconds_to_hours = lambda x: x / 3600 if x else None 

seconds_to_hours_in_relation_to_midnight = lambda x: 24 + seconds_to_hours(x) if x else None


def seconds_to_datetime(x):
    time_in_hours = seconds_to_hours(x)
    return time_to_datetime(time_in_hours)


def seconds_to_datetime_in_relation_to_midnight(x):
    time_in_hours = seconds_to_hours_in_relation_to_midnight(x)
    return time_to_datetime(time_in_hours)


def time_to_datetime(x):

    hours = math.floor(x)
    minutes = math.floor( (x - hours) * 60 )

    if hours >= 24:
        hours -= 24

    datetime_obj = datetime.time(hours, minutes, 0)
    return datetime_obj



# attribute_name: [display_transform x->x, original_type, transformed_type, original_unit: str, transformed_unit: str, title: str]
sleep_transform = {

    "total": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Total Sleep Time", True],
    "awake": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Awake Sleep Time", True],
    "rem": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "REM Sleep Time", True],
    "light": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Light Sleep Time", True],
    "deep": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Deep Sleep Time", True],
    "duration": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Sleep Duration", True],

    "bedtime_end_delta": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "End of Sleep Period", True],
    "bedtime_start_delta": [seconds_to_hours_in_relation_to_midnight, int, float, Unit.seconds, Unit.hours, "Start of Sleep Period", True],
    "midpoint_at_delta": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Sleep Midpoint Delta", True],
    "midpoint_time": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Sleep Mindpoint", True],

    "efficiency": [identity, int, int, Unit.score, Unit.score, "Sleep Efficiency", True],
    "score": [identity, int, int, Unit.score, Unit.score, "Sleep Score", True],
    "score_alignment": [identity, int, int, Unit.score, Unit.score, "Sleep Score Alignment", True],
    "score_deep": [identity, int, int, Unit.score, Unit.score, "Deep Sleep Score", True],
    "score_disturbances": [identity, int, int, Unit.score, Unit.score, "Sleep Disturbances Score", True],
    "score_efficiency": [identity, int, int, Unit.score, Unit.score, "Sleep Efficiency Score", True],
    "score_latency": [identity, int, int, Unit.score, Unit.score, "Sleep Latency Score", True],
    "score_rem": [identity, int, int, Unit.score, Unit.score, "REM Sleep Score", True],
    "score_total": [identity, int, int, Unit.score, Unit.score, "Total Sleep Score", True],

    "rmssd": [identity, int, int, Unit.raw_data, Unit.raw_data, "RMSSD", True],
    "hr_average": [identity, float, float, Unit.raw_data, Unit.raw_data, "Average Heart Rate", True],
    "hr_lowest": [identity, int, int, Unit.raw_data, Unit.raw_data, "Lowest Heart Rate", True],
    "temperature_delta": [identity, int, int, Unit.celsius, Unit.celsius, "Temperature Delta", True],
    "temperature_deviation": [identity, int, int, Unit.celsius, Unit.celsius, "Temperature Deviation", True],
    "temperature_trend_deviation": [identity, int, int, Unit.raw_data, Unit.raw_data, "Temperature Trend Deviation", True],
    "breath_average": [identity, float, float, Unit.raw_data, Unit.raw_data, "Breath Average", True],

}

readiness_transform = {

    "score": [identity, int, int, Unit.score, Unit.score, "Readiness Score", True],
    "score_activity_balance": [identity, int, int, Unit.score, Unit.score, "Activity Balance Score", True],
    "score_hrv_balance": [identity, int, int, Unit.score, Unit.score, "Heart Rate Variability Balance Score", True],
    "score_previous_day": [identity, int, int, Unit.score, Unit.score, "Previous Day Readiness Score", True],
    "score_previous_night": [identity, int, int, Unit.score, Unit.score, "Previous Night Sleep Score", True],
    "score_recovery_index": [identity, int, int, Unit.score, Unit.score, "Recovery Index Score", True],
    "score_resting_hr": [identity, int, int, Unit.score, Unit.score, "Resting Heart Rate Score", True],
    "score_sleep_balance": [identity, int, int, Unit.score, Unit.score, "Sleep Balance Score", True],
    "score_temperature": [identity, int, int, Unit.score, Unit.score, "Temperature Score", True],

}


activity_transform = {

    "score": [identity, int, int, Unit.score, Unit.score, "Activity Score", False],
    "average_met": [identity, float, float, Unit.raw_data, Unit.raw_data, "Average MET", False],
    "cal_active": [identity, int, int, Unit.raw_data, Unit.raw_data, "Active Cal", False],
    "cal_total": [identity, int, int, Unit.raw_data, Unit.raw_data, "Total Cal", False],
    "daily_movement": [identity, int, int, Unit.raw_data, Unit.raw_data, "Daily Steps", False],
    "high": [identity, int, int, Unit.raw_data, Unit.raw_data, "High Activity", False],
    "inactive": [identity, int, int, Unit.raw_data, Unit.raw_data, "Inactive", False],
    "low": [identity, int, int, Unit.raw_data, Unit.raw_data, "Low Activity", False],
    "medium": [identity, int, int, Unit.raw_data, Unit.raw_data, "Medium Activity", False],
    "inactivity_alerts": [identity, int, int, Unit.raw_data, Unit.raw_data, "Inactivity Alterts", False],

}


bedtime_transform = {
    "bedtime_window_start": [seconds_to_datetime_in_relation_to_midnight, int, datetime.time, Unit.seconds, Unit.hours, "Bedtime Window Start Time", False],
    "bedtime_window_end": [seconds_to_datetime_in_relation_to_midnight, int, datetime.time, Unit.seconds, Unit.hours, "Bedtime Window End Time", False],
}



subjective_transform = dict()


summary_type_transform = {
    SummaryType.sleep: sleep_transform,
    SummaryType.readiness: readiness_transform,
    SummaryType.activity: activity_transform,
    SummaryType.bedtime: bedtime_transform,
    SummaryType.subjective: subjective_transform,
}

