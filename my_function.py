from osgeo import gdal
import geopandas as gpd
import os


def verif_crs(raster_dir, bands, shp_path):
    gdal.UseExceptions()  # supprime les warnings

    # Récupère l'EPSG de toutes les bandes
    raster_epsgs = []
    for b in bands:
        path = os.path.join(raster_dir, f"bretagne_24-25_{b}.tif")
        ds = gdal.Open(path)
        epsg = int(ds.GetSpatialRef().GetAttrValue("AUTHORITY", 1))
        raster_epsgs.append(epsg)
        ds = None

    # Vérifie si toutes les bandes ont le même EPSG
    if len(set(raster_epsgs)) != 1:
        return f"⚠️ Les CRS des rasters ne sont pas tous identiques : {raster_epsgs}"

    raster_epsg = raster_epsgs[0]

    # EPSG du shapefile
    shp_epsg = gpd.read_file(shp_path).crs.to_epsg()

    # Compare raster vs shapefile
    if raster_epsg == shp_epsg:
        return f"✅ Tous les CRS sont identiques (EPSG:{raster_epsg})"
    else:
        return f"⚠️ CRS différent (rasters:{raster_epsg} vs shp:{shp_epsg})"
