import numpy as np
from src.utils.logging_config import logger


def xywh2xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y


def xyxy2xywh(bboxes):
    bboxes[:, 2] = bboxes[:, 2] - bboxes[:, 0]
    bboxes[:, 3] = bboxes[:, 3] - bboxes[:, 1]
    return bboxes


def multiclass_nms_class_agnostic(boxes, scores, nms_thr, score_thr):
    """Multiclass NMS implemented in Numpy. Class-agnostic version."""
    cls_inds = scores.argmax(1)
    cls_scores = scores[np.arange(len(cls_inds)), cls_inds]

    valid_score_mask = cls_scores > score_thr
    if valid_score_mask.sum() == 0:
        return None
    valid_scores = cls_scores[valid_score_mask]
    valid_boxes = boxes[valid_score_mask]
    valid_cls_inds = cls_inds[valid_score_mask]

    keep = nms(valid_boxes, valid_scores, nms_thr)
    # dets = []
    for i in keep:
        dets = np.concatenate(
            [valid_boxes[keep], valid_scores[keep, None], valid_cls_inds[keep, None]], 1
        )
    return dets


def nms(boxes, scores, nms_thr):
    """Single class NMS implemented in Numpy."""
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= nms_thr)[0]
        order = order[inds + 1]
    return keep


def multiclass_nms_class_agnostic_keypoints(boxes, scores, kpts, nms_thr, score_thr):
    """Multiclass NMS implemented in Numpy. Class-agnostic version."""
    cls_inds = scores.argmax(1)
    cls_scores = scores[np.arange(len(cls_inds)), cls_inds]

    valid_score_mask = cls_scores > score_thr
    if valid_score_mask.sum() == 0:
        return None
    valid_scores = cls_scores[valid_score_mask]
    valid_boxes = boxes[valid_score_mask]
    valid_boxes = xywh2xyxy(valid_boxes)
    valid_cls_inds = cls_inds[valid_score_mask]
    valid_kpts = kpts[valid_score_mask]

    keep = nms(valid_boxes, valid_scores, nms_thr)
    dets = []
    for i in keep:
        dets = np.concatenate(
            [
                valid_boxes[keep],
                valid_scores[keep, None],
                valid_cls_inds[keep, None],
                valid_kpts[keep],
            ],
            1,
        )
    return dets


import numpy as np
from scipy.spatial import distance
import time


def non_max_suppression_obb(
    prediction,
    conf_thres=0.25,
    iou_thres=0.45,
    classes=None,
    agnostic=False,
    multi_label=False,
    max_det=300,
    nc=0,  # number of classes (optional)
    max_time_img=0.05,
    max_nms=30000,
    max_wh=7680,
):

    # Checks
    assert (
        0 <= conf_thres <= 1
    ), f"Invalid Confidence threshold {conf_thres}, valid values are between 0.0 and 1.0"
    assert 0 <= iou_thres <= 1, f"Invalid IoU {iou_thres}, valid values are between 0.0 and 1.0"

    if classes is not None:
        classes = np.array(classes)

    if prediction.shape[-1] == 6:  # end-to-end model (BNC, i.e. 1,300,6)
        output = [pred[pred[:, 4] > conf_thres] for pred in prediction]
        if classes is not None:
            output = [pred[np.any(pred[:, 5:6] == classes, axis=1)] for pred in output]
        return output

    bs = prediction.shape[0]  # batch size (BCN, i.e. 1,84,6300)
    nc = nc or (prediction.shape[1] - 4)  # number of classes
    nm = prediction.shape[1] - nc - 4  # number of masks
    mi = 4 + nc  # mask start index
    xc = np.max(prediction[:, 4:mi], axis=1) > conf_thres  # candidates

    # Settings
    time_limit = 2.0 + max_time_img * bs  # seconds to quit after
    multi_label &= nc > 1  # multiple labels per box (adds 0.5ms/img)

    prediction = np.transpose(prediction, (0, 2, 1))  # shape(1,84,6300) to shape(1,6300,84)

    # Process each image in the batch
    t = time.time()
    output = [np.zeros((0, 6 + nm))] * bs
    for xi, x in enumerate(prediction):  # image index, image inference
        x = x[xc[xi]]  # confidence
        # If none remain process next image
        if x.shape[0] == 0:
            continue

        # Detections matrix nx6 (xyxy, conf, cls)
        box, cls, mask = np.split(x, (4, 4 + nc), axis=1)

        if multi_label:
            i, j = np.where(cls > conf_thres)
            x = np.concatenate((box[i], x[i, 4 + j, None], j[:, None].astype(float), mask[i]), 1)
        else:  # best class only
            conf = cls.max(1, keepdims=True)
            j = cls.argmax(1, keepdims=True)
            x = np.concatenate((box, conf, j.astype(float), mask), 1)[conf.flatten() > conf_thres]

        # Filter by class
        if classes is not None:
            x = x[(x[:, 5:6] == classes).any(1)]

        # Check shape
        n = x.shape[0]  # number of boxes
        if n == 0:  # no boxes
            continue
        if n > max_nms:  # excess boxes
            x = x[
                np.argsort(x[:, 4])[::-1][:max_nms]
            ]  # sort by confidence and remove excess boxes

        # Batched NMS
        c = x[:, 5:6] * (0 if agnostic else max_wh)  # classes
        scores = x[:, 4]  # scores

        boxes = np.concatenate((x[:, :2] + c, x[:, 2:4], x[:, -1:]), axis=1)  # xywhr

        keep = nms(boxes, scores, iou_thres)
        keep = keep[:max_det]  # limit detections

        output[xi] = x[keep]
        if (time.time() - t) > time_limit:
            logger.warning(f"WARNING ⚠️ NMS time limit {time_limit:.3f}s exceeded")
            break  # time limit exceeded

    return output


