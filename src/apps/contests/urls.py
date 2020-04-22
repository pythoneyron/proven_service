# -*- coding:utf-8 -*-
from django.urls import path

from apps.accounts.decorators import expert_rights
from apps.contests.views import ContentsListView, TeamListView, FinalResultsListView, ResultsUpdateView,\
    FinalResultsByCriteriaListView, RenderToPDFView, HistoryChangesAssessmentsView

app_name = 'contests'

urlpatterns = [
    path('final_results/', FinalResultsListView.as_view(), name='final_results'),
    path('<int:contest_id>/teams/', expert_rights(TeamListView.as_view()), name='teams'),
    path('<int:contest_id>/team/<int:team_id>/results_team/', expert_rights(ResultsUpdateView.as_view()),
         name='results_team'),
    path('<int:contest_id>/final_results_teams/', FinalResultsByCriteriaListView.as_view(), name='final_results_teams'),
    path('<int:contest_id>/history_changes/', HistoryChangesAssessmentsView.as_view(),
         name='history_changes'),
    path('<int:contest_id>/render_to_pdf/', RenderToPDFView.as_view(), name='render_to_pdf'),
    path('', expert_rights(ContentsListView.as_view()), name='contests'),
]
