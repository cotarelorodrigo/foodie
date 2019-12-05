from src.auth.services.service import Service
import googlemaps
import os
import math
import re
import src.settings

class DirecService(Service):

    def __init__(self):
        self.gmaps_client = googlemaps.Client(key=os.environ.get('GOOGLE_DIREC_API_KEY', 'secret'))

    def get_possible_journeys(self, initial_position, final_position):
        '''
            init = {"latitude": -34.863794, "longitude": -58.389695}
            final = {"latitude": -34.863544, "longitude": -58.380655}
        '''
        #chequear en los endpoints que usen esta funcion los parametros con el CoordinateSchema
        ways = self.gmaps_client.directions(initial_position, final_position, alternatives=True)
        return ways

    def get_nearly_deliverys(self, shop, deliverys):
        '''
            shop = {"latitude": -34.863794, "longitude": -58.389695}
            deliverys = [{"latitude": -34.858390, "longitude": -58.381415}, {"latitude": -34.861102, "longitude": -58.384215}, {"latitude": -34.863221, "longitude": -58.390684}]
        '''
        print("shop: {}".format(shop))
        print("deliverys: {}".format(deliverys))
        coordinates_shop = {"latitude": shop["latitude"], "longitude":shop["longitude"]}
        coordinates_delviery = [{"latitude": d["latitude"], "longitude":d["longitude"]} for d in deliverys]
        matrix = self.gmaps_client.distance_matrix(origins=coordinates_shop, destinations=coordinates_delviery)
        distancias = []
        for delivery in matrix['rows'][0]['elements']:
            if delivery['status'] == 'OK':
                print("d: {}".format(delivery))
                dist = float(re.findall("\d+\.\d+", delivery['distance']['text'])[0]) 
                distancias.append(dist)
            else:
                distancias.append(math.inf)
        return sorted(deliverys, key = lambda d: distancias[deliverys.index(d)])

    def get_shops_info(self, _coordinates, _radius):
        shops = self.gmaps_client.places(query='restaurant', location=_coordinates, radius=_radius, language='es')
        shops_list = []
        for shop in shops['results']:
            d = {"name": shop['name'], "address": shop['formatted_address'], "coordinates": {"latitude": shop['geometry']['location']['lat'],
            "longitude": shop['geometry']['location']['lng']}, "rating": shop["rating"], "photoUrl": shop['icon']}
            shops_list.append(d)
        return shops_list