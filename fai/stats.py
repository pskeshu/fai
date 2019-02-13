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


def pearson(x, y, without_zero=True):
    """Calculate the Pearson's correlation coefficient (PCC).

    Parameters
    ----------
    x : (N,) array

    y : (N,) array

    without_zero : bool
        if `without_zero` is True (default)
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


def mean(array, without_zero=True):
    """Calculate the mean value of an array.

    Parameters
    ----------
    array : (N, M) numpy array

    without_zero : bool
        if `without_zero` is True (default)
            mean of all the values of the array, without counting the zeros.

        if `without_zero` is False
            mean of all the values of the array, including the zeros.

    Returns
    -------
    mean : float
    """

    if without_zero:
        array = util.ignore_zero(array)

    return np.mean(array)


def median(array, without_zero=True):
    """Calculate the median value of an array.

    Parameters
    ----------
    array : (N, M) numpy array

    without_zero : bool
        if `without_zero` is True (default)
            median of all the values of the array, without counting the zeros.

        if `without_zero` is False
            median of all the values of the array, including the zeros.

    Returns
    -------
    median : float

    """
    if without_zero:
        array = util.ignore_zero(array)

    return np.median(array)


def std(array, without_zero=True):
    """Calculate the standard deviation value of an array.

    Parameters
    ----------
    array : (N, M) numpy array

    without_zero : bool
        if `without_zero` is True (default)
            standard deviation of all the values of the array, without
            counting the zeros.

        if `without_zero` is False
            standard deviation of all the values of the array, including
            the zeros.

    Returns
    -------
    standard deviation : float
    """
    if without_zero:
        array = util.ignore_zero(array)

    return np.std(array)


def sem(array, without_zero=True):
    """Calculate the standard error in mean for an array.

    Parameters
    ----------
    array : (N,) numpy array

    without_zero : bool
        if `without_zero` is True (default)
            standard error of all the values of the array, without
            counting the zeros.

        if `without_zero` is False
            standard error of all the values of the array, including
            the zeros.

    Returns
    -------
    standard error : float
        The standard error in mean for the given array
    """
    if without_zero:
        array = util.ignore_zero(array)

    return stats.sem(array)
