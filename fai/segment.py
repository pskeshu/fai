from fai import interact
import numpy as np


def separate_channels(dataclass):
    """Separate the parallel and perpendicular channels of the image.

    Parameters
    ----------
    dataclass : AnisotropyData dataclass
        Image stored in the `raw_data` attribute.

    Returns
    -------
    dataclass : AnisotropyData dataclass
        Channels are stored in the `parallel` and `perpendicular` attributes.

    """
    image = dataclass.raw_data

    if image.ndim is not 3:
        raise("Not a 3D image")

    z, x, y = image.shape
    midpoint = int(x/2)

    diff = 50  # workaround to get roughly aligned parallel channel

    perpendicular = image[:, :midpoint, ]
    parallel = image[:, midpoint - diff:, ]

    dataclass.parallel = parallel
    dataclass.perpendicular = perpendicular

    metadata = dataclass.metadata
    metadata.update({"midpoint": midpoint, "diff": diff})

    return dataclass


def define_roi(dataclass):
    """Interactively define the region of interest to crop a smaller region
    from the field of view. This is useful to semi-automatically segment
    nucleus from the field when automatic segmentation results in sub-optimal
    segmentation.

    Parameters
    ----------
    dataclass : AnisotropyData dataclass
        Channels stored in the `parallel` and `perpendicular` attribute.

    Returns
    -------
    dataclass : AnisotropyData dataclass.
        Segmented regions are stored in the `parallel_roi` and
        `perpendicular_roi` attributes.

    """
    img_parallel = dataclass.parallel
    image_perpendicular = dataclass.perpendicular

    roi_parallel, coords = interact.roi_rectangle(img_parallel)
    roi_perpendicular = interact.create_rectangular_mask(
        image_perpendicular, *coords)

    dataclass.parallel_roi = roi_parallel
    dataclass.perpendicular_roi = roi_perpendicular

    metadata = dataclass.metadata
    metadata.update({"coords": coords})

    return dataclass

def autonuclei(dataclass):
    """Segment nucleus from an image.
    """
    parallel = dataclass.parallel_roi[0]
    from fai import view

    thres = process.otsu(parallel)

    view.dd(parallel)

    mask = parallel > thres - 60
    mask = process.remove_small(mask, 1000)
    mask = process.fill_holes(mask)


    pass
