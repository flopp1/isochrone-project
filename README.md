
# Public Transport isochrone generator for Singapore

Generates isochrones contoured for public transport for any point in Singapore by clicking on a map and displaying the resulting GeoJSON from OpenTripPlanner.

Note: 

2.5.0 (2.2.0 - 2.5.0) MUST be used for OpenTripPlanner as it is the latest version with isochrone generation support. It was deprecated and removed in 2.6.0 due to limitations and lack of maintenance resources.





## Run Locally

Clone the project

```bash
  git clone https://github.com/flopp1/isochrones
```

Go to the project directory

```bash
  cd "isochrone project"
```

Download Python dependencies

```bash
  pip install dash dash-leaflet requests
```

Get the OpenTripPlanner binary: otp-2.5.0-shaded.jar from [OpenTripPlanner Releases](https://github.com/opentripplanner/OpenTripPlanner/releases) and place in the repository directory

Download [Singapore OpenStreetMap database](https://geo2day.com/asia/singapore.html) and [Singapore GTFS database](https://github.com/thecrapone/singapore-gtfs-2026). Rename to singapore-osm.pbf and singapore-gtfs.zip respectively, and place in ./data

Build graph.obj [Required for first run, thereafter optional, only if there are changes to the OSM/GTFS data]

```bash
java -Xmx[Memory to allocate in GB]G -jar otp-2.5.0-shaded.jar --build --save ./data
```

Start the OTP server FIRST

```bash
java -Xmx[Memory to allocate in GB]G -jar otp-2.5.0-shaded.jar --load ./data
```

Start the Dash server

```bash
python main.py
```

View the webapp at http://127.0.0.1:8050

