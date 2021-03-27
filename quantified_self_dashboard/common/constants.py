from enum import Enum


# TODO: move into enum
SLEEP = 'sleep'
READINESS = 'readiness'
ACTIVITY = 'activity'
BEDTIME = 'bedtime'
USERINFO = 'userinfo'
SUBJECTIVE = 'subjective'

# TODO: move into enum
TYPE_BOOL = 'bool'
TYPE_PERCENTAGE = 'percentage'
TYPE_NUMBER = 'number'



Periodicity = Enum(
    value ='Periodictiy',
    names = [
        ('daily', 0),
        ('weekly', 1),
        ('monthly', 2),
        ('yearly', 3)
    ]
)

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
}


AnalysisType = Enum(
    value = 'AnalysisType',
    names = [
        ("test", 0)
    ]
)
