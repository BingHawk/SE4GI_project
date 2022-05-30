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
    (node["place"="city"](area.a);
     node["place"="town"](area.a););
    (._;>;);
    out;
    '''

    @staticmethod
    def __unionTags(cities):
        outString = '('
        for city in cities:
            outString += '''node["place"]["name"="{}"](area.a);'''.format(city)
        outString += ')'
        return outString

    @classmethod
    def getCities(cls, filter = None): 
        query = '''
                [out:json];
                (area["ISO3166-1"="IT"];) ->.a;
                (
                    node["place"="city"](area.a);
                    node["place"="town"](area.a);
                );
                (._;>;);
                out;
                '''

        print(query)
        res = cls.API.query(query)

        cities = []
        for node in res.nodes:
            if filter is None or node.tags['name'].title() in filter:
                c = {
                    'name': node.tags['name'].title(),
                    'coordinates':[float(node.lon), float(node.lat)]
                }
                cities.append(c)
        return cities


if __name__ == "__main__":

    # filter = ['Alessandria', 'Alfonsine', 'Ancona', 'Arezzo', 'Ascoli Piceno', 'Asti','Roma']
    filter = ['Alessandria', 'Alfonsine', 'Ancona', 'Arezzo', 'Ascoli Piceno', 'Asti', 'Avellino', 'Bari', 'Barletta-Andria-Trani', 'Belluno', 'Benevento', 'Bergamo', 'Biella', 'Bologna', 'Bolzano/Bozen', 'Brescia', 'Brindisi', 'Cagliari', 'Campobasso', 'Carbonia-Iglesias', 'Carpi', 'Caserta', 'Catanzaro', 'Cento', 'Cesena', 'Chiesanuova', 'Civitavecchia', 'Colorno', 'Como', 'Cosenza', 'Cremona', 'Crotone', 'Cuneo', 'Faenza', 'Ferrara', 'Fiorano Modenese', 'Firenze', 'Foggia', "Forli'", "Forli'-Cesena", 'Frosinone', 'Genova', 'Grosseto', 'Guastalla', 'Imola', 'Imperia', 'Jolanda Di Savoia', 'Langhirano', "L'Aquila", 'La Spezia', 'Latina', 'Lecce', 'Lecco', 'Livorno', 'Lodi', 'Lucca', "Lugagnano Val D'Arda", 'Macerata', 'Mantova', 'Massa-Carrara', 'Matera', 'Mezzani', 'Milano', 'Mirandola', 'Modena', 'Molinella', 'Monza E Della Brianza', 'Napoli', 'Novara', 'Nuoro', 'Olbia-Tempio', 'Oristano', 'Ostellato', 'Padova', 'Parma', 'Pavia', 'Perugia', 'Pesaro E Urbino', 'Pescara', 'Piacenza', 'Pisa', 'Pistoia', 'Porretta Terme', 'Potenza', 'Prato', 'Ravenna', 'Reggio Di Calabria', "Reggio Nell'Emilia", 'Rieti', 'Rimini', 'Roma', 'Rovigo', 'Salerno', 'San Clemente', 'San Lazzaro Di Savena', 'San Leo', 'Sassari', 'Sassuolo', 'Savignano Sul Rubicone', 'Savona', 'Siena', 'Sogliano Al Rubicone', 'Sondrio', 'Sorbolo', 'Taranto', 'Teramo', 'Terni', 'Torino', 'Trento', 'Treviso', 'Varese', 'Venezia', 'Verbano-Cusio-Ossola', 'Vercelli', 'Verona', 'Verucchio', 'Vibo Valentia', 'Vicenza', 'Villa Minozzo', 'Viterbo']

    cityCoords = Osm.getCities(filter = filter)
        
    gottenCities = [city['name'] for city in cityCoords]
    print(gottenCities)
    print(len(gottenCities))
    print(len(list(dict.fromkeys(gottenCities))))

    missing = 0
    for city in filter:
        if city not in gottenCities:
            print("missing city:",city)
            missing = missing + 1
        else:
            gottenCities.remove(city)
    if missing == 0:
        print("All cities exist")
    else: 
        print("Missing {} cities".format(missing))

    print(gottenCities)
