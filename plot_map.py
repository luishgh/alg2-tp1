import dash_leaflet as dl
import dash_leaflet.express as dlx
# from dash_extensions.enrich import DashProxy, html
from dash_extensions.enrich import DashProxy, Input, Output, html

from dash_extensions.javascript import assign

from lib.kdtree import KDTree

# Define function to get axis values from geographic coordinates
def get_axis(point, axis):
    if axis == 1:  # Latitude
        return point['lat']
    elif axis == 0:  # Longitude
        return point['lon']

bares = [
    #dict('NOME_FANTASIA', latitude, longitude) --- IDEIA! (acho que só add a lista que tá sendo geranda dos dados_geoloc e 
    #transformar em dict funciona)
    
    dict(name = 'PIZZARIA E CHURRASCARIA VARANDA', lat = -20.007130861204672, lon = -44.00976338917243),
    dict(name = 'TATU REI DO ANGU A  BAHIANA', lat = -19.973146360483586, lon =-44.01507213335438)
]

tree = KDTree(bares, get_axis)

# Generate geojson with a marker for each city and name as tooltip.
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c["name"])} for c in bares])

bounds_rmbh = [[-20.1, -44.2], [-19.7, -43.7]]  #pode ajustar se necessario [SW e oposto]

app = DashProxy(prevent_initial_callbacks=True)
app.layout = html.Div(
    [
        dl.Map(
            children=[
                dl.TileLayer(),
                dl.GeoJSON(data=geojson, id="geojson_obj"),
                dl.FeatureGroup([dl.EditControl(
                    id="edit_control",
                    draw={
                        "polygon": False,
                        "polyline": False,
                        "rectangle": True,
                        "circle": False,
                        "marker": False,
                        "circlemarker": False
                    },

                )]),
            ],
            style={"height": "50vh"},
            center=[-19.92, -43.94],  # Centro aproximado de BH
            zoom=10,
            maxBounds=bounds_rmbh,
            minZoom=9,
            maxZoom=17,
            scrollWheelZoom=True
        ),
    ]
)



# # Copy data from the edit control to the geojson component.
# @app.callback(Output("geojson_obj", "data"), Input("edit_control", "geojson"))
# def mirror(x):
#     print("Sou uma forma completa!", x)
#     return geojson
#     # return x



# # Copy data from the edit control to the geojson component.
# @app.callback(Output("edit_control", "geojson"), Input("edit_control", "geojson"))
# def getlast(x):
#     if x is not None and x and x != {}:
#         return {
#             "type": x['type'],
#             "features": x['features'][-1:]
#         }
#     return x

# Callback to filter points based on the rectangle drawn
@app.callback(Output("geojson_obj", "data"), Input("edit_control", "geojson"))
def filter_points_by_rectangle(rectangle_geojson):
    if rectangle_geojson and "features" in rectangle_geojson and rectangle_geojson["features"]:
        # Get the bounds of the rectangle
        rectangle = rectangle_geojson["features"][-1]  # Last drawn rectangle
        if rectangle["geometry"]["type"] == "Polygon":
            coords = rectangle["geometry"]["coordinates"][0]  # Rectangle coordinates

            lx = min(coord[0] for coord in coords)
            ly = min(coord[1] for coord in coords)
            rx = max(coord[0] for coord in coords)
            ry = max(coord[1] for coord in coords)
            print(f"Rectangle bounds: {lx}, {rx}, {ly}, {ry}")

            # Query KDTree for points within the rectangle bounds
            filtered_points = tree.query([(lx, rx), (ly, ry)])

            # Generate new GeoJSON for filtered points
            return dlx.dicts_to_geojson([{**c, **dict(tooltip=c["name"])} for c in filtered_points])

    # If no rectangle or invalid data, return all points
    return dlx.dicts_to_geojson([{**c, **dict(tooltip=c["name"])} for c in bares])


if __name__ == "__main__":
    app.run()