from django.apps import AppConfig


class ContestsConfig(AppConfig):
    name = 'apps.contests'

    def ready(self):
        import apps.contests.signals
