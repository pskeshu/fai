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
