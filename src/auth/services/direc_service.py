from src.auth.services.service import Service
import googlemaps
import os
import src.settings

class DirecService(Service):

    def __init__(self):
        self.gmaps_client = googlemaps.Client(key=os.environ.get('GOOGLE_DIREC_API_KEY', 'secret'))

    def get_possible_journeys(self, initial_position, final_position):
        #chequear en los endpoints que usen esta funcion los parametros con el CoordinateSchema
        ways = self.gmaps_client.directions(initial_position, final_position, alternatives=True)
        return ways