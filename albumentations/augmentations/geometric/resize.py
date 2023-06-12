import random
from typing import Dict, Sequence, Tuple, Union

import cv2
import numpy as np

from albumentations.core.transforms_interface import DicomType

from ...core.transforms_interface import (
    BoxInternalType,
    DualTransform,
    KeypointInternalType,
    to_tuple,
    INTER_LINEAR
)
from . import functional as F
from ..dicom import functional as Fdicom

__all__ = ["RandomScale", "LongestMaxSize", "SmallestMaxSize", "Resize"]


class RandomScale(DualTransform):
    """Randomly resize the input. Output image size is different from the input image size.

    Args:
        scale_limit ((float, float) or float): scaling factor range. If scale_limit is a single float value, the
            range will be (-scale_limit, scale_limit). Note that the scale_limit will be biased by 1.
            If scale_limit is a tuple, like (low, high), sampling will be done from the range (1 + low, 1 + high).
            Default: (-0.1, 0.1).
        interpolation (int): scipy interpolation method (e.g. albumenations3d.INTER_NEAREST). Default: albumentations3d.INTER_LINEAR
        p (float): probability of applying the transform. Default: 0.5.

    Targets:
        image, mask, bboxes, keypoints

    Image types:
        uint8, float32
    """

    def __init__(self, scale_limit=0.1, interpolation=cv2.INTER_LINEAR, always_apply=False, p=0.5):
        super(RandomScale, self).__init__(always_apply, p)
        self.scale_limit = to_tuple(scale_limit, bias=1.0)
        self.interpolation = interpolation

    def get_params(self):
        return {"scale": random.uniform(self.scale_limit[0], self.scale_limit[1])}

    def apply(self, img, scale=0, interpolation=INTER_LINEAR, **params):
        return F.scale(img, scale, interpolation)

    def apply_to_bbox(self, bbox, **params):
        # Bounding box coordinates are scale invariant
        return bbox

    def apply_to_keypoint(self, keypoint, scale=1, **params):
        return F.keypoint_scale(keypoint, scale, scale, scale)
    
    def apply_to_dicom(self, dicom: DicomType, scale = 1, **params) -> DicomType:
        return Fdicom.dicom_scale(dicom, scale, scale, scale)

    def get_transform_init_args(self):
        return {"interpolation": self.interpolation, "scale_limit": to_tuple(self.scale_limit, bias=-1.0)}


class LongestMaxSize(DualTransform):
    """Rescale an image so that maximum side is equal to max_size, keeping the aspect ratio of the initial image.

    Args:
        max_size (int, list of int): maximum size of the image after the transformation. When using a list, max size
            will be randomly selected from the values in the list.
        interpolation (int): scipy interpolation method (e.g. albumenations3d.INTER_NEAREST). Default: albumentations3d.INTER_LINEAR
        p (float): probability of applying the transform. Default: 1.

    Targets:
        image, mask, bboxes, keypoints

    Image types:
        uint8, float32
    """

    def __init__(
        self,
        max_size: Union[int, Sequence[int]] = 1024,
        interpolation: int = 1,
        always_apply: bool = False,
        p: float = 1,
    ):
        super(LongestMaxSize, self).__init__(always_apply, p)
        self.interpolation = interpolation
        self.max_size = max_size

    def apply(
        self, img: np.ndarray, max_size: int = 1024, interpolation: int = INTER_LINEAR, **params
    ) -> np.ndarray:
        return F.longest_max_size(img, max_size=max_size, interpolation=interpolation)

    def apply_to_bbox(self, bbox: BoxInternalType, **params) -> BoxInternalType:
        # Bounding box coordinates are scale invariant
        return bbox

    def apply_to_keypoint(self, keypoint: KeypointInternalType, max_size: int = 1024, **params) -> KeypointInternalType:
        height = params["rows"]
        width = params["cols"]
        depth = params["slices"]

        scale = max_size / max([height, width, depth])
        return F.keypoint_scale(keypoint, scale, scale, scale)
    
    def apply_to_dicom(self, dicom: DicomType, max_size: int = 1024, **params) -> DicomType:
        height = params["rows"]
        width = params["cols"]
        depth = params["slices"]
        scale = max_size / min([height, width, depth])
        return Fdicom.dicom_scale(dicom, scale, scale, scale)

    def get_params(self) -> Dict[str, int]:
        return {"max_size": self.max_size if isinstance(self.max_size, int) else random.choice(self.max_size)}

    def get_transform_init_args_names(self) -> Tuple[str, ...]:
        return ("max_size", "interpolation")


