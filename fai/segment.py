from fai import interact, process, util
import numpy as np
import scipy.ndimage as ndi


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
    midpoint = int(x / 2)

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


def identify_nucleus(image):
    """Segment nucleus from an image

    Parameters
    ----------
    image : (N, M) array
        Image to segment

    Returns
    -------
    mask : (N, M) bool array
        Masked image
    """
    image = process.gaussian(image, sigma=3)
    thres = process.otsu(image)
    mask = image > thres - 60
    mask = process.clear_border(mask)
    mask = process.fill_holes(mask)
    mask = process.remove_small(mask, 1000)
    return mask


def nuclei_mask(images):
    """Helper function for `identify_nucleus`

    Parameters
    ----------
    images : (S, N, M) array
        Images to segment

    Returns
    -------
    masks : (S, N, M) bool array
        Masked images
    """
    masks = []

    for img in images:
        mask = identify_nucleus(img)
        masks.append(mask)
    masks = np.array(masks)

    return masks


def nuclei(dataclass):
    """Segment nuclei in a series of image.

    Parameters
    ----------
    dataclass : AnisotropyData dataclass
        `parallel_roi` and `perpendicular_roi` is used.

    Returns
    -------
    dataclass : AnisotropyData dataclass

    Updates 
    -------
    `mask_roi` : binary mask of the region of interest
    `

    """

    # Read the parallel and perpendicular RoI region
    # This has the manually defined approximate region around the cells
    parallel_roi = dataclass.parallel_roi
    perpendicular_roi = dataclass.perpendicular_roi_reg

    # Binarize the image, with True values corresponding
    # to region of the nucleus
    mask_roi = nuclei_mask(parallel_roi)

    # Store the mask over the RoI
    dataclass.mask_roi = mask_roi

    # Find best way to crop the cell out of the mask
    z, x, y = crop_mask(mask_roi)

    # Crop the parallel and perpendicular RoI with the calculated slice objects
    # and multiply with the mask to eliminate the pixels outside the nucleus
    cropped_mask_roi = mask_roi[z, x, y]
    cropped_parallel_roi = cropped_mask_roi * parallel_roi[z, x, y]
    cropped_perpendicular_roi = cropped_mask_roi * perpendicular_roi[z, x, y]

    # Store the cropped parallel and perpendicular images channels,
    # containing the nuclei information alone, to the dataclass
    dataclass.mask_roi_cropped = util.pad(cropped_mask_roi)
    dataclass.parallel_roi_cropped = util.pad(cropped_parallel_roi)
    dataclass.perpendicular_roi_reg_cropped = util.pad(cropped_perpendicular_roi)

    return dataclass


def crop_mask(mask):
    """Identify objects in a mask, and crop around the bounding box of the
    object.

    Parameters
    ----------
    mask : (S, N, M) array
        Mask to crop

    Returns
    -------
    slice_ : tuple
        Slice object to crop the image
    """
    labelled_mask = ndi.label(mask)[0]
    slice_ = ndi.find_objects(labelled_mask, max_label=1)[0]
    return slice_
