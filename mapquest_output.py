#Angelo Zhu
#59714552

import mapquest_main
import mapquest_code
import urllib
import inspect

class LatLong:
    def getInfo(self, api: dict) -> list:
        '''Returns a list of the latitudes and longitudes
            of each location. Formatted the way it should be printed.
            '''
        new_latlong_list = ['LATLONGS']
        latlong_list = self.get_lat_lng(api)
        for num in range(0, len(latlong_list), 2):
            new_latlong_list.append(self._format_lat(latlong_list[num]) +
                                    ' ' + self._format_long(latlong_list[num + 1]))

        return new_latlong_list

    def get_lat_lng(self, api: dict) -> list:
        '''Returns the latitudes and longitudes of the locations found within the api'''
        latlong_list = []
        for element in api['route']['locations']:
            lat = element['displayLatLng']['lat']
            long = element['displayLatLng']['lng']

            latlong_list.append(lat)
            latlong_list.append(long)

        return latlong_list
        
    def _format_lat(self, lat: float) -> str:
        '''Rounds latitude to two decimal places and gives it direction'''
        if lat > 0:
            return str('{0:.2f}'.format(lat) + 'N')
        elif lat < 0:
            return str('{0:.2f}'.format(abs(lat)) + 'S')

    def _format_long(self, long: float) -> str:
        '''Rounds longitude to two decimal places and gives it direction'''
        if long > 0:
            return str('{0:.2f}'.format(long) + 'E')
        elif long < 0:
            return str('{0:.2f}'.format(abs(long)) + 'W')

class Steps:
    def getInfo(self, api: dict) -> list:
        '''Returns a list of all the directions found within the api'''
        step_list = ['DIRECTIONS']
        dict_one = api['route']['legs']
        
        for element in dict_one:
            dict_two = element['maneuvers']
        
        for item in dict_two:
            step_list.append(item['narrative'])

        return step_list

class TotalTime:
    def getInfo(self, api: dict) -> list:
        '''Returns a list of the time of the trip. Formatted to only minutes'''
        split_time = api['route']['formattedTime'].split(':')

        hour = split_time[0]
        minute = split_time[1]
        second = split_time[2]

        time = self._convert_str_to_int(minute) + self.round_seconds(second) + self.convert_hours(hour)
        
        return ['TOTAL TIME: ' + str(time) + ' minutes']


    def _convert_str_to_int(self, string: str) -> int:
        '''Converts the string number into an integer number'''
        if string[0] == '0':
            return int(string[1])
        return int(string)

    def round_seconds(self, second: str) -> int:
        '''Rounds seconds to one minute or zero minutes'''
        second = self._convert_str_to_int(second)
        if second >= 30:
            return 1
        return 0

    def convert_hours(self, hours: str) -> int:
        '''Converts hours to minutes'''
        hours = self._convert_str_to_int(hours)
        return hours * 60

class TotalDistance:
    def getInfo(self, api: dict) -> list:
        '''Returns the total distance of the journey in correct format. Found in the route api.'''
        return ['TOTAL DISTANCE: ' + str(round(self.getDistance(api))) + ' miles']

    def getDistance(self, api: dict) -> list:
        '''Retunrs the total distance of the journey'''
        return api['route']['distance']

class Elevation:
    def getInfo(self, api: dict) -> list:
        '''Retunrs the elevation of each location if they are within 250 miles of each other'''
        elevation_list = ['ELEVATION']
        for element in api['elevationProfile']:
            elevation_list.append(round(element['height'] * 3.28084))            

        return elevation_list

def run_outputs(outputs: ['Outputs'], route_api: dict, elevation_api: dict) -> None:
    '''Receives information from the api depending on input. Prints the collected information
        from api'''
    output_list = []
    for element in outputs:
        if str(type(element)) == '<class \'mapquest_output.Elevation\'>':
            output_list.append(element.getInfo(elevation_api))
        else:
            output_list.append(element.getInfo(route_api))
        
    for element in output_list:
        print()
        for line in element:
            print(line)


if __name__ == '__main__':
    try:
        inputs = mapquest_main.get_input()

        mapquest_route_api = mapquest_code.get_result(mapquest_code.build_route_url(inputs))
        mapquest_elevation_api = mapquest_code.get_result(mapquest_code.build_elevation_url(LatLong().get_lat_lng(mapquest_route_api)))
     
        run_outputs(inputs['outputs'], mapquest_route_api, mapquest_elevation_api)
        print('\nDirections Courtesy of MapQuest; Map Data Copyright OpenStreetMap Contributors')
    except (KeyError):
        '''Mapquest cannot develop an api for the inputted location'''
        print('NO ROUTE FOUND')
    except (urllib.error.URLError, urllib.error.HTTPError):
        '''Incorrect key/url or no internet connection'''
        print('MAPQUEST ERROR')
