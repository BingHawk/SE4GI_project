from flask import Flask, request, render_template
from backend import get_locations

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["APPLICATION_ROOT"] = "/"


@app.route('/', methods=["GET"])
def main():
    # Get shops data from OpenStreetMap
    locations = get_locations()

    # Initialize variables
    markers = ''
    for location in locations:
        try:
            # Create the marker each location
            id = 'location'+str(location['id'])

            markers += "var {id} = L.marker([{lat}, {long}]);\
                {id}.addTo(map);".format(id=id, lat=location['coordinates']['latitude'],\
                                                             long=location['coordinates']['longitude'])
        except KeyError:
            continue
    # Render the page with the map
    print(markers)
    return render_template('results.html', markers=markers, lat=45.4, lon=9.18, zoom=8)

    """
            markers += "var {idd} = L.marker([{latitude}, {longitude}]);\
                {idd}.addTo(map).bindPopup('{brand}<br>{website}');".format(idd=idd, latitude=node.lat,\
                                                                             longitude=node.lon,
                                                                             brand=shop_brand,\
                                                                             website=shop_website)
"""