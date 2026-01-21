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
        # car le set permet de voir les valeurs uniques

    raster_epsg = raster_epsgs[0]

    # EPSG du shapefile
    shp_epsg = gpd.read_file(shp_path).crs.to_epsg()

    # Compare raster vs shapefile
    if raster_epsg == shp_epsg:
        return f"✅ Tous les CRS sont identiques (EPSG:{raster_epsg})"
    else:
        return f"⚠️ CRS différent (rasters:{raster_epsg} vs shp:{shp_epsg})"


def verif_rasters_geom(raster_dir, bands):

    gdal.UseExceptions()

    pixel_sizes = []
    dimensions = []

    for b in bands:
        path = os.path.join(raster_dir, f"bretagne_24-25_{b}.tif")
        ds = gdal.Open(path)

        # Taille des pixels
        gt = ds.GetGeoTransform()
        pixel_size = (gt[1], abs(gt[5]))  # (x, y)
        pixel_sizes.append(pixel_size)

        # Dimensions
        dims = (ds.RasterXSize, ds.RasterYSize)
        dimensions.append(dims)

        ds = None

    if len(set(pixel_sizes)) != 1:
        return f"⚠️ Tailles de pixels différentes : {pixel_sizes}"

    if len(set(dimensions)) != 1:
        return f"⚠️ Dimensions différentes : {dimensions}"

    return f"✅ Toutes les bandes ont la même taille de pixel {pixel_sizes[0]} et les mêmes dimensions {dimensions[0]}"
