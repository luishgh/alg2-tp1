import dash_leaflet as dl
import dash_leaflet.express as dlx
# from dash_extensions.enrich import DashProxy, html
from dash_extensions.enrich import DashProxy, Input, Output, html

from dash_extensions.javascript import assign

bares = [
    #dict('NOME_FANTASIA', latitude, longitude) --- IDEIA! (acho que só add a lista que tá sendo geranda dos dados_geoloc e 
    #transformar em dict funciona)
    
    dict(name = 'PIZZARIA E CHURRASCARIA VARANDA', lat = -20.007130861204672, lon = -44.00976338917243),
    dict(name = 'TATU REI DO ANGU A  BAHIANA', lat = -19.973146360483586, lon =-44.01507213335438)
]

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



# Copy data from the edit control to the geojson component.
@app.callback(Output("geojson_obj", "data"), Input("edit_control", "geojson"))
def mirror(x):
    print("Sou uma forma completa!", x)
    return geojson
    # return x



# Copy data from the edit control to the geojson component.
@app.callback(Output("edit_control", "geojson"), Input("edit_control", "geojson"))
def getlast(x):
    if x is not None and x and x != {}:
        return {
            "type": x['type'],
            "features": x['features'][-1:]
        }
    return x

if __name__ == "__main__":
    app.run()