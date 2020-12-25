from django.shortcuts import render
from AllRecipes.AllRecipes import AllRecipes


def meal_planner(request):
    if request.method == "GET":
        return render(request, "meal_planner/meal_planner.html", context={"state": "no_results"})
    if request.method == "POST":
        # Search :
        query_options = {
            "wt": "pork curry",  # Query keywords
            "ingIncl": "olives",  # 'Must be included' ingrdients (optional)
            "ingExcl": "onions salad",  # 'Must not be included' ingredients (optional)
            "sort": "re"  # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
        }
        query_result = AllRecipes.search(query_options)

        # print(query_result)

        # Get :
        main_recipe_url = query_result[0]['url']
        detailed_recipe = AllRecipes.get(
            main_recipe_url)  # Get the details of the first returned recipe (most relevant in our case)

        # Display result :
        print("## %s :" % detailed_recipe['name'])  # Name of the recipe

        for ingredient in detailed_recipe['ingredients']:  # List of ingredients
            print("- %s" % ingredient)

        for step in detailed_recipe['instructions']:  # List of cooking steps
            print("# %s" % step)
        return render(request, "meal_planner/meal_planner.html", context={"state": "show_results", "detailed_recipe": detailed_recipe})
