import matplotlib.pyplot as plt
import numpy as np

def imshow_multiple(
    images, direction="row", titles=None, base_figsize=4, **imshow_kwargs
):
    """
    Display multiple images as rows or columns, attempting
    to infer the correct dimensions for the plot from 
    `base_figsize` and the worst aspect ratio among `images`.
    """
    titles = [None for _ in images] if titles is None else titles
    plotshape = (1, len(images)) if direction == "row" else (len(images), 1)
    shapes = np.array([i.shape[:2] for i in images])
    if direction == "row":
        width, height = shapes[:, 1].sum(), shapes[:, 0].max()
    else:
        width, height = shapes[:, 1].max(), shapes[:, 0].sum()
    if (aspect := width / height) > 1:
        width_i, height_i = base_figsize * aspect, base_figsize
    else:
        width_i, height_i = base_figsize, base_figsize * aspect
    fig, axes = plt.subplots(*plotshape, figsize=(width_i, height_i))
    axes = [axes] if len(images) == 1 else axes
    for im, ax, title in zip(images, axes, titles):
        ax.imshow(im, **imshow_kwargs)
        if title is not None:
            ax.set_title(title)
    return fig, axes
