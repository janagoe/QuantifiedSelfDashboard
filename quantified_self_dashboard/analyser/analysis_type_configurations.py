from common.constants import *


PlotType = Enum(
    value = 'PlotType',
    names = [
        ('time_period', 0),
        ('lines', 1),
        ('bar_chart', 2),
        ('histogram', 3),
    ]
)

analysis_type_plot_titles_template = {
    AnalysisType.scores_daily: "Daily Scores",
    AnalysisType.scores_weekly: "Weekly Scores",
    AnalysisType.scores_monthly: "Monthly Scores",
    AnalysisType.scores_weekdays: "Scores by Weekdays",

    AnalysisType.sleep_durations_daily: "Sleep Times",
    AnalysisType.sleep_durations_weekly: "Weekly Sleep Times",
    AnalysisType.sleep_durations_monthly: "Monthly Sleep Times",
    AnalysisType.sleep_durations_weekdays: "Sleep Times by Weekday",

    AnalysisType.bedtimes_daily: "Daily Bedtimes from {} until {}",
    AnalysisType.bedtimes_weekly: "Weekly Bedtimes from {} until {}",
    AnalysisType.bedtimes_monthly: "Monthly Bedtimes from {} until {}",
    AnalysisType.bedtimes_weekdays: "Bedtimes by Weekday from {} until {}",

    AnalysisType.recovery_indicators_daily: "Daily Recovery Indicators",
    AnalysisType.recovery_indicators_weekly: "Weekly Recover Indicators",
    AnalysisType.recovery_indicators_monthly: "Monthly Recovery Indicators",
    AnalysisType.recovery_indicators_weekdays: "Recovery Indicators by Weekday",

    AnalysisType.sleep_score_distribution: "Sleep Score Distribution from {} until {}",
    AnalysisType.readiness_score_distribution: "Readiness Score Distribution from {} until {}",
    AnalysisType.activity_score_distribution: "Activity Score Distribution from {} until {}",
}

analysis_type_summary_type_measurement_tuples = {
    AnalysisType.scores_daily: [(SummaryType.sleep, "score"), (SummaryType.readiness, "score"), (SummaryType.activity, "score")],
    AnalysisType.scores_weekly: [(SummaryType.sleep, "score"), (SummaryType.readiness, "score"), (SummaryType.activity, "score")],
    AnalysisType.scores_monthly: [(SummaryType.sleep, "score"), (SummaryType.readiness, "score"), (SummaryType.activity, "score")],
    AnalysisType.scores_weekdays: [(SummaryType.sleep, "score"), (SummaryType.readiness, "score"), (SummaryType.activity, "score")],

    AnalysisType.sleep_durations_daily: [(SummaryType.sleep, "deep"), (SummaryType.sleep, "rem"), (SummaryType.sleep, "light"), (SummaryType.sleep, "awake")],
    AnalysisType.sleep_durations_weekly: [(SummaryType.sleep, "deep"), (SummaryType.sleep, "rem"), (SummaryType.sleep, "light"), (SummaryType.sleep, "awake")],
    AnalysisType.sleep_durations_monthly: [(SummaryType.sleep, "deep"), (SummaryType.sleep, "rem"), (SummaryType.sleep, "light"), (SummaryType.sleep, "awake")],
    AnalysisType.sleep_durations_weekdays: [(SummaryType.sleep, "deep"), (SummaryType.sleep, "rem"), (SummaryType.sleep, "light"), (SummaryType.sleep, "awake")],

    AnalysisType.bedtimes_daily: [(SummaryType.sleep, "bedtime_start_delta"), (SummaryType.sleep, "duration")],
    AnalysisType.bedtimes_weekly: [(SummaryType.sleep, "bedtime_start_delta"), (SummaryType.sleep, "duration")],
    AnalysisType.bedtimes_monthly: [(SummaryType.sleep, "bedtime_start_delta"), (SummaryType.sleep, "duration")],
    AnalysisType.bedtimes_weekdays: [(SummaryType.sleep, "bedtime_start_delta"), (SummaryType.sleep, "duration")],

    AnalysisType.recovery_indicators_daily: [(SummaryType.sleep, 'hr_lowest'), (SummaryType.sleep, 'rmssd')],
    AnalysisType.recovery_indicators_weekly: [(SummaryType.sleep, 'hr_lowest'), (SummaryType.sleep, 'rmssd')],
    AnalysisType.recovery_indicators_monthly: [(SummaryType.sleep, 'hr_lowest'), (SummaryType.sleep, 'rmssd')],
    AnalysisType.recovery_indicators_weekdays: [(SummaryType.sleep, 'hr_lowest'), (SummaryType.sleep, 'rmssd')],

    AnalysisType.sleep_score_distribution: [(SummaryType.sleep, "score")],
    AnalysisType.readiness_score_distribution: [(SummaryType.readiness, "score")],
    AnalysisType.activity_score_distribution: [(SummaryType.activity, "score")],
}

