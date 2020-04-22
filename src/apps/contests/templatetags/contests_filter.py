# -*- coding:utf-8 -*-

from django import template

from apps.contests.utils import del_max_and_min_value, get_total_score_average, get_deleted_value_with_data_user,\
    get_points

register = template.Library()


@register.filter
def get_max_deleted_value(criteria, team):
    return get_deleted_value_with_data_user(criteria, team)[0]


@register.filter
def get_max_deleted_user(criteria, team):
    return get_deleted_value_with_data_user(criteria, team)[-1]


@register.filter
def get_min_deleted_value(criteria, team):
    return get_deleted_value_with_data_user(criteria, team, min_value=True)[0]


@register.filter
def get_min_deleted_user(criteria, team):
    return get_deleted_value_with_data_user(criteria, team, min_value=True)[-1]


@register.filter
def get_assessment(criteria_id, assessment_obj):
    """ Получить оценку """
    assessment = assessment_obj.filter(criteria_id=criteria_id).first()
    if assessment:
        return assessment.point
    return 0


@register.filter
def get_count_changes(criteria_id, assessment_obj):
    """ Получить количество изменений """
    assessment = assessment_obj.filter(criteria_id=criteria_id).first()
    if assessment:
        number_changes = assessment.numberchanges_set.first()
        if number_changes:
            return number_changes.count_changes
    return 0


@register.filter
def get_average_value_by_criteria(team, criteria_obj):
    """ Получить среднее значениее баллов критерии всех пользователей """
    coefficient = criteria_obj.coefficient
    assessments = criteria_obj.assessment_set.filter(team=team).values_list('point')
    points = [assessment[0] * coefficient for assessment in assessments]
    del_max_and_min_value(points)
    len_points = len(points)
    return round(sum(points) / len_points, 2) if sum(points) else 0


@register.filter
def get_place(places_qs, contest):
    """ Получить место в конкурса """
    place_obj = places_qs.filter(contest=contest).first()
    if place_obj:
        return place_obj.place
    return '-'


@register.filter
def get_total_penalty(team, contest):
    """ Получить штрафы всех пользователей """
    penalty = sum([penalty.point for penalty in team.penalty_set.filter(contest=contest)])
    if penalty:
        return penalty
    return 0


@register.filter
def filter_queryset_by_team(assessments_history, team):
    """ Отфильтровать оценки по команде """
    if assessments_history:
        assessments_history = assessments_history.filter(team=team)
    return assessments_history


@register.filter
def filter_queryset_by_user(assessments_history, user):
    """ Отфильтровать оценки по пользователю """
    if assessments_history:
        assessments_history = assessments_history.filter(user=user)
    return assessments_history


@register.filter
def get_total_score_all_average_criteria(team, contest):
    """ Получить сумму всех баллов критерий со средним значением """
    return get_total_score_average(team, contest)


@register.filter
def get_total_score_all_average_criteria_with_penalty(team, contest):
    """ Получить сумму всех баллов критерий со средним значением с учетом штрафа """
    return get_total_score_average(team, contest, with_penalty=True)


@register.filter
def get_total_score_all_average_criteria_without_del_min_max(team, contest):
    """ Получить сумму всех баллов критерий со средним значением
    без учета удаления максимального и минимального зачение """
    return get_total_score_average(team, contest, del_max_min=False)


@register.filter
def get_total_score_all_average_criteria_without_del_min_max_and_not_coefficient(team, contest):
    """ Получить сумму всех баллов критерий со средним значением
    без учета удаления максимального и минимального значения и коэффициента """
    return get_total_score_average(team, contest, del_max_min=False, with_coefficient=False)


@register.filter
def get_total_all_values(team, contest):
    """ Получить сумму всех баллов """
    return round(sum(get_points(team, contest)), 2)
