from django import forms


class OptionsForm(forms.Form):
    days_of_week = forms.CharField(label='Your name', max_length=100)
    max_prep_time = forms.Select(choices={("short", "medium", "long")})
    ingredients_included = forms.CharField(label='Your name', max_length=1000)
    ingredients_excluded = forms.CharField(label='Your name', max_length=1000)