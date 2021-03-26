from common.constants import *



identity = lambda x: x

seconds_to_hours = lambda x: x / 3600 



# attribute_name: [display_transform x->x, original_type, transformed_type, original_unit: str, transformed_unit: str, title: str]

sleep_transform = {

    "total": [seconds_to_hours, int, float, SECONDS, HOURS, "Total Sleep Time"],
    "awake": [seconds_to_hours, int, float, SECONDS, HOURS, "Awake Sleep Time"],
    "rem": [seconds_to_hours, int, float, SECONDS, HOURS, "REM Sleep Time"],
    "light": [seconds_to_hours, int, float, SECONDS, HOURS, "Light Sleep Time"],
    "deep": [seconds_to_hours, int, float, SECONDS, HOURS, "Deep Sleep Time"],
    "duration": [seconds_to_hours, int, float, SECONDS, HOURS, "Sleep Duration"],

    "bedtime_end_delta": [seconds_to_hours, int, float, SECONDS, HOURS, "Bedtime End Delta"],
    "bedtime_start_delta": [seconds_to_hours, int, float, SECONDS, HOURS, "Bedtime Start Delta"],
    "midpoint_at_delta": [seconds_to_hours, int, float, SECONDS, HOURS, "Sleep Mitpoint Delta"],
    "midpoint_time": [seconds_to_hours, int, float, SECONDS, HOURS, "Sleep Mindpoint"],

    "efficiency": [identity, int, int, SCORE, SCORE, "Sleep Efficiency"],
    "score": [identity, int, int, SCORE, SCORE, "Sleep Score"],
    "score_alignment": [identity, int, int, SCORE, SCORE, "Sleep Score Alignment"],
    "score_deep": [identity, int, int, SCORE, SCORE, "Deep Sleep Score"],
    "score_disturbances": [identity, int, int, SCORE, SCORE, "Sleep Disturbances Score"],
    "score_efficiency": [identity, int, int, SCORE, SCORE, "Sleep Efficiency Score"],
    "score_latency": [identity, int, int, SCORE, SCORE, "Sleep Latency Score"],
    "score_rem": [identity, int, int, SCORE, SCORE, "REM Sleep Score"],
    "score_total": [identity, int, int, SCORE, SCORE, "Total Sleep Score"],

    "rmssd": [identity, int, int, RAW, RAW, "RMSSD"],
    "hr_average": [identity, float, float, RAW, RAW, "Average {}".format(HR)],
    "hr_lowest": [identity, int, int, RAW, RAW, "Lowest {}".format(HR)],
    "temperature_delta": [identity, int, int, CELSIUS, CELSIUS, "Temperature Delta"],
    "temperature_deviation": [identity, int, int, CELSIUS, CELSIUS, "Temperature Deviation"],
    "temperature_trend_deviation": [identity, int, int, RAW, RAW, "Temperature Trend Deviation"],

}

readiness_transform = dict()
activity_transform = dict()
bedtime_transform = dict()
subjective_transform = dict()


summary_type_transform = {
    SLEEP: sleep_transform,
    READINESS: readiness_transform,
    ACTIVITY: activity_transform,
    BEDTIME: bedtime_transform,
    SUBJECTIVE: subjective_transform,
}






