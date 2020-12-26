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
    days_of_week = forms.CharField(label='Meal Days', max_length=100)
    max_prep_time = forms.ChoiceField(choices=PREP_TIMES, required=False)
    dietary_restrictions = forms.MultipleChoiceField(choices=DIETARY_RESTRICTIONS, required=False)
    instant_pot = forms.BooleanField(label="Instant Pot?", required=False)
    ingredients_included = forms.CharField(label='Ingredients Included', max_length=1000, required=False)
    ingredients_excluded = forms.CharField(label='Ingredients Excluded', max_length=1000, required=False)
