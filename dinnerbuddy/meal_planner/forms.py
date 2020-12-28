from django import forms


class OptionsForm(forms.Form):
    PREP_TIMES = (("short", "short"),
                  ("medium", "medium"),
                  ("long", "long"))
    DIETARY_RESTRICTIONS = (
        ("vegan", "vegan"),
        ("vegetarian", "vegetarian"),
        ("keto", "keto"),
        ("dairy free", "dairy free"),
        ("gluten free", "gluten free"),
        ("kosher", "kosher"),
        ("halal", "halal"),
        ("paleo", "paleo"))
    days_of_week = forms.CharField(label='Meal Days', max_length=100,
                                   widget=forms.TextInput(attrs={'class': 'form-input'}))
    max_prep_time = forms.ChoiceField(choices=PREP_TIMES, required=False,
                                      widget=forms.Select(attrs={'class': 'form-select'}))
    dietary_restrictions = forms.MultipleChoiceField(choices=DIETARY_RESTRICTIONS, required=False,
                                                     widget=forms.SelectMultiple(attrs={'class': 'form-select'}))
    instant_pot = forms.BooleanField(label="Instant Pot?", required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-switch'}))
    ingredients_included = forms.CharField(label='Ingredients Included', max_length=1000, required=False,
                                           widget=forms.TextInput(attrs={'class': 'form-input'}))
    ingredients_excluded = forms.CharField(label='Ingredients Excluded', max_length=1000, required=False,
                                           widget=forms.TextInput(attrs={'class': 'form-input'}))
