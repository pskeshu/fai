import numpy as np


def pad(list_of_images):
    """Add padding to the edges of an image.

    Parameters
    ----------
    list_of_images : list or array

    Return
    ------
    padded_list : ndarray
        Images with same x, y dimension
    """
    padded_list = []
    a = 0
    b = 0
    for nuclei in list_of_images:
        x, y = nuclei.shape
        if x > a:
            a = x
        if y > b:
            b = y

    for nuclei in list_of_images:
        nuc_a, nuc_b = nuclei.shape
        if b > a:
            limit_a = int(round(b/2)) - int(round(nuc_a/2))
            limit_b = int(round((b - nuc_b)/2))
            padded = np.zeros([b, b])
            padded[limit_a:nuc_a + limit_a,
                   limit_b:nuc_b + limit_b] = nuclei
        else:
            limit_a = int(round((a - nuc_a)/2))
            limit_b = int(round(a/2)) - int(round(nuc_b/2))
            padded = np.zeros([a, a])
            padded[limit_a:nuc_a + limit_a,
                   limit_b:nuc_b + limit_b] = nuclei

        padded_list.append(padded)
    return np.asarray(padded_list)


def iterate(func, iterable, **kwds):
    """Iterate through an iterable, and use as values for the given
    function. Similar to map().

    Parameters
    ----------
    func : function

    iterable : list or array

    kwds : optional kwds to pass to function

    Return
    ------
    values : list
        list of values returned by the function for elements in iterable
    """
    values = []

    for i in iterable:
        values.append(func(i, **kwds))

    return values
