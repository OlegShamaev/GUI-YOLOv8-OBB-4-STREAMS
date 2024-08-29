import numpy as np
import os
import cv2 as cv
from collections import namedtuple
import abc
from src.utils.general import path_leaf
import time


class ModelError(Exception):
    pass


Model = namedtuple("Model", "model confidence_threshold iou_threshold input_size class_names")


class YoloPredictorBase(object):
    def __init__(self):
        self._model = None

    @abc.abstractmethod
    def init(self):
        return NotImplemented

    @abc.abstractmethod
    def postprocess(self, model_output, scale):
        return NotImplemented

    @abc.abstractmethod
    def inference(self, image):
        return NotImplemented

    @abc.abstractstaticmethod
    def draw_results(self, image, model_results):
        return NotImplemented
