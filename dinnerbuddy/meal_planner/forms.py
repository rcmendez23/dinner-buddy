from django import forms


class OptionsForm(forms.Form):
    days_of_week = forms.CharField(label='Your name', max_length=100)
    your_name = forms.CharField(label='Your name', max_length=100)