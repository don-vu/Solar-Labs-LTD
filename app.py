import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# 1. PAGE SETUP
st.set_page_config(page_title="Solar Intelligence", layout="wide")

st.markdown("""
    <style>
        /* 1. Push the map to the absolute edges */
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        
        /* 2. Hide the Streamlit menus */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* 3. Lock the main page so it physically cannot scroll */
        .stApp {
            overflow: hidden !important;
        }
        
        /* 4. Force the map to be exactly 100% of the screen's height and width */
        iframe {
            height: 100vh !important;
            width: 100vw !important;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data 
def load_data():
    # Update this path to where your actual geojson is
    gdf = gpd.read_file("/Users/boi/Desktop/2026projects/HackEDD/images/6.geojson")
    gdf = gdf.to_crs(epsg=4326)
    
    # Calculate solar potential and savings
    gdf['solar_potential_kwh'] = gdf['area'] * 0.7 * 1100 * 0.2
    gdf['money_saved'] = gdf['solar_potential_kwh'] * 0.15
    return gdf

with st.spinner("Analyzing rooftop AI data..."):
    gdf = load_data()

# Calculate totals for the floating legend
total_buildings = len(gdf)
total_kwh = gdf['solar_potential_kwh'].sum()
total_savings = gdf['money_saved'].sum()

# 2. CREATE THE MAP
center = gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[center.y, center.x],
    zoom_start=18,
    tiles="http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}",
    attr="Google Satellite",
    max_zoom=20
)

# Add the orange buildings with tooltips
for _, row in gdf.iterrows():
    tooltip_html = f"""
    <div style='font-family: sans-serif; padding: 10px; min-width: 150px;'>
        <h4 style='margin-top: 0; color: #FF9F00;'>Building #{row.building_id}</h4>
        <b>Roof Area:</b> {row.area:,.0f} m²<br>
        <b>Energy Potential:</b> {row.solar_potential_kwh:,.0f} kWh/yr<br>
        <b>Est. Savings:</b> <span style='color: green;'>${row.money_saved:,.0f}/yr</span>
    </div>
    """
    folium.GeoJson(
        row.geometry,
        tooltip=folium.Tooltip(tooltip_html),
        style_function=lambda x: {
            "fillColor": "#FFB300", 
            "color": "#FF8F00",
            "weight": 2,
            "fillOpacity": 0.5,
        },
    ).add_to(m)

# --- NEW: THE UPGRADED FLOATING LEGEND ---
# I made the box slightly taller to fit your Title and made the background slightly transparent!
legend_html = f'''
     <div style="
     position: absolute; 
     bottom: 50px; left: 50px; width: 340px; height: 260px; 
     background-color: rgba(255, 255, 255, 0.9); border:2px solid grey; z-index:9999; font-size:16px;
     border-radius: 10px; padding: 15px; box-shadow: 3px 3px 10px rgba(0,0,0,0.3); font-family: sans-serif;
     ">
     <h3 style="margin-top:0px; border-bottom:1px solid #ddd; padding-bottom:10px; color:#333;">☀️ AI Solar Intelligence</h3>
     <p style="margin: 5px 0;"><b>Buildings Analyzed:</b> <br><span style="font-size:22px; color:#333;">{total_buildings}</span></p>
     <p style="margin: 5px 0;"><b>Total Solar Potential:</b> <br><span style="font-size:22px; color:#FF9F00;">{total_kwh:,.0f} kWh/yr</span></p>
     <p style="margin: 5px 0;"><b>Estimated Savings:</b> <br><span style="font-size:22px; color:green;">${total_savings:,.0f}/yr</span></p>
     </div>
     '''

m.get_root().html.add_child(folium.Element(legend_html))

# 3. DISPLAY FULL WIDTH & HEIGHT
# Height increased to 900 to push the bottom of the map down to your screen's edge.
st_folium(m, width="100%", height=900)