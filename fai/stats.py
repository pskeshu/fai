import numpy as np
from scipy import stats


def ignore_zero(data):
    """Returns array without zeros.

    Parameters
    ----------
    data : array

    Returns
    -------
    data : array
        without any zeros in the array
    """
    return data[np.nonzero(data)]


def pearson(x, y, without_zero=False):
    """Calculate the Pearson's correlation coefficient (PCC).

    Parameters
    ----------
    x : (N,) array

    y : (N,) array

    without_zero : bool
        if `without_zero` is True:
            PCC for the array, without counting the zeros.

        if `without_zero` is False
            PCC for the array, counting the zeros.

    Returns
    -------
    r : float
        Pearson's correlation coefficient

    p-value : float
        2-tailed p-value
    """
    if without_zero:
        x = ignore_zero(x)
        y = ignore_zero(y)

    return stats.pearsonr(x, y)


def mean(image, without_zero=False, roundval=None):
    """Calculate the mean value of an array.

    Parameters
    ----------
    image : (N, M) numpy array

    without_zero : bool
        if `without_zero` is True:
            mean of all the values of the array, without counting the zeros.

        if `without_zero` is False
            mean of all the values of the array, including the zeros.

    roundval : int
        Round off the decimal points of each element.

    Returns
    -------
    mean : float
    """

    image = np.float(image)

    if without_zero:
        image = util.ignore_zero(image)

    if roundval is not None:
        return round(np.mean(image), roundval)

    return np.mean(image)


def median(image, without_zero=False, roundval=None):
    """Calculate the median value of an array.

    Parameters
    ----------
    image : (N, M) numpy array

    without_zero : bool

    roundval : int
        Round off the decimal points of each element.

    Returns
    -------
    median : float
        if `without_zero` is True:
            median of all the values of the array, without counting the zeros.

        if `without_zero` is False
            median of all the values of the array, including the zeros.
    """
    image = np.float(image)

    if without_zero:
        image = util.ignore_zero(image)

    if roundval is not None:
        return round(np.median(image), roundval)

    return np.median(image)


def std(image):
    """Calculate the standard deviation value of an array.

    Parameters
    ----------
    image : (N, M) numpy array

    without_zero : bool

    roundval : int
        Round off the decimal points of each element.

    Returns
    -------
    standard deviation : float
        if `without_zero` is True:
            standard deviation of all the values of the array, without
            counting the zeros.

        if `without_zero` is False
            standard deviation of all the values of the array, including
            the zeros.
    """
    image = np.float(image)

    if without_zero:
        image = util.ignore_zero(image)

    if roundval is not None:
        return round(np.std(image), roundval)

    return np.std(image)
