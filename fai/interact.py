import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RectangleSelector


def create_circular_mask(images, centers, radius):
    """Create a circular mask for a stack of images, given their centers
    and radius.

    Parameters
    ----------
    images : (S, N, M) numpy array
        The images for which the mask is to the generated.

    centers : list of x, y coords
        list of coordinates that describes the center of the circular mask

    radius : int
        Radius of the circular mask


    Returns
    -------
    mask : (S, N, M) boolean numpy array
    """
    masks = []
    for image, center in zip(images, centers):
        h, w = image.shape
        Y, X = np.ogrid[:h, :w]

        dist_from_center = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
        mask = dist_from_center <= radius
        masks.append(mask)
    return np.array(masks)


def roi_circle(img, radius=10):
    """
    Click to interactively draw a circular RoI for a stack of images.

    Parameters
    ----------
    img : (S, N, M) numpy array
        Images for which to draw RoI

    radius : int
        Radius of the RoI

    Returns
    -------
    masked image : (S, N, M) numpy array
        RoI

    centers : (N,) array
        list of x, y coordinates of the center of RoI
    """
    if img.ndim is not 3:
        raise ValueError("Not a 3D image.")

    centers = [[None, None] for n in img]
    current_num = [0]
    clicks = [None]

    def update_centers(value, first_click):
        if first_click:
            for i in range(len(centers)):
                centers[i] = value
            clicks[0] = 1
        else:
            num = current_num[0]
            for i in range(num, len(centers)):
                centers[i] = value

    def on_press(event):
        if event.inaxes is not ax:
            return

        if event.inaxes is zbox:
            return

        if fig.canvas.manager.toolbar._active is not None:
            return

        center = [event.xdata, event.ydata]
        if clicks[0] is None:
            update_centers(center, True)
        else:
            update_centers(center, False)

        draw_circle()

    def draw_circle():
        num = current_num[0]
        circ.center = centers[num]
        circ.radius = radius
        fig.canvas.draw_idle()

    def update_image(num):
        num = int(num)
        current_num[0] = num
        image = np.squeeze(img[num:num+1])
        image_ax.set_data(image)
        draw_circle()
        fig.canvas.draw_idle()

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)

    image_ax = ax.imshow(img[0], cmap=plt.cm.gray)
    ax.axis("off")

    circ = plt.Circle([None, None], 10, ec="k", alpha=0.7)
    ax.add_patch(circ)

    zbox = plt.axes([0.1, 0.05, 0.8, 0.025])

    zslide = Slider(zbox, 'Z', 0, img.shape[0] - 1, valinit=0, valfmt="%i")
    zslide.on_changed(update_image)

    cid = fig.canvas.mpl_connect('button_press_event', on_press)

    plt.show()

    if [None, None] in centers:
        return None, None
    mask = create_circular_mask(img, centers, radius)
    return mask * img, np.array(centers)


def create_rectangular_mask(image, click, release):
    """
    Given the edges, crop a rectangular region from an image.

    Parameters
    ----------
    image : (S, N, M) numpy array
        Image that needs to be cropped

    click : (2,) array or list
        Starting coords of the diagonal of the rectangle

    release : (2,) array or list
        Ending coords of the diagonal of the rectangle

    Returns
    -------
    roi : (S, N, M) numpy array
        Segmented RoI
    """
    x1, y1 = click
    x2, y2 = release
    return image[:,  y1:y2, x1:x2]


def roi_rectangle(img):
    """
    Click to interactively draw a rectangular RoI for a stack of images.

    Parameters
    ----------
    img : (S, N, M) numpy array
        Images for which to draw RoI

    Returns
    -------
    roi : (S, N, M) numpy array
        Segmented RoI
    """
    if img.ndim is not 3:
        raise ValueError("Not a 3D image.")

    click = [None, None]
    release = [None, None]

    def on_press(event):
        if event.inaxes is not ax:
            return

        if event.inaxes is zbox:
            return

        if fig.canvas.manager.toolbar._active is not None:
            return

    def update_image(num):
        num = int(num)
        image = np.squeeze(img[num:num+1])
        image_ax.set_data(image)
        fig.canvas.draw_idle()

    def line_select_callback(eclick, erelease):
        click[:] = eclick.xdata, eclick.ydata
        release[:] = erelease.xdata, erelease.ydata

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)

    image_ax = ax.imshow(img[0], cmap=plt.cm.gray)
    ax.axis("off")

    zbox = plt.axes([0.1, 0.05, 0.8, 0.025])

    zslide = Slider(zbox, 'Z', 0, img.shape[0] - 1, valinit=0, valfmt="%i")
    zslide.on_changed(update_image)

    cid = fig.canvas.mpl_connect('button_press_event', on_press)
    rs_selector = RectangleSelector(ax, line_select_callback,
                                        drawtype="box", interactive=True)
    plt.show()

    click = list(map(int, click))
    release = list(map(int, release))

    roi = create_rectangular_mask(img, click, release)
    return roi, [click, release]
