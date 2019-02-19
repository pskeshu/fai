import csv
from dataclasses import dataclass
import numpy as np
import pickle


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

    # Cropped parallel and perpendicular image that is
    # used to calculate anisotropy
    parallel_roi_cropped: np.ndarray = None
    perpendicular_roi_reg_cropped: np.ndarray = None

    # Calculated anisotropy
    anisotropy_raw: np.ndarray = None  # Raw data
    anisotropy_round: np.ndarray = None  # Rounded to 3 decimal points
    # Median filtered after calculating anisotropy
    anisotropy_round_median: np.ndarray = None

    # Stats from anisotropy_round_median for plotting line curves.
    mean: list = None
    median: list = None

    # r_t - r_0
    mean_delta: list = None
    median_delta: list = None

    # r_t/r_0
    mean_norm: list = None
    median_norm: list = None

    # If we are multiplexing, with a second fluorophore
    # For instance, two color live imaging of cb.
    secondary_parallel: np.ndarray = None
    secondary_perpendicular: np.ndarray = None

    secondary_parallel_roi: np.ndarray = None
    secondary_perpendicular_roi: np.ndarray = None


def save(dataclass_object, filename):
    """Save the pickled dataclass object to a file.

    Parameters
    ----------
    dataclass_object : dataclass
        dataclass to be pickled and saved to disk

    filename : str

    Returns
    -------
    None
    """
    with open(filename, "wb") as file:
        pickle.dump(dataclass_object, file)
    return


def read(filename, minimal=True):
    """Read the dataclass object from a file.

    Parameters
    ----------
    filename : str

    minimal : bool
        Sets some of the dataclass attributes to `None`
        to reduce the amount of data stored in memory

    Returns
    -------
    data : dataclass object
    """
    with open(filename, "rb") as file:
        data = pickle.load(file)

    if minimal:
        data.parallel = None
        data.parallel_roi = None

        data.perpendicular = None
        data.perpendicular_roi = None
        data.perpendicular_roi_reg = None

        data.mask_roi = None
        data.mask_roi_cropped = None
    return data


def write_to_csv(lists, filename):
    """Write lists to a csv file.

    Parameters
    ----------
    lists : list of lists

    filename : str

    Returns
    -------
    None
    """
    column_transformed = np.array(lists).T

    with open(filename, 'w') as csvfile:
        wr = csv.writer(csvfile)
        for column in column_transformed:
            wr.writerow(column)

    return