class SmallestMaxSize(DualTransform):
    """Rescale an image so that minimum side is equal to max_size, keeping the aspect ratio of the initial image.

    Args:
        max_size (int, list of int): maximum size of smallest side of the image after the transformation. When using a
            list, max size will be randomly selected from the values in the list.
        interpolation (int): scipy interpolation method (e.g. albumenations3d.INTER_NEAREST). Default: albumentations3d.INTER_LINEAR
        p (float): probability of applying the transform. Default: 1.

    Targets:
        image, mask, bboxes, keypoints

    Image types:
        uint8, float32
    """

    def __init__(
        self,
        max_size: Union[int, Sequence[int]] = 1024,
        interpolation: int = 1,
        always_apply: bool = False,
        p: float = 1,
    ):
        super(SmallestMaxSize, self).__init__(always_apply, p)
        self.interpolation = interpolation
        self.max_size = max_size

    def apply(
        self, img: np.ndarray, max_size: int = 1024, interpolation: int = cv2.INTER_LINEAR, **params
    ) -> np.ndarray:
        return F.smallest_max_size(img, max_size=max_size, interpolation=interpolation)

    def apply_to_bbox(self, bbox: BoxInternalType, **params) -> BoxInternalType:
        return bbox

    def apply_to_keypoint(self, keypoint: KeypointInternalType, max_size: int = 1024, **params) -> KeypointInternalType:
        height = params["rows"]
        width = params["cols"]
        depth = params["slices"]

        scale = max_size / min([height, width, depth])
        return F.keypoint_scale(keypoint, scale, scale, scale)
    
    def apply_to_dicom(self, dicom: DicomType, max_size: int = 1024, **params) -> DicomType:
        height = params["rows"]
        width = params["cols"]
        depth = params["slices"]
        scale = max_size / min([height, width, depth])
        return Fdicom.dicom_scale(dicom, scale, scale, scale)

    def get_params(self) -> Dict[str, int]:
        return {"max_size": self.max_size if isinstance(self.max_size, int) else random.choice(self.max_size)}

    def get_transform_init_args_names(self) -> Tuple[str, ...]:
        return ("max_size", "interpolation")


class Resize(DualTransform):
    """Resize the input to the given height, width, depth.

    Args:
        height (int): desired height of the output.
        width (int): desired width of the output.
        depth (int): desired depth of the output.
        interpolation (int): scipy interpolation method (e.g. albumenations3d.INTER_NEAREST). Default: albumentations3d.INTER_LINEAR
        p (float): probability of applying the transform. Default: 1.

    Targets:
        image, mask, bboxes, keypoints

    Image types:
        uint8, float32
    """

    def __init__(self, height, width, depth, interpolation=INTER_LINEAR, always_apply=False, p=1):
        super(Resize, self).__init__(always_apply, p)
        self.height = height
        self.width = width
        self.depth = depth
        self.interpolation = interpolation

    def apply(self, img, interpolation=INTER_LINEAR, **params):
        return F.resize(img, height=self.height, width=self.width, depth=self.depth, interpolation=interpolation)

    def apply_to_bbox(self, bbox, **params):
        # Bounding box coordinates are scale invariant
        return bbox
    
    def apply_to_dicom(self, dicom: DicomType, **params) -> DicomType:
        height = params["rows"]
        width = params["cols"]
        depth = params["slices"]
        scale_x = self.width / width
        scale_y = self.height / height
        scale_z = self.depth / depth
        return Fdicom.dicom_scale(dicom, scale_x, scale_y, scale_z)


    def apply_to_keypoint(self, keypoint, **params):
        height = params["rows"]
        width = params["cols"]
        depth = params["slices"]
        scale_x = self.width / width
        scale_y = self.height / height
        scale_z = self.depth / depth
        return F.keypoint_scale(keypoint, scale_x, scale_y, scale_z)

    def get_transform_init_args_names(self):
        return ("height", "width", "depth", "interpolation")