analysis_type_periodicity = {
    AnalysisType.scores_daily: Periodicity.daily,
    AnalysisType.scores_weekly: Periodicity.weekly,
    AnalysisType.scores_monthly: Periodicity.monthly,
    AnalysisType.scores_weekdays: Periodicity.weekdays,

    AnalysisType.sleep_durations_daily: Periodicity.daily,
    AnalysisType.sleep_durations_weekly: Periodicity.weekly,
    AnalysisType.sleep_durations_monthly: Periodicity.monthly,
    AnalysisType.sleep_durations_weekdays: Periodicity.weekdays,

    AnalysisType.bedtimes_daily: Periodicity.daily,
    AnalysisType.bedtimes_weekly: Periodicity.weekly,
    AnalysisType.bedtimes_monthly: Periodicity.monthly,
    AnalysisType.bedtimes_weekdays: Periodicity.weekdays,

    AnalysisType.recovery_indicators_daily: Periodicity.daily,
    AnalysisType.recovery_indicators_weekly: Periodicity.weekly,
    AnalysisType.recovery_indicators_monthly: Periodicity.monthly,
    AnalysisType.recovery_indicators_weekdays: Periodicity.weekdays,

    AnalysisType.sleep_score_distribution: Periodicity.daily,
    AnalysisType.readiness_score_distribution: Periodicity.daily,
    AnalysisType.activity_score_distribution: Periodicity.daily,
}
default_periodicity = Periodicity.daily

analysis_type_plot_kwargs = {
    AnalysisType.scores_daily: {'yaxis_to_zero': True},
    AnalysisType.scores_weekly: {'yaxis_to_zero': True},
    AnalysisType.scores_monthly: {'yaxis_to_zero': True},
    AnalysisType.scores_weekdays: {'yaxis_to_zero': True},

    AnalysisType.sleep_durations_daily: {'yaxis_to_zero': True},
    AnalysisType.sleep_durations_weekly: {'yaxis_to_zero': True},
    AnalysisType.sleep_durations_monthly: {'yaxis_to_zero': True},
    AnalysisType.sleep_durations_weekdays: {'yaxis_to_zero': True},

    AnalysisType.recovery_indicators_daily: {'yaxis_to_zero': True},
    AnalysisType.recovery_indicators_weekly: {'yaxis_to_zero': True},
    AnalysisType.recovery_indicators_monthly: {'yaxis_to_zero': True},
    AnalysisType.recovery_indicators_weekdays: {'yaxis_to_zero': True},
}

analysis_type_plot_type = {
    AnalysisType.scores_daily: PlotType.lines,
    AnalysisType.scores_weekly: PlotType.lines,
    AnalysisType.scores_monthly: PlotType.lines,
    AnalysisType.scores_weekdays: PlotType.lines,

    AnalysisType.sleep_durations_daily: PlotType.bar_chart,
    AnalysisType.sleep_durations_weekly: PlotType.bar_chart,
    AnalysisType.sleep_durations_monthly: PlotType.bar_chart,
    AnalysisType.sleep_durations_weekdays: PlotType.bar_chart,

    AnalysisType.bedtimes_daily: PlotType.time_period,
    AnalysisType.bedtimes_weekly: PlotType.time_period,
    AnalysisType.bedtimes_monthly: PlotType.time_period,
    AnalysisType.bedtimes_weekdays: PlotType.time_period,
    
    AnalysisType.recovery_indicators_daily: PlotType.lines,
    AnalysisType.recovery_indicators_weekly: PlotType.lines,
    AnalysisType.recovery_indicators_monthly: PlotType.lines,
    AnalysisType.recovery_indicators_weekdays: PlotType.lines,

    AnalysisType.sleep_score_distribution: PlotType.histogram,
    AnalysisType.readiness_score_distribution: PlotType.histogram,
    AnalysisType.activity_score_distribution: PlotType.histogram,
}
default_plot_type = PlotType.lines

