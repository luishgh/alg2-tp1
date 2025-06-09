import pandas as pd
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.enrich import DashProxy, Input, Output, State, html
from dash_extensions.javascript import assign
from dash import dash_table
from pprint import pprint 
import os

port = int(os.environ.get("PORT", 10000))

from lib.kdtree import KDTree


def get_axis(point, axis):
    if axis == 1:  # Latitude
        return point['lat']
    elif axis == 0:  # Longitude
        return point['lon']
    
def process_bares(bares):
    return [
        {
            **bar,
            "tooltip": bar["name"],
            "popup": make_popup(bar)
        } for bar in bares
    ]


def make_popup(bar):
    if bar['comida_de_buteco']: 
        # comida de boteco
        popup_html = f"""
        <div style="font-family: Arial; font-size: 10px; max-width: 280px;">
            <h4 style="margin-bottom: 5px; color: red;">{bar['name']}</h4>
            <div style="display: flex; gap: 10px; flex-wrap: nowrap; min-width: 260px;">
                <!-- Left column -->
                <div style="flex: 1; min-width: 130px;">
                    <p style="margin: 2px 0;"><strong>Comida di Buteco:</strong> Sim</p>
                    <p style="margin: 2px 0;"><strong>Endereço:</strong> {bar['address']}</p>
                </div>

                <!-- Right column -->
                <div style="flex: 1; min-width: 130px;">
                    <p style="margin: 2px 0;"><strong>Latitude:</strong> {bar['lat']:.5f}</p> 
                    <p style="margin: 2px 0;"><strong>Longitude:</strong> {bar['lon']:.5f}</p>
                </div>
            </div>

            <hr style="border: 0; height: 2px; background-color: #89CC50; width: 80%; margin: 5px auto;">
            <p style="margin: 2px 0; text-align: center;"><strong>{bar['nome_prato']}</strong></p>
            <p style="margin: 5px 0;"><strong>Descrição:</strong> {bar['prato_descricao']}</p>

            {f'''
            <div style="text-align: center; margin-top: 2px;">
                <img src="{bar["image"]}" style="max-width: 90px; border-radius: 5px; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
            </div>
            ''' if bar["image"] else ''}
        </div>
        """

    else: 
        # ESTABELECIMENTO COMUM
        popup_html = f"""
        <div style="font-family: Arial; font-size: 10px; max-width: 250px;">
            <h4 style="margin-bottom: 5px; color: #2E86C1;">{bar['name']}</h4>
            <p style="margin: 2px 0;"><strong>Está no Comida di Buteco:</strong> Não</p>
            <p style="margin: 2px 0;"><strong>Endereço:</strong> {bar['address']}</p>
            <p style="margin: 2px 0;"><strong>Latitude:</strong> {bar['lat']:.5f}</p> 
            <p style="margin: 2px 0;"><strong>Longitude:</strong> {bar['lon']:.5f}</p>
        </div>
        """
    return popup_html

df_data = pd.read_csv("./data/dados_tratados_geolocalizados.csv")
df_data['COLOR'] =  df_data['HAS_CDB'].map(lambda x: 'red' if x else 'blue')
df_data['ENDERECO_FORMATADO'] = df_data['ENDERECO_FORMATADO'].map(lambda x: x + ', BH - MG')
# df_plot = pd.concat([
#     df_data[(df_data['HAS_CDB']) & (df_data['HAS_GEOLOC'])],
#     df_data[(df_data['HAS_GEOLOC'])].head(6000),
# ]).drop_duplicates()
bares = df_data[df_data['HAS_GEOLOC']][[
    'NOME_FANTASIA', 'LATITUDE', 'LONGITUDE', 'COLOR',  'ENDERECO_FORMATADO',
    'HAS_CDB','NOME_PRATO', 'PRATO_DESCRICAO', 'PRATO_IMAGEM'
]].rename(columns={
    'NOME_FANTASIA': 'name',
    'LATITUDE': 'lat',
    'LONGITUDE': 'lon',
    'COLOR': 'color',
    'ENDERECO_FORMATADO': 'address',
    'HAS_CDB': 'comida_de_buteco',
    'NOME_PRATO': 'nome_prato',
    'PRATO_DESCRICAO': 'prato_descricao',
    'PRATO_IMAGEM':'image',
}).to_dict(orient='records')

# KDTree e GeoJSON
tree = KDTree(bares, get_axis)

dados_bares_inicial = process_bares(bares)
geojson = dlx.dicts_to_geojson(dados_bares_inicial)

