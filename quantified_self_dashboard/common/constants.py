from enum import Enum



SUMMARY_DATE = 'summary_date'


# SummaryTypes ------------------------------

SummaryType = Enum(
    value = 'SummaryType',
    names = [
        ('sleep', 0),
        ('readiness', 1),
        ('activity', 2),
        ('bedtime', 3),
        ('userinfo', 4),
        ('subjective', 5),
    ]
)



# Periodicities ------------------------------

Periodicity = Enum(
    value ='Periodictiy',
    names = [
        ('daily', 0),
        ('weekly', 1),
        ('monthly', 2),
        ('yearly', 3),
        ('weekdays', 4)
    ]
)


# Units ------------------------------

Unit = Enum(
    value = 'Unit',
    names = [
        ('undefined', 0),
        ('seconds', 1),
        ('minutes', 2),
        ('hours', 3),
        ('heart_rate_variablity', 4),
        ('heart_rate', 5),
        ('score', 6),
        ('celsius', 7),
        ('raw_data', 8),
        ('time_of_day', 9),
    ]
)

UnitsAnnotationText = {
    Unit.seconds: "Undefined", 
    Unit.seconds: "Time in s", 
    Unit.minutes: "Time in min", 
    Unit.hours: "Time in h", 
    Unit.heart_rate_variablity: "HRV", 
    Unit.heart_rate: "HR", 
    Unit.score: "Score", 
    Unit.celsius: "°C", 
    Unit.raw_data: "Raw", 
    Unit.time_of_day: "Time of Day", 
}


# AnalysisTypes ------------------------------

AnalysisType = Enum(
    value = 'AnalysisType',
    names = [

        ("scores_daily", 1),
        ("scores_weekly", 2),
        ("scores_monthly", 3),
        ("scores_weekdays", 4),
        ("sleep_durations_daily", 5),
        ("sleep_durations_weekly", 6),
        ("sleep_durations_monthly", 7),
        ("sleep_durations_weekdays", 8),
        ("bedtimes_daily", 9),
        ("bedtimes_weekly", 10),
        ("bedtimes_monthly", 11),
        ("bedtimes_weekdays", 12),
        ("recovery_indicators_daily", 13),
        ("recovery_indicators_weekly", 14),
        ("recovery_indicators_monthly", 15),
        ("recovery_indicators_weekdays", 16),
        ("sleep_score_distribution", 17),
        ("readiness_score_distribution", 18),
        ("activity_score_distribution", 19),
    ]
)

all_analysis_types = [
    AnalysisType.scores_daily,
    AnalysisType.scores_weekly,
    AnalysisType.scores_monthly,
    AnalysisType.scores_weekdays,
    AnalysisType.sleep_durations_daily,
    AnalysisType.sleep_durations_weekly,
    AnalysisType.sleep_durations_monthly,
    AnalysisType.sleep_durations_weekdays,
    AnalysisType.bedtimes_daily,
    AnalysisType.bedtimes_weekly,
    AnalysisType.bedtimes_monthly,
    AnalysisType.bedtimes_weekdays,
    AnalysisType.recovery_indicators_daily,
    AnalysisType.recovery_indicators_weekly,
    AnalysisType.recovery_indicators_monthly,
    AnalysisType.recovery_indicators_weekdays,
    AnalysisType.sleep_score_distribution,
    AnalysisType.readiness_score_distribution,
    AnalysisType.activity_score_distribution,
]


# SubjectiveMeasurementTypes ------------------------------

SubjectiveMeasurementType = Enum(
    value = 'SubjectiveMeasurementType',
    names = [
        ('bool', 0),
        ('percentage', 1),
        ('number', 2),
    ]
)

