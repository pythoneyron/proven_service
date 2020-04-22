# -*- coding:utf-8 -*-
import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from xhtml2pdf import pisa

from apps.contests.models import Assessment, Contests, PlaceTaken, Criteria


def fetch_pdf_resources(uri, rel):
    if uri.find(settings.MEDIA_URL) != -1:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    elif uri.find(settings.STATIC_URL) != -1:
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
    else:
        path = None
    return path


def render_to_pdf(template_src, context_dict):
    result = BytesIO()
    html = render_to_string(template_src, context_dict)
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='utf-8', link_callback=fetch_pdf_resources)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def del_max_and_min_value(points):
    """ Удаляет одно максимальное и минимальное значение для большей точности """
    if len(points) > 2:
        for val in (max(points), min(points)):
            points.remove(val)


def get_points(team, contest, title=None, with_coefficient=True):
    """ Возвращает сумму балов """
    assessments = Assessment.objects.filter(criteria__contest=contest, team=team)
    if title:
        assessments = assessments.filter(criteria__title=title)
    if with_coefficient:
        return [assessment.point * assessment.criteria.coefficient for assessment in assessments]
    return [assessment.point for assessment in assessments]


def get_list_average_value_all_criteries(team, contest, del_max_min, with_coefficient):
    """ Возвращает список средних значений критерий """
    criteries = Criteria.objects.filter(contest=contest, assessment__team=team)
    temp_title_criteria = set()
    for criteria in criteries:
        temp_title_criteria.add(criteria.title)

    average_value_all_criteries = list()
    for title in temp_title_criteria:
        points = get_points(team, contest, title, with_coefficient)
        if del_max_min:
            del_max_and_min_value(points)
        len_points = len(points)
        average_value_all_criteries.append(sum(points) / len_points if sum(points) else 0)
    return average_value_all_criteries


def get_total_score_average(team, contest, with_penalty=False, del_max_min=True, with_coefficient=True):
    """ Возвращает сумму средних значений критерий с учетом штрафа или без него """
    average_value_all_criteries = get_list_average_value_all_criteries(team, contest, del_max_min, with_coefficient)
    if with_penalty:
        penalty = sum([penalty.point for penalty in team.penalty_set.filter(contest=contest)])
        return round(sum(average_value_all_criteries) - penalty, 2)
    return round(sum(average_value_all_criteries), 2)


def get_deleted_value_with_data_user(criteria, team, min_value=None):
    """
    Возвращает кортеж значение оценки и пользователя
    :param criteria:
    :param team:
    :param min_value:
    :return: tuple:
    """
    assessments = Assessment.objects.filter(team=team, criteria=criteria)
    points = [(assessment.point, assessment.user) for assessment in assessments]
    if points and len(points) > 2:
        if min_value:
            return min(points, key=lambda x: x[0])
        else:
            return max(points, key=lambda x: x[0])
    return 0, 0


def count_place():
    """ Считает занятое место для команды. Вызывается сигналом при редактировании модели Assessment и Penalty """
    for contest in Contests.objects.all():
        all_teams = dict()
        for team in contest.team_set.all():
            penalty = sum([penalty.point for penalty in team.penalty_set.filter(contest=contest)])
            all_teams[team.id] = round(sum(get_list_average_value_all_criteries(
                team, contest, del_max_min=True, with_coefficient=True)), 2) - penalty

        if all_teams:
            for place in range(1, len(all_teams) + 1):
                team_id = max(all_teams, key=lambda key: all_teams[key])
                all_teams.pop(team_id)
                obj, created = PlaceTaken.objects.get_or_create(contest=contest, team_id=team_id)
                obj.place = place
                obj.save()
