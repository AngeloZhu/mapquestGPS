#Angelo Zhu
#59714552


import urllib.parse
import urllib.request
import json
import mapquest_main

BASE_MAPQUEST_ROUTE_URL = 'http://open.mapquestapi.com/directions/v2/route?'
BASE_MAPQUEST_ELEVATION_URL = 'http://open.mapquestapi.com/elevation/v1/profile?'
MAPQUEST_API_KEY = 'UEz5vfmxyvHWT61tQPrwFTqYJsTVdpY3'


def build_route_url(search_query: dict) -> str:
    '''Builds the route url for mapquest with the given search query.
        Returned as a string'''
    
    query_parameters = [
        ('key', MAPQUEST_API_KEY), ('from', search_query['locations'][0])]
    
    for i in range(0, len(search_query['locations']) - 1):
        query_parameters.append(('to', search_query['locations'][i + 1]))


    return BASE_MAPQUEST_ROUTE_URL + urllib.parse.urlencode(query_parameters)


def build_elevation_url(search_query: list) -> list:
    '''Builds the elevation url for mapquest with the given lat/longs.
    Returned as a string'''
    
    search_query = list(map(str, search_query))
    '''changes the list of ints into a list of strings'''
    lat_longs = ','.join(search_query)
    query_parameters = [
    ('key', MAPQUEST_API_KEY), ('shapeFormat', 'raw'),
    ('latLngCollection', lat_longs)]
    
    return BASE_MAPQUEST_ELEVATION_URL + urllib.parse.urlencode(query_parameters)


def get_result(url: str) -> dict:
    '''Opens the url and obtains it's api'''
    
    response = None

    try:
        response = urllib.request.urlopen(url)
        return json.load(response)
    finally:
        if response != None:
            response.close()
