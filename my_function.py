import os
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt


def calcul_nari(img, nodata=-9999.0):
    """
    Calcule le NARI (Normalized Anthocyanin Reflectance Index) pour UNE image.

    img : array (lignes, colonnes, bandes)
        Image avec les bandes spectrales empilées.
    nodata : float
        Valeur NoData voulue en sortie.
    """

    img = img.astype("float32", copy=False)

    B03 = img[:, :, 1]
    B05 = img[:, :, 3]

    valid = (B03 != 0) & (B05 != 0) & np.isfinite(B03) & np.isfinite(B05)

    nari = np.full(B03.shape, nodata, dtype="float32")

    inv_B03 = np.zeros_like(B03, dtype="float32")
    inv_B05 = np.zeros_like(B05, dtype="float32")

    inv_B03[valid] = 1.0 / B03[valid]
    inv_B05[valid] = 1.0 / B05[valid]

    den = inv_B03 + inv_B05
    valid2 = valid & (den != 0)

    nari[valid2] = (inv_B03[valid2] - inv_B05[valid2]) / den[valid2]

    return nari


def rasterise_gdal(shp_path, ref_image, out_raster, attribute, gdal_dtype, fill_value=0):
    """
    Rasterise un shapefile sur la grille d'un raster de référence.

    shp_path   : chemin du shapefile
    ref_image  : raster de référence (grille)
    out_raster : raster de sortie (.tif)
    attribute  : champ à rasteriser
    gdal_dtype : type GDAL de sortie (ex: gdal.GDT_Int16, gdal.GDT_Int32)
    fill_value : valeur de fond (par défaut 0)
    """

    os.makedirs(os.path.dirname(out_raster), exist_ok=True)

    ref_ds = gdal.Open(ref_image)

    cols, rows = ref_ds.RasterXSize, ref_ds.RasterYSize
    gt, proj = ref_ds.GetGeoTransform(), ref_ds.GetProjection()

    drv = gdal.GetDriverByName("GTiff")
    out_ds = drv.Create(out_raster, cols, rows, 1, gdal_dtype)
    out_ds.SetGeoTransform(gt)
    out_ds.SetProjection(proj)
    out_ds.GetRasterBand(1).Fill(fill_value)

    # Rasterisation (écrit l'attribut dans le raster)
    gdal.Rasterize(out_ds, shp_path, attribute=attribute)

    out_ds = None
    ref_ds = None


def plot_contrib(importances, bands, dates, mode="bands", ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))

    import numpy as np

    n_bands = len(bands)
    n_dates = len(dates)

    contrib = {}

    if mode == "bands":
        for i, b in enumerate(bands):
            idx = np.arange(i, n_bands * n_dates, n_bands)
            contrib[b] = importances[idx].sum()
        title = "Contribution des bandes"

    elif mode == "dates":
        for i, d in enumerate(dates):
            idx = slice(i * n_bands, (i + 1) * n_bands)
            contrib[d] = importances[idx].sum()
        title = "Contribution des dates"

    labels = list(contrib.keys())
    values = list(contrib.values())

    ax.bar(labels, values)
    ax.set_title(title)
    ax.set_ylim(0, 0.2)
    ax.tick_params(axis="x", rotation=45)
