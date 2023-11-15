from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.conf import settings


class PokemonAPIView(APIView):
    def get(self, request):
        limit_query = request.query_params.get("limit")
        offset_query = request.query_params.get("offset")
        search_query = request.query_params.get("search")

        limit = limit_query if limit_query else settings.POKE_API_DEFAULT_LIMIT
        offset = offset_query if offset_query else settings.POKE_API_DEFAULT_OFFEST
        search = search_query if search_query else ""

        response = None
        type_request = 0
        if search != "":
            url_search = f"{settings.POKE_API_URL}/{search}"
            response = requests.get(url_search).json()
        else:
            type_request = 1
            query_params = {
                "limit": limit,
                "offset": offset,
            }
            response = requests.get(settings.POKE_API_URL, params=query_params).json()

        pokemon_result_data = self.return_data_pokemon(response, type_request)
        return Response(pokemon_result_data)

    def return_data_pokemon(self, response, type_request):
        """_summary_

        Args:
            response Response: Response with data after call pokeapi
            type_request int: 0: search, 1: list all

        Returns:
            dict: Return a dict with all data
        """
        result_pokemon = []
        data_pokemon = {}
        count = 1
        next = ""
        previous = ""
        if type_request == 0:
            data_pokemon = {
                "name": response["species"]["name"],
                "sprite": response["sprites"]["front_default"],
                "num_abilities": len(response["abilities"]),
                "main_abilitie": response["abilities"][0]["ability"]["name"],
                "url": response["species"]["url"],
                "height": response["height"],
                "weight": response["weight"],
            }
            result_pokemon.append(data_pokemon)
        else:
            for pokemon in response["results"]:
                response_pokemon = requests.get(pokemon["url"]).json()
                data_pokemon = {
                    "name": response_pokemon["name"],
                    "sprite": response_pokemon["sprites"]["front_default"],
                    "num_abilities": len(response_pokemon["abilities"]),
                    "main_abilitie": response_pokemon["abilities"][0]["ability"][
                        "name"
                    ],
                    "url": pokemon["url"],
                    "height": response_pokemon["height"],
                    "weight": response_pokemon["weight"],
                }
                result_pokemon.append(data_pokemon)
                count = response["count"]
                next = response["next"] if response["next"] else ""
                previous = response["previous"] if response["previous"] else ""

        pokemon_result_data = {
            "count": count,
            "next": next,
            "previous": previous,
            "results": result_pokemon,
        }

        return pokemon_result_data
