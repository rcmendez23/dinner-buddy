from django.shortcuts import render
from AllRecipes.AllRecipes import AllRecipes
from .forms import OptionsForm
import random

NON_DINNER_KEYWORDS = ['choco', 'cookie', 'muffin', 'brownie', 'cake', 'meringue', 'biscuit', 'scone', 'tiramisu',
                       'caramel', 'popcorn', 'fill', 'guac', 'gravy', 'sauce', 'salsa', 'pesto', 'pudding', 'seasoning',
                       'edamame', 'fruit', 'banana', 'bread', 'bar', 'margarita', 'sangria', 'coffee', 'cider',
                       'smoothie',
                       'ice cream', 'crisps', 'apple pie']


def is_dinner_recipe(recipe_name):
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

            random.shuffle(query_result)

            recipes = []

            # Get recipe data
            num_meals = len(days_of_week)
            for result in query_result:
                if len(recipes) >= num_meals:
                    break
                url = result['url']
                recipe = AllRecipes.get(url)
                if is_dinner_recipe(recipe["name"]):
                    recipes.append(recipe)

            message = None
            if len(recipes) < num_meals:
                print("Number of recipes found (" + str(len(
                    recipes)) + ") was less than the number requested (" + str(num_meals) + ")")
                message = "Oh no! We couldn't find enough recipes for your search."

            # array of (day, recipe) tuples
            days_to_recipes = [(days_of_week[i], recipes[i]) for i in range(min(num_meals, len(recipes)))]

            return render(request, "meal_planner/meal_planner.html",
                          context={"state": "show_results", "options_form": options_form,
                                   "days_to_recipes": days_to_recipes, "error": message})

        return render(request, "meal_planner/meal_planner.html",
                      context={"state": "no_results", "options_form": options_form,
                               "error": options_form.errors.get("__all__")})
