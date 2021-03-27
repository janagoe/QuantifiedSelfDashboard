from common.constants import *



identity = lambda x: x

seconds_to_hours = lambda x: x / 3600 



# attribute_name: [display_transform x->x, original_type, transformed_type, original_unit: str, transformed_unit: str, title: str]

sleep_transform = {

    "total": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Total Sleep Time"],
    "awake": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Awake Sleep Time"],
    "rem": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "REM Sleep Time"],
    "light": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Light Sleep Time"],
    "deep": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Deep Sleep Time"],
    "duration": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Sleep Duration"],

    "bedtime_end_delta": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Bedtime End Delta"],
    "bedtime_start_delta": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Bedtime Start Delta"],
    "midpoint_at_delta": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Sleep Mitpoint Delta"],
    "midpoint_time": [seconds_to_hours, int, float, Unit.seconds, Unit.hours, "Sleep Mindpoint"],

    "efficiency": [identity, int, int, Unit.score, Unit.score, "Sleep Efficiency"],
    "score": [identity, int, int, Unit.score, Unit.score, "Sleep Unit.score"],
    "score_alignment": [identity, int, int, Unit.score, Unit.score, "Sleep Unit.score Alignment"],
    "score_deep": [identity, int, int, Unit.score, Unit.score, "Deep Sleep Unit.score"],
    "score_disturbances": [identity, int, int, Unit.score, Unit.score, "Sleep Disturbances Unit.score"],
    "score_efficiency": [identity, int, int, Unit.score, Unit.score, "Sleep Efficiency Unit.score"],
    "score_latency": [identity, int, int, Unit.score, Unit.score, "Sleep Latency Unit.score"],
    "score_rem": [identity, int, int, Unit.score, Unit.score, "REM Sleep Unit.score"],
    "score_total": [identity, int, int, Unit.score, Unit.score, "Total Sleep Unit.score"],

    "rmssd": [identity, int, int, Unit.raw_data, Unit.raw_data, "RMSSD"],
    "hr_average": [identity, float, float, Unit.raw_data, Unit.raw_data, "Average Heart Rate"],
    "hr_lowest": [identity, int, int, Unit.raw_data, Unit.raw_data, "Lowest Heart Rate"],
    "temperature_delta": [identity, int, int, Unit.celsius, Unit.celsius, "Temperature Delta"],
    "temperature_deviation": [identity, int, int, Unit.celsius, Unit.celsius, "Temperature Deviation"],
    "temperature_trend_deviation": [identity, int, int, Unit.raw_data, Unit.raw_data, "Temperature Trend Deviation"],

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






