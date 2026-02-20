import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import box  # NEW: Tool to draw our invisible screen boundary

# 1. PAGE SETUP
st.set_page_config(page_title="Solar Intelligence", layout="wide")

st.markdown("""
    <style>
        .block-container { padding: 0rem !important; max-width: 100% !important; }
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp { overflow: hidden !important; }
        iframe { height: 100vh !important; width: 100vw !important; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data 
def load_data():
    gdf = gpd.read_file("/Users/boi/Desktop/2026projects/HackEDD/images/6.geojson")
    gdf = gdf.to_crs(epsg=4326)
    
    # 1. Base Energy & Money
    gdf['solar_potential_kwh'] = gdf['area'] * 0.7 * 1100 * 0.2
    gdf['money_saved'] = gdf['solar_potential_kwh'] * 0.15
    
    # 2. NEW: Impact Metrics
    # 0.5 kg of CO2 per kWh, divided by 1000 to get Metric Tonnes
    gdf['co2_saved_tonnes'] = (gdf['solar_potential_kwh'] * 0.5) / 1000 
    gdf['homes_powered'] = gdf['solar_potential_kwh'] / 7200
    gdf['evs_charged'] = gdf['solar_potential_kwh'] / 3000
    
    return gdf

with st.spinner("Analyzing rooftop AI data..."):
    gdf = load_data()

# 2. CREATE THE BASE MAP
center = gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[center.y, center.x],
    zoom_start=18,
    tiles="http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}",
    attr="Google Satellite",
    max_zoom=20
)

# Add all the orange buildings
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

# 3. DISPLAY MAP & LISTEN FOR MOVEMENT
# We added key="solar_map" so it remembers where you zoomed, and returned_objects=["bounds"] to track the screen edges
map_data = st_folium(m, width="100%", height=900, key="solar_map", returned_objects=["bounds"])

# 4. THE DYNAMIC MATH (Filter based on what is visible)
visible_gdf = gdf # Default to all buildings

if map_data and map_data.get("bounds"):
    # Grab the corners of your current screen
    bounds = map_data["bounds"]
    sw_lon, sw_lat = bounds["_southWest"]["lng"], bounds["_southWest"]["lat"]
    ne_lon, ne_lat = bounds["_northEast"]["lng"], bounds["_northEast"]["lat"]
    
    # Draw an invisible box using those corners
    screen_box = box(sw_lon, sw_lat, ne_lon, ne_lat)
    
    # Filter our data to ONLY include buildings inside that box
    visible_gdf = gdf[gdf.geometry.intersects(screen_box)]

# Calculate totals for ONLY the visible buildings
total_buildings = len(visible_gdf)
total_kwh = visible_gdf['solar_potential_kwh'].sum()
total_savings = visible_gdf['money_saved'].sum()
total_co2 = visible_gdf['co2_saved_tonnes'].sum()
total_homes = visible_gdf['homes_powered'].sum()
total_evs = visible_gdf['evs_charged'].sum()

# --- THE CRAP-OPTIMIZED LEGEND ---
# --- THE FINAL POLISHED LEGEND ---
st.markdown(f'''
     <div style="
     position: fixed; top: 20px; right: 20px; width: 320px; 
     background-color: rgba(255, 255, 255, 0.98); 
     border: 1px solid #e0e0e0; z-index: 99999; font-family: sans-serif;
     border-radius: 12px; padding: 18px 20px; 
     box-shadow: 0px 8px 24px rgba(0,0,0,0.15);
     ">
     
     <h4 style="color: #111; margin: 0 0 4px 0; font-size: 15px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;">
         Live Screen Analytics
     </h4>
     
     <div style="display: flex; align-items: baseline; margin-bottom: 2px;">
         <span style="font-weight: 600; color: #555; font-size: 14px; width: 140px;">Buildings Detected:</span>
         <span style="font-size: 18px; font-weight: 700; color: #1a1a1a;">{total_buildings}</span>
     </div>
     
     <div style="display: flex; align-items: baseline; margin-bottom: 2px;">
         <span style="font-weight: 600; color: #555; font-size: 14px; width: 140px;">Energy Potential:</span>
         <span style="font-size: 18px; font-weight: 700; color: #FF9F00;">{total_kwh:,.0f} <span style="font-size: 12px;">kWh/yr</span></span>
     </div>
     
     <div style="display: flex; align-items: baseline; margin-bottom: 12px; border-bottom: 1px solid #f0f0f0; padding-bottom: 12px;">
         <span style="font-weight: 600; color: #555; font-size: 14px; width: 140px;">Est. Savings:</span>
         <span style="font-size: 18px; font-weight: 700; color: #10B981;">${total_savings:,.0f}<span style="font-size: 12px;">/yr</span></span>
     </div>
     
     <h4 style="color: #111; margin: 0 0 4px 0; font-size: 15px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase;">
         Environmental Impact
     </h4>
     
     <div style="display: flex; align-items: baseline; margin-bottom: 2px;">
         <span style="font-weight: 600; color: #555; font-size: 14px; width: 140px;">CO₂ Prevented:</span>
         <span style="font-size: 18px; font-weight: 700; color: #1a1a1a;">{total_co2:,.0f} <span style="font-size: 12px;">Tonnes</span></span>
     </div>
     
     <div style="display: flex; align-items: baseline; margin-bottom: 2px;">
         <span style="font-weight: 600; color: #555; font-size: 14px; width: 140px;">Homes Powered:</span>
         <span style="font-size: 18px; font-weight: 700; color: #1a1a1a;">{total_homes:,.0f}</span>
     </div>
     
     <div style="display: flex; align-items: baseline; margin-bottom: 0px;">
         <span style="font-weight: 600; color: #555; font-size: 14px; width: 140px;">EVs Charged:</span>
         <span style="font-size: 18px; font-weight: 700; color: #1a1a1a;">{total_evs:,.0f}</span>
     </div>
     
     </div>
''', unsafe_allow_html=True)