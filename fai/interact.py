import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


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
