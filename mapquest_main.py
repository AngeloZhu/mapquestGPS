#Angelo Zhu
#59714552

import urllib.parse
import mapquest_code
import mapquest_output


def get_input() -> dict:
    '''Receives input and returns a dictionary containing a list of locations
        and a list of wanted outputs'''
    d = {'LATLONG' : mapquest_output.LatLong(),
        'STEPS' : mapquest_output.Steps(),
        'TOTALTIME' : mapquest_output.TotalTime(),
        'TOTALDISTANCE' : mapquest_output.TotalDistance(),
        'ELEVATION' : mapquest_output.Elevation()}
    
##    number = int(input())
##    location = []
##    
##    for i in range(0, number):
##        location.append(input())
##        
##    next_num = int(input())
##    outputs = []
##    
##    for i in range(0, next_num):
##        outputs.append(d[input()])
##
##    d = dict()
##    d['locations'] = location
##    d['outputs'] = outputs
##        
##    return d '''
    start = input('Enter starting address: ')
    end = input('Enter destination address: ')

    return {'locations': [start, end], 'outputs': [d['LATLONG'], d['STEPS'],
                            d['TOTALTIME'], d['TOTALDISTANCE'], d['ELEVATION']]}
                

