import random
from typing import Iterable, Optional, Tuple, Dict, Any, List

import numpy as np

from ...core.transforms_interface import DualTransform
from . import functional as F

__all__ = ["GridDropout"]


class GridDropout(DualTransform):
    """GridDropout, drops out rectangular regions of an image and the corresponding mask in a grid fashion.

    Args:
        ratio (float): the ratio of the mask holes to the unit_size (same for all spatial dimensions).
            Must be between 0 and 1. Default: 0.5.
        unit_size_min (int): minimum size of the grid unit. Must be between 2 and the image shorter edge.
            If 'None', holes_number_x and holes_number_y are used to setup the grid. Default: `None`.
        unit_size_max (int): maximum size of the grid unit. Must be between 2 and the image shorter edge.
            If 'None', holes_number_x and holes_number_y are used to setup the grid. Default: `None`.
        holes_number_x (int): the number of grid units in x direction. Must be between 1 and image width//2.
            If 'None', grid unit width is set as image_width//10. Default: `None`.
        holes_number_y (int): the number of grid units in y direction. Must be between 1 and image height//2.
            If `None`, grid unit height is set equal to the grid unit width or image height, whatever is smaller.
        holes_number_z (int): the number of grid units in z direction. Must be between 1 and image depth//2.
            If `None`, grid unit depth is set equal to the grid unit width, height, whatever is smaller.
        shift_x (int): offsets of the grid start in x direction from (0,0) coordinate.
            Clipped between 0 and grid unit_width - hole_width. Default: 0.
        shift_y (int): offsets of the grid start in y direction from (0,0) coordinate.
            Clipped between 0 and grid unit height - hole_height. Default: 0.
        shift_z (int): offsets of the grid start in z direction from (0,0) coordinate.
            Clipped between 0 and grid unit depth - hole_height. Default: 0.
        random_offset (boolean): weather to offset the grid randomly between 0 and grid unit size - hole size
            If 'True', then shift_x, shift_y, shift_z are ignored and set randomly. Default: `False`.
        fill_value (int): value for the dropped pixels. Default = 0
        mask_fill_value (int): value for the dropped pixels in mask.
            If `None`, transformation is not applied to the mask. Default: `None`.
        always_apply (bool): whether to always apply the transformation. Default: False
        p (float): probability of applying the transform. Default: 0.5.

    Targets:
        image, mask

    Image types:
        uint8, float32

    References:
        https://arxiv.org/abs/2001.04086

    """

    def __init__(
        self,
        ratio: float = 0.5,
        unit_size_min: Optional[int] = None,
        unit_size_max: Optional[int] = None,
        holes_number_x: Optional[int] = None,
        holes_number_y: Optional[int] = None,
        holes_number_z: Optional[int] = None,
        shift_x: int = 0,
        shift_y: int = 0,
        shift_z: int = 0,
        random_offset: bool = False,
        fill_value: int = 0,
        mask_fill_value: Optional[int] = None,
        always_apply: bool = False,
        p: float = 0.5,
    ):
        super(GridDropout, self).__init__(always_apply, p)
        self.ratio = ratio
        self.unit_size_min = unit_size_min
        self.unit_size_max = unit_size_max
        self.holes_number_x = holes_number_x
        self.holes_number_y = holes_number_y
        self.holes_number_z = holes_number_z
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.shift_z = shift_z
        self.random_offset = random_offset
        self.fill_value = fill_value
        self.mask_fill_value = mask_fill_value
        if not 0 < self.ratio <= 1:
            raise ValueError("ratio must be between 0 and 1.")

    def apply(
        self,
        img: np.ndarray,
        holes: Iterable[Tuple[int, int, int, int, int, int]] = (),
        **params
    ) -> np.ndarray:
        """Applies the transformation to the image"""
        return F.cutout(img, holes, self.fill_value)

    def apply_to_mask(
        self,
        img: np.ndarray,
        holes: Iterable[Tuple[int, int, int, int, int, int]] = (),
        **params
    ) -> np.ndarray:
        """Applies the transformation to a mask and"""
        if self.mask_fill_value is None:
            return img

        return F.cutout(img, holes, self.mask_fill_value)

    def get_params_dependent_on_targets(self, params) -> Dict[str, Any]:
        """Returns additional parameters needed for the `apply` methods that depend on a target
        (e.g. `apply_to_bboxes` method expects image size)
        """
        img = params["image"]
        height, width, depth = img.shape[:3]
        # set grid using unit size limits
        if self.unit_size_min and self.unit_size_max:
            if not 2 <= self.unit_size_min <= self.unit_size_max:
                raise ValueError(
                    "Max unit size should be >= min size, both at least 2 pixels."
                )
            if self.unit_size_max > min(height, width):
                raise ValueError(
                    "Grid size limits must be within the shortest image edge."
                )
            unit_width = random.randint(self.unit_size_min, self.unit_size_max + 1)
            unit_height = unit_depth = unit_width
        else:
            # set grid using holes numbers
            if self.holes_number_x is None:
                unit_width = max(2, width // 10)
            else:
                if not 1 <= self.holes_number_x <= width // 2:
                    raise ValueError(
                        "The hole_number_x must be between 1 and image width//2."
                    )
                unit_width = width // self.holes_number_x
            if self.holes_number_y is None:
                unit_height = max(min(unit_width, height), 2)
            else:
                if not 1 <= self.holes_number_y <= height // 2:
                    raise ValueError(
                        "The hole_number_y must be between 1 and image height//2."
                    )
                unit_height = height // self.holes_number_y
            if self.holes_number_z is None:
                unit_depth = max(min(unit_width, depth), 2)
            else:
                if not 1 <= self.holes_number_z <= depth // 2:
                    raise ValueError(
                        "The hole_number_z must be between 1 and image depth//2."
                    )
                unit_depth = depth // self.holes_number_z

        hole_width = int(unit_width * self.ratio)
        hole_height = int(unit_height * self.ratio)
        hole_depth = int(unit_depth * self.ratio)
        # min 1 pixel and max unit length - 1
        hole_width = min(max(hole_width, 1), unit_width - 1)
        hole_height = min(max(hole_height, 1), unit_height - 1)
        hole_depth = min(max(hole_depth, 1), unit_depth - 1)
        # set offset of the grid
        if self.shift_x is None:
            shift_x = 0
        else:
            shift_x = min(max(0, self.shift_x), unit_width - hole_width)
        if self.shift_y is None:
            shift_y = 0
        else:
            shift_y = min(max(0, self.shift_y), unit_height - hole_height)
        if self.shift_z is None:
            shift_z = 0
        else:
            shift_z = min(max(0, self.shift_z), unit_depth - hole_depth)
        if self.random_offset:
            shift_x = random.randint(0, unit_width - hole_width)
            shift_y = random.randint(0, unit_height - hole_height)
            shift_z = random.randint(0, unit_depth - hole_depth)
        holes = []
        for i in range(width // unit_width + 1):
            for j in range(height // unit_height + 1):
                for k in range(depth // unit_depth + 1):
                    x1 = min(shift_x + unit_width * i, width)
                    y1 = min(shift_y + unit_height * j, height)
                    z1 = min(shift_z + unit_depth * k, depth)
                    x2 = min(x1 + hole_width, width)
                    y2 = min(y1 + hole_height, height)
                    z2 = min(z1 + hole_depth, depth)
                    holes.append((x1, y1, z1, x2, y2, z2))

        return {"holes": holes}

    @property
    def targets_as_params(self) -> List[str]:
        return ["image"]

    def get_transform_init_args_names(self) -> Tuple[str, ...]:
        """Returns initialization argument names. (e.g. Transform(arg1 = 1, arg2 = 2) -> ('arg1', 'arg2'))"""
        return (
            "ratio",
            "unit_size_min",
            "unit_size_max",
            "holes_number_x",
            "holes_number_y",
            "holes_number_z",
            "shift_x",
            "shift_y",
            "shift_z",
            "random_offset",
            "fill_value",
            "mask_fill_value",
        )
