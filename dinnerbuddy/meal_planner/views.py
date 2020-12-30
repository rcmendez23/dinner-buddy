from django.shortcuts import render
from AllRecipes.AllRecipes import AllRecipes
from .forms import OptionsForm
import random

NON_DINNER_KEYWORDS = ['choco', 'cookie', 'muffin', 'brownie', 'cake', 'meringue', 'biscuit', 'scone', 'tiramisu',
                       'caramel', 'popcorn', 'fill', 'guac', 'gravy', 'sauce', 'salsa', 'pesto', 'pudding', 'seasoning',
                       'edamame', 'fruit', 'banana', 'bread', 'bar', 'margarita', 'sangria', 'coffee', 'cider', 'smoothie',
                       'ice cream', 'crisps', 'apple pie']


def dinner_recipe(recipe_name):
    recipe_name = recipe_name.lower()
    keywords_in_name = list(filter(lambda x: x in recipe_name, NON_DINNER_KEYWORDS))
    return len(keywords_in_name) == 0


def meal_planner(request):
    if request.method == "GET":
        options_form = OptionsForm()
        return render(request, "meal_planner/meal_planner.html",
                      context={"state": "no_results", "options_form": options_form})

    if request.method == "POST":
        options_form = OptionsForm(request.POST)

        if options_form.is_valid():
            keywords = []
            cleaned_form_data = options_form.cleaned_data
            if cleaned_form_data['instant_pot']:
                keywords.append("instant pot")
            days_of_week = request.POST.getlist('days_of_week')
            dietary_restrictions = cleaned_form_data['dietary_restrictions']
            keywords += dietary_restrictions
            ingredients_excluded = cleaned_form_data['ingredients_excluded']
            ingredients_included = cleaned_form_data['ingredients_included']

            query_options = {
                "wt": ",".join(keywords),  # Query keywords
                "ingIncl": ingredients_included,  # 'Must be included' ingredients (optional)
                "ingExcl": ingredients_excluded,  # 'Must not be included' ingredients (optional)
                "sort": "re"  # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
            }
            query_result = AllRecipes.search(query_options)

            recipes = []

            # Get :
            num_meals = len(days_of_week)
            i = 0
            count = 0
            while count < num_meals:
                main_recipe_url = query_result[i]['url']
                recipe = AllRecipes.get(main_recipe_url)
                if dinner_recipe(recipe["name"]):
                    recipes.append(recipe)
                    count += 1
                i += 1

            random.shuffle(recipes)

            days_to_recipes = [(days_of_week[i], recipes[i]) for i in range(num_meals)]  # array of (day, recipe) tuples

            return render(request, "meal_planner/meal_planner.html",
                          context={"state": "show_results", "options_form": options_form,
                                   "days_to_recipes": days_to_recipes})

        return render(request, "meal_planner/meal_planner.html",
                      context={"state": "no_results", "options_form": options_form})
