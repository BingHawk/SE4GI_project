for city in getCityCoords().keys():
            coords = getCityCoords()
            locations[city] = {'cityName': city, 'coordinates': coords[city], 'particles': result['measurements']}
