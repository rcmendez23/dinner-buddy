# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request
import json

import re

import random

MAX_PAGE = 10


class AllRecipes(object):

    @staticmethod
    def search(query_dict):
        """
        Search recipes parsing the returned html data.
        """
        base_url = "https://allrecipes.com/search/results/?"
        query_url = urllib.parse.urlencode(query_dict)

        page_shuffle = '&page=' + str(random.randint(1, MAX_PAGE))

        url = base_url + query_url + page_shuffle

        req = urllib.request.Request(url)
        req.add_header('Cookie', 'euConsent=true')

        html_content = urllib.request.urlopen(req).read()

        soup = BeautifulSoup(html_content, 'html.parser')

        search_data = []
        articles = soup.findAll("article", {"class": "fixed-recipe-card"})

        iterarticles = iter(articles)
        try:
            next(iterarticles)
        except StopIteration as e:
            print(e)

        for article in iterarticles:
            data = {}
            try:
                data["name"] = article.find("h3", {"class": "fixed-recipe-card__h3"}).get_text().strip(' \t\n\r')
                data["description"] = article.find("div", {"class": "fixed-recipe-card__description"}).get_text().strip(
                    ' \t\n\r')
                data["url"] = article.find("a", href=re.compile('^https://www.allrecipes.com/recipe/'))['href']
                try:
                    data["image"] = \
                        article.find("a", href=re.compile('^https://www.allrecipes.com/recipe/')).find("img")[
                            "data-original-src"]
                except Exception as e1:
                    print(e1)
            except Exception as e2:
                print(e2)
            if data and "image" in data:  # Do not include if no image, could be an ad
                search_data.append(data)


        return search_data

    @staticmethod
    def get(url):
        """
        'url' from 'search' method.
         ex. "/recipe/106349/beef-and-spinach-curry/"
        """
        # base_url = "https://allrecipes.com/"
        # url = base_url + uri

        req = urllib.request.Request(url)
        req.add_header('Cookie', 'euConsent=true')

        html_content = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html_content, 'html.parser')

        script_tag = soup.find("script", {"type": "application/ld+json"})
        inner_json_string = str(script_tag).replace("<script type=\"application/ld+json\">", "").replace("</script>",
                                                                                                         "")
        json_data = json.loads(inner_json_string)
        recipe_data = json_data[1]

        # required data
        name = recipe_data.get("name", None)
        if not name:
            raise MissingRecipeDataError("Name for recipe was not found.")
        ingredients = recipe_data.get("recipeIngredient", None)
        if not ingredients:
            raise MissingRecipeDataError("Ingredients for recipe were not found.")
        total_time = recipe_data.get("totalTime", None)
        if not total_time:
            raise MissingRecipeDataError("Total time for recipe was not found.")

        # optional data
        image_and_metadata = recipe_data.get("image", None)
        description = recipe_data.get("description", None)
        prep_time = recipe_data.get("prepTime", None)
        cook_time = recipe_data.get("cookTime", None)
        recipe_yield = recipe_data.get("recipeYield", None)
        instructions = recipe_data.get("recipeInstructions", None)
        rating = recipe_data.get("aggregateRating", None).get("ratingValue", None)
        nutrition = recipe_data.get("nutrition", None)

        data = {
            "rating": rating,
            "ingredients": ingredients,
            "instructions": instructions,
            "name": name,
            "prep_time": prep_time,
            "cook_time": cook_time,
            "total_time": total_time,
            "description": description,
            "yield": recipe_yield,
            "nutrition": nutrition,
            "image_and_metadata": image_and_metadata,
            "url": url,
        }

        return data


class MissingRecipeDataError(RuntimeError):
    pass
