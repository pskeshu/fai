# Note: compare the results for:
#   1. round() vs np.around()
#   2. np.float() vs float()

import numpy as np


def anisotropy(parallel, perpendicular, g_factor, bg):
    """Calculate anisotropy, given an image.

    Parameters
    ----------
    parallel : (N, M) numpy array
        The parallel component of the light.

    perpendicular : (N, M) numpy array
        The perpendicular component of the light.

    g_factor : float
        The correction factor for the bias in polarization.

    bg : float
        The constant background value to be subtracted from the image before
        calculating anisotropy. This is usually the baseline of the sensor.
        This value is generally 100.0 in the case of Andor Zyla 4.2 sCMOS
        camera.


    Returns
    -------
    image : (N, M) numpy array
        The anisotropy map, rounded off to the 3rd decimal value.

    """

    numerator = numerator - bg
    denominator = denominator - bg

    numerator = (parallel - (g_factor * perpendicular))
    denominator = (parallel + (2 * g_factor * perpendicular))

    with np.errstate(divide='ignore', invalid='ignore'):
        anisotropy_map = np.true_divide(numerator, denominator)
        anisotropy_map[~ np.isfinite(anisotropy_map)] = 0

    anisotropy_map[anisotropy_map >= 1] = 0
    anisotropy_map[anisotropy_map <= 0] = 0

    return np.round(anisotropy_map, 3)
