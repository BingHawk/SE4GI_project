import overpy

# Import to another file with:
# from osm import Osm
# Run query by writing
# Osm.getCities(filter = [])
# Where filter is an optional input. If a list is inputed, only the cities in the list will 
# be outputted

class Osm:
    API = overpy.Overpass()

    citiesQuery = '''
    [out:json];
    (area["ISO3166-1"="IT"];) ->.a;
    node["place" = "city"](area.a);
    (._;>;);
    out;
    '''

    @classmethod
    def getCities(cls, filter = None):
        res = cls.API.query(cls.citiesQuery)

        cities = []
        for node in res.nodes:
            if filter is None or node.tags['name'] in filter:
                c = {
                    'name': node.tags['name'],
                    'coordinates':[float(node.lon), float(node.lat)]
                }
                cities.append(c)

        return cities


if __name__ == "__main__":
    CityCoords = Osm.getCities(filter = ['Roma','Milano'])
    print(CityCoords)