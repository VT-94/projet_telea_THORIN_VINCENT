import numpy as np


def calcul_navi(img, nodata=-9999.0, idx_b03=1, idx_b05=3):
    """
    Calcule le NARI (Normalized Anthocyanin Reflectance Index) pour UNE image multi-bandes.

    Parameters
    ----------
    img : ndarray (rows, cols, bands)
        Image Sentinel-2 (float ou convertible) avec les bandes empilées.
    nodata : float
        Valeur NoData en sortie.
    idx_b03 : int
        Index (python) de la bande B03 dans img.
    idx_b05 : int
        Index (python) de la bande B05 dans img.

    Returns
    -------
    nari : ndarray (rows, cols) float32
        Carte NARI pour l'image.
    """

    img = img.astype("float32", copy=False)

    B03 = img[:, :, idx_b03]
    B05 = img[:, :, idx_b05]

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