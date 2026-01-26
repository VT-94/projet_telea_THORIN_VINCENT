import numpy as np


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
