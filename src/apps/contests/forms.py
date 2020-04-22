from django import forms
from django.forms.models import modelformset_factory, BaseModelFormSet

from apps.accounts.models import User
from apps.accounts.choices import RoleUser
from apps.contests.models import Criteria, NumberChanges, Assessment


class CriteriaForm(forms.ModelForm):
    assessment = forms.IntegerField(required=True)
    user_id = forms.IntegerField(required=True)
    team_id = forms.IntegerField(required=True)

    class Meta:
        model = Criteria
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(CriteriaForm, self).__init__(*args, **kwargs)

    def clean(self):
        user_id = self.cleaned_data.get('user_id')
        assessment = self.cleaned_data.get('assessment')
        team_id = self.cleaned_data.get('team_id')
        criteria_obj = self.cleaned_data.get('id')
        user = User.objects.get(id=user_id)

        if user.role == RoleUser.Expert:
            assessment_obj = Assessment.objects.filter(user_id=user_id, team_id=team_id, criteria=criteria_obj).first()

            if assessment and 1 <= assessment <= 5:

                if assessment_obj and assessment_obj.point != assessment:
                    assessment_obj.point = assessment
                    assessment_obj.save()
                else:
                    assessment_obj = Assessment.objects.create(
                        user_id=user_id, team_id=team_id, criteria=criteria_obj, point=assessment
                    )

                obj, created = NumberChanges.objects.get_or_create(assessment=assessment_obj, user_id=user_id)
                if obj.count_changes >= 3:
                    self._errors["assessment"] = self.error_class(
                        ['Достигнуто максимальное число изменений критерии']
                    )
                else:
                    obj.count_changes += 1
                    obj.save()
            else:
                self._errors["assessment"] = self.error_class(['Оценка должна быть в диапазоне от 1 до 5'])
        else:
            self._errors["assessment"] = self.error_class(['Редактирование доступно только эксперту'])
        return self.cleaned_data


class BaseCriteriaFormSet(BaseModelFormSet):
    def __init__(self, *args, contest_id=None, **kwargs):
        self.contest_id = contest_id
        super().__init__(*args, **kwargs)
        self.queryset = Criteria.objects.filter(contest__id=self.contest_id)


CriteriaFormSet = modelformset_factory(Criteria, form=CriteriaForm, formset=BaseCriteriaFormSet, fields='__all__', extra=0)
