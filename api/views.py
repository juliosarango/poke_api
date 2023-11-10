from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from django.conf import settings


class PokemonAPIView(APIView):
    def get(self, request):
        response = requests.get(settings.POKE_API_URL).json()
        result_pokemon = []

        for pokemon in response["results"]:
            response_pokemon = requests.get(pokemon["url"]).json()
            data_pokemon = {
                "name": response_pokemon["name"],
                "sprite": response_pokemon["sprites"]["front_default"],
                "num_abilities": len(response_pokemon["abilities"]),
                "url": pokemon["url"],
            }
            result_pokemon.append(data_pokemon)

        pokemos_result_data = {
            "count": response["count"],
            "next": response["next"],
            "previous": response["previous"],
            "results": result_pokemon,
        }
        return Response(pokemos_result_data)
