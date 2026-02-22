import geopandas as gpd

gdf = gpd.read_file("data.geojson")
gdf.to_parquet("data.parquet", index=False)