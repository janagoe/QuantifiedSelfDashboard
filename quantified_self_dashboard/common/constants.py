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
        ('yearly', 3)
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
        ("test", 0),
        ("scores_daily", 1),
        ("bedtimes_daily", 2),
        ("sleep_duration", 3),
        ("sleep_durations", 4),
    ]
)


# SubjectiveMeasurementTypes ------------------------------

SubjectiveMeasurementType = Enum(
    value = 'SubjectiveMeasurementType',
    names = [
        ('bool', 0),
        ('percentage', 1),
        ('number', 2),
    ]
)

