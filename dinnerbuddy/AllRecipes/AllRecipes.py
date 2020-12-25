# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request
import json

import re


class AllRecipes(object):

    @staticmethod
    def search(query_dict):
        """
        Search recipes parsing the returned html data.
        """
        base_url = "https://allrecipes.com/search/results/?"
        query_url = urllib.parse.urlencode(query_dict)

        url = base_url + query_url

        req = urllib.request.Request(url)
        req.add_header('Cookie', 'euConsent=true')

        html_content = urllib.request.urlopen(req).read()

        soup = BeautifulSoup(html_content, 'html.parser')

        search_data = []
        articles = soup.findAll("article", {"class": "fixed-recipe-card"})

        iterarticles = iter(articles)
        next(iterarticles)
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
                    pass
                try:
                    data["rating"] = float(
                        article.find("div", {"class": "fixed-recipe-card__ratings"}).find("span")["data-ratingstars"])
                except ValueError:
                    data["rating"] = None
            except Exception as e2:
                pass
            if data and "image" in data:  # Do not include if no image -> its probably an add or something you do not want in your result
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
        inner_json_string = str(script_tag).replace("<script type=\"application/ld+json\">", "").replace("</script>", "")
        json_data = json.loads(inner_json_string)
        recipe_data = json_data[1]
        name = recipe_data["name"]
        image_and_metadata = recipe_data["image"]
        description = recipe_data["description"]
        prep_time = recipe_data["prepTime"]
        cook_time = recipe_data["cookTime"]
        total_time = recipe_data["totalTime"]
        recipe_yield = recipe_data["recipeYield"]
        ingredients = recipe_data["recipeIngredient"]
        instructions = recipe_data["recipeInstructions"]
        rating = recipe_data["aggregateRating"]["ratingValue"]
        nutrition = recipe_data["nutrition"]

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
            "image_and_metadata": image_and_metadata
        }

        return data
