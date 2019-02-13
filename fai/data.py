from dataclasses import dataclass
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
    anisotropy_raw: np.ndarray = None  # Raw data
    anisotropy_round: np.ndarray = None  # Rounded to 3 decimal points
    anisotropy_round_median: np.ndarray = None  # Median filtered

    # Stats from anisotropy_round_median for plotting line curves.
    mean: list = None
    median: list = None
    std: list = None
    sem: list = None

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
