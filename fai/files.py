from dataclasses import dataclass
import os
import glob
import tifffile
import numpy as np


@dataclass
class AnisotropyData:
    filename: str
    raw_data: np.ndarray
    metadata: dict

    # The raw parallel and perpendicular channels
    parallel: np.ndarray = None
    perpendicular: np.ndarray = None

    # Region of interest is generally drawn manually
    # around a nucleus. The perpendicular component
    # is registered, with respect to the parallel
    # component which is kept fixed in position.
    parallel_roi: np.ndarray = None
    perpendicular_roi: np.ndarray = None
    perpendicular_roi_reg: np.ndarray = None

    # Segmented binary mask from parallel_roi
    mask_roi: np.ndarray = None

    # Cropped binary mask - nucleus in a bounding box
    mask_roi_cropped: np.ndarray = None

    # Cropped parallel and perpendicular image
    parallel_roi_cropped: np.ndarray = None
    perpendicular_roi_reg_cropped: np.ndarray = None

    # Calculated anisotropy - typically from the
    # cropped parallel and perpendicular image.
    anisotropy: np.ndarray = None

    # Stats from anisotropy data
    # For plotting
    mean: list = None
    median: list = None
    mean_norm: list = None
    median_norm: list = None

    # If we are multiplexing, with a second fluorophore
    # For instance, two color live imaging of cb.
    secondary_parallel: np.ndarray = None
    secondary_perpendicular: np.ndarray = None

    secondary_parallel_roi: np.ndarray = None
    secondary_perpendicular_roi: np.ndarray = None


def only(file_list, keyword):
    """Helper function to return files from list of files that match the
    items in the keyword.

    Parameters
    ----------
    file_list : list
        List with paths to differnt files that needs to be filtered.

    keyword : str
        Keyword that is to be used for the filtering criteria.

    Returns
    -------
    list_ : list
        This is the list which has all the elements of file_list after
        filtering with keyword.
    """
    list_ = [_ for _ in file_list if all(key in _ for key in keyword)]
    return sorted(list_)


def skip(file_list, keyword):
    """Helper function to return files from list of files that does not match
    the items in the keyword.

    Parameters
    ----------
    file_list : list
        List with paths to differnt files that needs to be filtered.

    keyword : str
        Keyword that is to be used for the filtering criteria.

    Returns
    -------
    list_ : list
        This is the list which has all the elements of file_list after
        filtering with keyword.
    """
    list_ = [_ for _ in file_list if all(key not in _ for key in keyword)]
    return sorted(list_)


def ls(keyword="./", only=None, skip=None):
    """Returns the path to all the files in a path as specified in the
    keyword. If a "*" is detected in the keyword, glob is used to run the
    search.

    Parameters
    ----------
    keyword : str, optional
        Keyword that specifies the path to images.

    only : list, optional
        List of secondary keywords to filter file names. Only filenames with
        these keywords will be returned.

    skip : list, optional
        List of secondary keywords to filter file names. Only filenames that
        do not have these keywords will be returned.

    Returns
    -------
    file_list : list
        List of files that match the keyword, and the only and skip criteria.
    """
    if "*" in keyword:
        return sorted(glob.glob(keyword))

    file_list = []
    for paths, subdirs, files in os.walk(keyword):
        for name in files:
            file_list.append(os.path.join(paths, name))

    if only is not None:
        file_list = only(file_list, only)

    if skip is not None:
        file_list = skip(file_list, skip)

    return sorted(file_list)


def mkdir(path):
    """Make a directory.

    Parameters
    ----------
    path : str
        The path for which the function checks if the folder exists, and makes
        a directory if it does not.

    Returns
    -------
    None
    """

    if not os.path.exists(path):
        os.makedirs(path)
    return


def file_exists(filename):
    """Function to check if a file exists.

    Parameters
    ----------
    filename : str
        The path of the file that needs to be verified if it exists.it

    Returns
    -------
    bool
        True if the file exists.
        False if the file does not exist.
    """
    return os.path.isfile(filename)


def imread(filename):
    """Wrapper for Tifffile to read images as int16 and returns a dataclass
    with the image data.

    Parameters
    ----------
    filename : str
        Image file that has to be opened.

    Returns
    -------
    dataclass

    Notes
    -----
    The images can be opened and analysed as floating point numbers.
    """
    raw_data = tifffile.imread(filename).astype(np.int16)
    return AnisotropyData(filename=filename, raw_data=raw_data, metadata={})


def imsave(array, filename):
    """Wrapper for Tifffile to save images.

    Parameters
    ----------
    array : N-dimensional numpy array
        Image file that has to be saved.

    filename : str
        Filename for the image to be saved as.

    Returns
    -------
    None
    """
    with tifffile.TiffWriter(filename, bigtiff=False) as tif:
        tif.save(array)
    return


def arsave(array, filename):
    """Save a numpy array to disk.

    Parameters
    ----------
    array : N-dimensional numpy array
        Array to be saved to disk

    filename : str
        Filename for the array.

    Returns
    -------
    None
    """
    np.save(filename, array)
    return


def arread(filename):
    """Read a numpy array binary file from disk.

    Parameters
    ----------
    filename : str
        Filename for the array.

    Returns
    -------
    array : N-dimensional numpy array
    """
    array = np.load(filename)
    return array
