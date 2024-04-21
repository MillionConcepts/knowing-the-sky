import cv2
import numpy as np


def mask2vec(arr):
    """
    Converts the truthy elements of an ndarray into an array of "vectors"
    suitable for use by OpenCV geometry functions.
    """
    return np.vstack(np.nonzero(arr.T)).T


def mask2shape(
    mask, 
    shape = "circle", 
    color = (0, 255, 255), 
    thickness = 2,
    draw_on_array = False
):
    """
    Draws the smallest possible circle, triangle, or rectangle around the 
    'truthy' elements of a boolean or 0/1-valued ndarray. Returns both the 
    shape parameters and the shape drawn in an ndarray. If `draw_on_mask` is 
    True, draws the shape on top of the existing elements of the mask.
    """
    if shape not in {"circle", "triangle", "rectangle"}:
        raise ValueError("Shape can be 'circle', 'triangle', or 'rectangle'.")
    if draw_on_array is False:
        canvas = np.zeros([*mask.shape, 3], 'u1')
    else:
        canvas = np.moveaxis(
            np.tile(np.where(mask, 255, 0).astype('u1'), [3, 1, 1]), 2, 1
        ).T.copy()
    # We can generally get faster results by finding the extreme outer
    # contour of the shape rather than directly reducing it to point 
    # vectors (which implies something about how optimized findContours() is...)
    (cont,), _ = cv2.findContours(
        mask.astype('u1'), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    param = {}
    if shape == "circle":
        (param['cx'], param['cy']), param['r'] = cv2.minEnclosingCircle(cont)
        cx, cy, r = map(lambda p: int(round(p)), param.values())
        return param, cv2.circle(canvas, (cx, cy), r, color, thickness)
    if shape == "triangle":
        param['area'], param['points'] = cv2.minEnclosingTriangle(cont)
        return param, cv2.drawContours(
            canvas, [param['points'].round().astype('i4')], 0, color, thickness
        )
    param['ul'], param['lr'], param['angle'] = cv2.minAreaRect(cont)
    return param, cv2.drawContours(
        canvas, 
        [cv2.boxPoints(tuple(param.values())).round().astype('i4')],
        0,
        color,
        thickness
    )
