from django.db import models
from simple_history.models import HistoricalRecords

from apps.accounts.models import User


class Contests(models.Model):
    """ Конкурсы """
    user = models.ManyToManyField(User, verbose_name='Пользователь')
    title = models.CharField(verbose_name='Наименование', max_length=255)
    start_date = models.DateTimeField(verbose_name='Дата Начала')
    end_date = models.DateTimeField(verbose_name='Дата Окончания')

    class Meta:
        verbose_name = 'Конкурс'
        verbose_name_plural = 'Конкурсы'

    def get_start_date_to_string(self):
        return self.start_date.strftime('%d-%m-%Y')

    def get_end_date_to_string(self):
        return self.end_date.strftime('%d-%m-%Y')

    def get_start_time_to_string(self):
        return self.start_date.strftime('%H:%M:%S')

    def get_end_time_to_string(self):
        return self.end_date.strftime('%H:%M:%S')

    def __str__(self):
        return f'{self.pk} - {self.title}'


class Team(models.Model):
    """ Команды """
    title = models.CharField(verbose_name='Название', max_length=255)
    address = models.CharField(verbose_name='Адрес', max_length=255)
    additionally = models.CharField(verbose_name='Дополнительно', max_length=255, blank=True, null=True)
    contest = models.ManyToManyField(Contests, verbose_name='Конкурс')
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True, upload_to='team_images/')

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return f'{self.pk} - {self.title}'


class PlaceTaken(models.Model):
    """ Занятые места """
    place = models.PositiveIntegerField(verbose_name='Место', blank=True, null=True)
    contest = models.ForeignKey(Contests, verbose_name='Конкурс', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, verbose_name='Команда', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Занятое место'
        verbose_name_plural = 'Занятые места'

    def __str__(self):
        return f'{self.place} - место. Конкурса - {self.contest.title}. Команды - {self.team.title}'


class Criteria(models.Model):
    """ Критерии """
    title = models.CharField(verbose_name='Название', max_length=255)
    coefficient = models.FloatField(verbose_name='Коэффициент')
    contest = models.ForeignKey(Contests, verbose_name='Конкурс', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Критерия'
        verbose_name_plural = 'Критерии'

    def __str__(self):
        return f'Критерия - {self.title}. Конкурса - {self.contest.title}'


class Assessment(models.Model):
    """ Оценки """
    point = models.PositiveIntegerField(verbose_name='Оценка', default=0)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, verbose_name='Команда', on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, verbose_name='Критерия', on_delete=models.CASCADE)
    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'Оценка - {self.point}. По критерию - {self.criteria.title}. Команды - {self.team.title}'


class Penalty(models.Model):
    """ Штрафы """
    point = models.FloatField(verbose_name='Штраф', default=0)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, verbose_name='Команда', on_delete=models.CASCADE)
    contest = models.ForeignKey(Contests, verbose_name='Конкурс', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Штраф'
        verbose_name_plural = 'Штрафы'

    def __str__(self):
        return f'Штраф - {self.point} баллов. Команды - {self.team.title}'


class NumberChanges(models.Model):
    """ Количество изменений """
    count_changes = models.PositiveIntegerField(default=0, blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, verbose_name='Оценка', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Количество изменений'
        verbose_name_plural = 'Количество изменений'

    def __str__(self):
        return f'{self.count_changes} - изменений по критерию - {self.assessment.criteria.title}.'