def nms_rotated(boxes, scores, threshold=0.45):
    """
    Single class NMS for oriented bounding boxes (OBB) implemented in Numpy.
    NMS for obbs, powered by probiou and fast-nms.

    Args:
        boxes (np.ndarray): (N, 5), xywhr.
        scores (np.ndarray): (N, ).
        threshold (float): IoU threshold.

    Returns:
    """
    if len(boxes) == 0:
        return np.empty((0,), dtype=np.int8)

    sorted_idx = np.argsort(scores)[::-1]
    boxes = boxes[sorted_idx]
    ious = batch_probiou(boxes, boxes)  # Assuming batch_probiou is implemented for numpy
    ious = np.triu(ious, k=1)
    max_ious = np.max(ious, axis=0)
    pick = np.where(max_ious < threshold)[0]

    return sorted_idx[pick]


def batch_probiou(obb1, obb2, eps=1e-7):
    """
    Calculate the prob IoU between oriented bounding boxes, https://arxiv.org/pdf/2106.06072v1.pdf.

    Args:
        obb1 (np.ndarray): A tensor of shape (N, 5) representing ground truth obbs, with xywhr format.
        obb2 (np.ndarray): A tensor of shape (M, 5) representing predicted obbs, with xywhr format.
        eps (float, optional): A small value to avoid division by zero. Defaults to 1e-7.

    Returns:
        np.ndarray: A tensor of shape (N, M) representing obb similarities.
    """
    obb1 = np.asarray(obb1)
    obb2 = np.asarray(obb2)

    x1, y1 = obb1[..., :2].T
    x2, y2 = obb2[..., :2].T
    a1, b1, c1 = _get_covariance_matrix(obb1)
    a2, b2, c2 = _get_covariance_matrix(obb2)

    x2 = x2[:, None]
    y2 = y2[:, None]

    t1 = (
        ((a1[:, None] + a2) * (y1 - y2) ** 2 + (b1[:, None] + b2) * (x1 - x2) ** 2)
        / ((a1[:, None] + a2) * (b1[:, None] + b2) - (c1[:, None] + c2) ** 2 + eps)
    ) * 0.25
    t2 = (
        ((c1[:, None] + c2) * (x2 - x1) * (y1 - y2))
        / ((a1[:, None] + a2) * (b1[:, None] + b2) - (c1[:, None] + c2) ** 2 + eps)
    ) * 0.5
    t3 = (
        ((a1[:, None] + a2) * (b1[:, None] + b2) - (c1[:, None] + c2) ** 2)
        / (
            4
            * (
                np.clip(a1 * b1 - c1**2, 0, None)[:, None] * np.clip(a2 * b2 - c2**2, 0, None)
            ).sqrt()
            + eps
        )
        + eps
    ).log() * 0.5
    bd = np.clip(t1 + t2 + t3, eps, 100.0)
    hd = np.sqrt(1.0 - np.exp(-bd) + eps)
    return 1 - hd


def _get_covariance_matrix(boxes):
    """
    Generating covariance matrix from obbs.

    Args:
        boxes (np.ndarray): A tensor of shape (N, 5) representing rotated bounding boxes, with xywhr format.

    Returns:
        tuple: Covariance matrices corresponding to original rotated bounding boxes.
    """
    gbbs = np.concatenate((boxes[:, 2:4] ** 2 / 12, boxes[:, 4:]), axis=-1)
    a, b, c = gbbs.T
    cos = np.cos(c)
    sin = np.sin(c)
    cos2 = cos**2
    sin2 = sin**2
    return a * cos2 + b * sin2, a * sin2 + b * cos2, (a - b) * cos * sin
