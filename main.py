import dash
from dash import html, Input, Output
import dash_leaflet as dl
import requests

app = dash.Dash(__name__)

COLOR_MAPPING = {
    "900": 'cyan',     # 15 Minutes
    "1800": 'gold',    # 30 Minutes
    "2700": 'tomato',  # 45 Minutes
    "3600": 'red'      # 60 Minutes
}

app.layout = html.Div([
    dl.Map(
        id="map",
        center=[1.3521, 103.8198],
        zoom=12,
        children=[
            # FIXED: Using standard OpenStreetMap tiles to bypass OpaqueResponseBlocking
            dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"),
            
            dl.LayerGroup(id="isochrone-layer"),
            dl.LayerGroup(id="marker-layer")
        ],
        style={'width': '100%', 'height': '100vh'}
    )
])

@app.callback(
    Output("marker-layer", "children"),
    Output("isochrone-layer", "children"),
    Input("map", "clickData")
)
def update_map(click_data):
    if click_data is None:
        return None, None

    lat = click_data['latlng']['lat']
    lng = click_data['latlng']['lng']
    
    marker = dl.Marker(position=[lat, lng], children=dl.Popup(f"Origin: {lat:.4f}, {lng:.4f}"))

    otp_url = "http://localhost:8080/otp/traveltime/isochrone"
    params = {
        'batch': 'true',
        'location': f"{lat},{lng}",
        'modes': 'WALK,TRANSIT',
        'time': '2026-05-25T08:30:00+08:00',
        'arriveBy': 'false',
        'cutoff': ['15M', '30M', '45M', '60M']
    }

    try:
        response = requests.get(otp_url, params=params)
        if response.status_code != 200:
            return marker, None
            
        geojson_data = response.json()
        
        # FIXED: Group features by color and create a separate GeoJSON layer for each color.
        # This completely avoids complex JS serialization issues.
        layers = []
        for feature in geojson_data.get('features', []):
            contour_time = str(feature['properties'].get('time'))
            fill_color = COLOR_MAPPING.get(contour_time, 'gray')
            
            # Create a single standalone feature collection for this specific polygon
            single_feature_collection = {
                "type": "FeatureCollection",
                "features": [feature]
            }
            
            # Apply standard, hardcoded static styling to this layer
            geo_layer = dl.GeoJSON(
                data=single_feature_collection,
                style={
                    "fillColor": fill_color,
                    "color": "black",
                    "weight": 1,
                    "fillOpacity": 0.4
                }
            )
            layers.append(geo_layer)
        
        return marker, layers

    except Exception as e:
        print(f"Error handling maps: {e}")
        return marker, None

if __name__ == '__main__':
    app.run(debug=True, port=8050)