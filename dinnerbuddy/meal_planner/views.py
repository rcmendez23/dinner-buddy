from django.shortcuts import render
from AllRecipes.AllRecipes import AllRecipes
from .forms import OptionsForm


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
                "ingIncl": ingredients_included,  # 'Must be included' ingrdients (optional)
                "ingExcl": ingredients_excluded,  # 'Must not be included' ingredients (optional)
                "sort": "re"  # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
            }
            query_result = AllRecipes.search(query_options)

            days_to_recipes = []  # array of (day, recipe) tuples

            # Get :
            num_meals = len(days_of_week)
            for i in range(num_meals):
                main_recipe_url = query_result[i]['url']
                recipe = AllRecipes.get(
                    main_recipe_url)
                days_to_recipes.append((days_of_week[i], recipe))

            return render(request, "meal_planner/meal_planner.html",
                          context={"state": "show_results", "options_form": options_form,
                                   "days_to_recipes": days_to_recipes})

        return render(request, "meal_planner/meal_planner.html",
                      context={"state": "no_results", "options_form": options_form})