bounds_rmbh = [[-20.1, -44.2], [-19.7, -43.7]] 

point_to_layer = assign("""
function(feature, latlng) {
    let color = feature.properties.color || "blue";
    let iconUrl = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-" + color + ".png";
    let icon = L.icon({
        iconUrl: iconUrl,
        shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });
    return L.marker(latlng, {icon: icon});
}
""")

on_each_feature = assign("""
function(feature, layer) {
    if (feature.properties && feature.properties.popup) {
        layer.bindPopup(feature.properties.popup);
    }
}
""")

app = DashProxy(
    prevent_initial_callbacks=True,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
        "https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.min.js"
    ]
)

app.layout = html.Div(
    [
        html.Header(
            [
                html.H1("Bares e Restaurantes em Belo Horizonte", className="header-title"),
                html.P("Explore os estabelecimentos gastronômicos da cidade selecionando áreas no mapa.", className="header-subtitle")
            ],
            style={
                "backgroundColor": "#89CC50",
                "padding": "15px 8px",
                "textAlign": "center",
                "color": "white",
                "boxShadow": "0px 2px 6px rgba(0,0,0,0.2)"
            }
        ),
        dl.Map(
            children=[
                dl.TileLayer(),
                dl.GeoJSON(
                    data=geojson,
                    id="geojson_obj",
                    options=dict(pointToLayer=point_to_layer),
                    hideout={},
                    hoverStyle={"weight": 3, "color": "gray", "dashArray": "5, 5"},
                    onEachFeature=on_each_feature,
                ),
                dl.FeatureGroup(id="drawn-features", children=[dl.EditControl(
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
            style={
                "height": "70vh",
                "margin": "5px auto 0",
                "width": "100%",
                "borderRadius": "5px",
                "boxShadow": "0 4px 12px rgba(0,0,0,0.1)"
            },
            center=[-19.92, -43.94],
            zoom=10,
            maxBounds=bounds_rmbh,
            minZoom=9,
            maxZoom=17,
            scrollWheelZoom=True
        ),
        html.Div([
            html.Pre(id="selected-bounds", style={
                "whiteSpace": "pre-wrap",
                "padding": "10px",
                "backgroundColor": "#eee",
                "borderRadius": "5px",
                "margin": "10px auto",
                "maxWidth": "60%",
                "fontFamily": "'Lato', sans-serif",
                "fontSize": "14px"
            }),
            html.Div(id="selected-table", style={"maxWidth": "80%", "margin": "0 auto"}),
        ])
    ],
    style={
        "fontFamily": "'Lato', sans-serif",
        "backgroundColor": "#f4f4f4",
        "margin": 0,
        "padding": 0
    }
)


@app.callback(
    Output("geojson_obj", "data"),
    Output("selected-bounds", "children"),
    Output("selected-table", "children"),
    Input("edit_control", "geojson"),
)
def update_selected(rectangle_geojson):
    if rectangle_geojson and "features" in rectangle_geojson and rectangle_geojson["features"]:
        rectangle = rectangle_geojson["features"][-1]  # Último retângulo desenhado
        if rectangle["geometry"]["type"] == "Polygon":
            coords = rectangle["geometry"]["coordinates"][0]

            lx = min(coord[0] for coord in coords)
            ly = min(coord[1] for coord in coords)
            rx = max(coord[0] for coord in coords)
            ry = max(coord[1] for coord in coords)
            print(f"Rectangle bounds: {lx}, {rx}, {ly}, {ry}")
            bounds_text = f"Bounds selecionados:\nLongitude: {lx:.5f} a {rx:.5f}\nLatitude: {ly:.5f} a {ry:.5f}"
            filtered_points = process_bares(tree.query([(lx, rx), (ly, ry)]))

            if filtered_points:
                columns = [{"name": c, "id": c} for c in ["name", "address", "comida_de_buteco", "lat", "lon", "nome_prato"]]
                table = dash_table.DataTable(
                    data=filtered_points,
                    columns=columns,
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left", "fontSize": 12, "padding": "4px"},
                    style_header={"backgroundColor": "#89CC50", "color": "white", "fontWeight": "bold"},
                    page_size=10,
                )
            else:
                table = "Nenhum ponto selecionado."

            new_rectangle_geoj = rectangle_geojson.copy()
            new_rectangle_geoj['features'] = new_rectangle_geoj['features'][-1:]

            return dlx.dicts_to_geojson(filtered_points), bounds_text, table

    return dlx.dicts_to_geojson(dados_bares_inicial), "Nenhuma área selecionada.", ""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)