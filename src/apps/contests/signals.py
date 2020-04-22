from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.contests.models import Assessment, Penalty
from apps.contests.utils import count_place


@receiver(post_save, sender=Assessment)
def count_place_by_assessment(sender, instance, **kwargs):
    count_place()


@receiver(post_save, sender=Penalty)
def count_place_by_penalty(sender, instance, **kwargs):
    count_place()
