from django.views.generic import ListView, FormView, View
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse

from apps.contests.models import Contests, Team, Criteria, Assessment
from apps.accounts.models import User
from apps.contests.forms import CriteriaFormSet
from apps.contests.utils import render_to_pdf
from apps.accounts.choices import RoleUser


class ContentsListView(ListView):
    model = Contests
    context_object_name = 'contests'
    template_name = 'contests/contests.html'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        self.queryset = super(ContentsListView, self).get_queryset()
        user = self.request.user
        if user.is_authenticated:
            return self.queryset.filter(user=user)
        return self.queryset.none()


class TeamListView(ListView):
    model = Team
    context_object_name = 'teams'
    template_name = 'contests/team.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        contest_id = self.kwargs.get('contest_id')
        if not request.user.contests_set.filter(id=contest_id):
            return redirect(reverse('contests:contests'))
        return super(TeamListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        self.queryset = super(TeamListView, self).get_queryset()
        contest_id = self.kwargs.get('contest_id')
        if contest_id:
            self.queryset = self.queryset.filter(contest__pk=contest_id)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(TeamListView, self).get_context_data(**kwargs)
        contest_id = self.kwargs.get('contest_id')
        context['contest'] = Contests.objects.filter(user__id=self.request.user.id, id=contest_id).first()
        return context


class ResultsUpdateView(FormView):
    model = Criteria
    form_class = CriteriaFormSet
    template_name = 'contests/detail_results.html'

    def dispatch(self, request, *args, **kwargs):
        contest_id = self.kwargs.get('contest_id')
        if not request.user.contests_set.filter(id=contest_id):
            return redirect(reverse('contests:contests'))
        return super(ResultsUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ResultsUpdateView, self).get_form_kwargs()
        contest_id = self.kwargs.get('contest_id')
        kwargs.update({
            'contest_id': contest_id
        })
        return kwargs

    def get_success_url(self):
        team_id = self.kwargs.get('team_id')
        contest_id = self.kwargs.get('contest_id')
        return reverse('contests:results_team', kwargs={'team_id': team_id, 'contest_id': contest_id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(ResultsUpdateView, self).get_context_data(**kwargs)
        team_id = self.kwargs.get('team_id')
        context['team'] = Team.objects.filter(id=team_id).first()
        contest_id = self.kwargs.get('contest_id')
        context['contest'] = Contests.objects.filter(user__id=self.request.user.id, id=contest_id).first()
        context['assessment'] = Assessment.objects.filter(user_id=self.request.user.id, team_id=team_id)
        return context


class HistoryChangesAssessmentsView(ListView):
    model = Assessment
    template_name = 'contests/history_changes.html'

    def get_context_data(self, **kwargs):
        context = super(HistoryChangesAssessmentsView, self).get_context_data(**kwargs)
        contest_id = self.kwargs.get('contest_id')
        context['users'] = User.objects.filter(role=RoleUser.Expert)
        context['teams'] = Team.objects.filter(contest__id=contest_id)
        context['contest'] = Contests.objects.filter(id=contest_id).first()

        assessments = Assessment.objects.filter(criteria__contest_id=contest_id)
        assessments_history = None
        for assessment in assessments:
            if assessments_history:
                assessments_history = assessments_history | assessment.history.all()
            else:
                assessments_history = assessment.history.all()

        context['assessments_history'] = assessments_history
        return context


class FinalResultsListView(ListView):
    model = Contests
    context_object_name = 'contests'
    template_name = 'contests/final_results.html'
    paginate_by = 10

    # def get_queryset(self, **kwargs):
    #     self.queryset = super(FinalResultsListView, self).get_queryset()
    #     user = self.request.user
    #     if user.is_authenticated:
    #         return self.queryset.filter(user=user)
    #     return self.queryset.none()


class FinalResultsByCriteriaListView(ListView):
    model = Team
    context_object_name = 'teams'
    template_name = 'contests/results_by_contests.html'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        self.queryset = super(FinalResultsByCriteriaListView, self).get_queryset()
        contest_id = self.kwargs.get('contest_id')
        if contest_id:
            self.queryset = self.queryset.filter(contest__pk=contest_id)
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(FinalResultsByCriteriaListView, self).get_context_data(**kwargs)
        contest_id = self.kwargs.get('contest_id')
        context['contest'] = Contests.objects.get(id=contest_id)
        context['criteria'] = Criteria.objects.filter(contest_id=contest_id)
        return context


class RenderToPDFView(View):
    model = Contests

    def get(self, request, contest_id):
        """ Генерирование PDF файла из HTML страницы"""

        context = dict()
        context['teams'] = Team.objects.filter(contest__pk=contest_id)
        context['contest'] = Contests.objects.get(id=contest_id)
        context['criteria'] = Criteria.objects.filter(contest_id=contest_id)

        template = 'contests/to_pdf.html'
        pdf = render_to_pdf(template, context)

        if pdf:
            filename = f'contest_{contest_id}.pdf'
            content = 'inline; filename="{}"'.format(filename)

            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = content
            return response

        return HttpResponse(status=404)
