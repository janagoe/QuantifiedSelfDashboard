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
    AnalysisType.sleep_durations: "Sleep Times",
    AnalysisType.sleep_score_distribution: "Sleep Score Distribution from {} until {}",
    AnalysisType.readiness_score_distribution: "Readiness Score Distribution from {} until {}",
    AnalysisType.activity_score_distribution: "Activity Score Distribution from {} until {}",
    AnalysisType.bedtimes_daily: "Daily Bedtimes from {} until {}"
}

analysis_type_summary_type_measurement_tuples = {
    AnalysisType.scores_daily: [(SummaryType.sleep, "score"), (SummaryType.readiness, "score"), (SummaryType.activity, "score")],
    AnalysisType.sleep_durations: [(SummaryType.sleep, "deep"), (SummaryType.sleep, "rem"), (SummaryType.sleep, "light"), (SummaryType.sleep, "awake")],
    AnalysisType.sleep_score_distribution: [(SummaryType.sleep, "score")],
    AnalysisType.readiness_score_distribution: [(SummaryType.readiness, "score")],
    AnalysisType.activity_score_distribution: [(SummaryType.activity, "score")],
    AnalysisType.bedtimes_daily: [(SummaryType.sleep, "bedtime_start_delta"), (SummaryType.sleep, "duration")],
}



analysis_type_periodicity = {
    AnalysisType.scores_daily: Periodicity.daily,
    AnalysisType.sleep_durations: Periodicity.daily,
    AnalysisType.sleep_score_distribution: Periodicity.daily,
    AnalysisType.readiness_score_distribution: Periodicity.daily,
    AnalysisType.activity_score_distribution: Periodicity.daily,
    AnalysisType.bedtimes_daily: Periodicity.daily,
}
default_periodicity = Periodicity.daily


analysis_type_plot_kwargs = {
    AnalysisType.scores_daily: {'yaxis_to_zero': True},
    AnalysisType.sleep_durations: {'yaxis_to_zero': True},
}



analysis_type_plot_type = {
    AnalysisType.scores_daily: PlotType.lines,
    AnalysisType.sleep_durations: PlotType.bar_chart,
    AnalysisType.sleep_score_distribution: PlotType.histogram,
    AnalysisType.readiness_score_distribution: PlotType.histogram,
    AnalysisType.activity_score_distribution: PlotType.histogram,
    AnalysisType.bedtimes_daily: PlotType.time_period,
}
default_plot_type = PlotType.lines

