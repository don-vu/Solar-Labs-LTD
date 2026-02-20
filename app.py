import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

st.title("Building Segmentation Viewer")

gdf = gpd.read_file("/Users/donvu/Downloads/buildings.geojson")

# Convert to WGS84 for web maps
gdf = gdf.to_crs(epsg=4326)

center = gdf.geometry.centroid.iloc[0]

m = folium.Map(
    location=[center.y, center.x],
    zoom_start=18
)

for _, row in gdf.iterrows():
    folium.GeoJson(
        row.geometry,
        tooltip=f"""
        Building ID: {row.building_id}
        Area: {row.area:.2f}
        """,
        style_function=lambda x: {
            "fillColor": "red",
            "color": "red",
            "weight": 1,
            "fillOpacity": 0.6,
        },
    ).add_to(m)

st_folium(m, width=1200, height=800)