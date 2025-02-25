from __future__ import absolute_import

import cv2
import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal_nulp

import dicaugment as A
import dicaugment.augmentations.functional as F
import dicaugment.augmentations.geometric.functional as FGeometric
from dicaugment.augmentations.utils import (
    is_multispectral_image,
)
from dicaugment.core.bbox_utils import filter_bboxes
from tests.utils import convert_3d_to_target_format


@pytest.mark.parametrize("target", ["image", "mask"])
def test_vflip(target):
    img = np.array(
        [[[1, 0], [1, 0], [1, 0]], [[0, 1], [1, 0], [1, 0]], [[0, 1], [0, 1], [1, 0]]],
        dtype=np.uint8,
    )
    expected = np.array(
        [[[0, 1], [0, 1], [1, 0]], [[0, 1], [1, 0], [1, 0]], [[1, 0], [1, 0], [1, 0]]],
        dtype=np.uint8,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    flipped_img = FGeometric.vflip(img)
    assert np.array_equal(flipped_img, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_vflip_float(target):
    img = np.array(
        [
            [[0.4, 0], [0.4, 0], [0.4, 0]],
            [[0.0, 0.4], [0.4, 0], [0.4, 0]],
            [[0.0, 0.4], [0.0, 0.4], [0.4, 0]],
        ],
        dtype=np.float32,
    )
    expected = np.array(
        [
            [[0.0, 0.4], [0.0, 0.4], [0.4, 0]],
            [[0.0, 0.4], [0.4, 0], [0.4, 0]],
            [[0.4, 0], [0.4, 0], [0.4, 0]],
        ],
        dtype=np.float32,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    flipped_img = FGeometric.vflip(img)
    assert_array_almost_equal_nulp(flipped_img, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_hflip(target):
    img = np.array(
        [[[1, 0], [1, 0], [1, 0]], [[0, 1], [1, 0], [1, 0]], [[0, 1], [0, 1], [1, 0]]],
        dtype=np.uint8,
    )
    expected = np.array(
        [[[1, 0], [1, 0], [1, 0]], [[1, 0], [1, 0], [0, 1]], [[1, 0], [0, 1], [0, 1]]],
        dtype=np.uint8,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    flipped_img = FGeometric.hflip(img)
    assert np.array_equal(flipped_img, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_hflip_float(target):
    img = np.array(
        [
            [[0.4, 0], [0.4, 0], [0.4, 0]],
            [[0.0, 0.4], [0.4, 0], [0.4, 0]],
            [[0.0, 0.4], [0.0, 0.4], [0.4, 0]],
        ],
        dtype=np.float32,
    )
    expected = np.array(
        [
            [[0.4, 0], [0.4, 0], [0.4, 0]],
            [[0.4, 0], [0.4, 0], [0.0, 0.4]],
            [[0.4, 0], [0.0, 0.4], [0.0, 0.4]],
        ],
        dtype=np.float32,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    flipped_img = FGeometric.hflip(img)
    assert_array_almost_equal_nulp(flipped_img, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_zflip(target):
    img = np.array(
        [[[1, 0], [1, 0], [1, 0]], [[0, 1], [1, 0], [1, 0]], [[0, 1], [0, 1], [1, 0]]],
        dtype=np.uint8,
    )
    expected = np.array(
        [[[0, 1], [0, 1], [0, 1]], [[1, 0], [0, 1], [0, 1]], [[1, 0], [1, 0], [0, 1]]],
        dtype=np.uint8,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    flipped_img = FGeometric.zflip(img)
    assert np.array_equal(flipped_img, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_zflip_float(target):
    img = np.array(
        [
            [[0.4, 0], [0.4, 0], [0.4, 0]],
            [[0.0, 0.4], [0.4, 0], [0.4, 0]],
            [[0.0, 0.4], [0.0, 0.4], [0.4, 0]],
        ],
        dtype=np.float32,
    )
    expected = np.array(
        [
            [[0, 0.4], [0, 0.4], [0, 0.4]],
            [[0.4, 0.0], [0, 0.4], [0, 0.4]],
            [[0.4, 0.0], [0.4, 0.0], [0, 0.4]],
        ],
        dtype=np.float32,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    flipped_img = FGeometric.zflip(img)
    assert_array_almost_equal_nulp(flipped_img, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
@pytest.mark.parametrize(
    ["code", "func"],
    [
        [0, FGeometric.vflip],
        [1, FGeometric.hflip],
        [2, FGeometric.zflip],
        [-1, lambda img: FGeometric.zflip(FGeometric.vflip(FGeometric.hflip(img)))],
    ],
)
def test_random_flip(code, func, target):
    img = np.array(
        [[[1, 0], [1, 0], [1, 0]], [[0, 1], [1, 0], [1, 0]], [[0, 1], [0, 1], [1, 0]]],
        dtype=np.uint8,
    )
    img = convert_3d_to_target_format([img], target=target)
    assert np.array_equal(FGeometric.random_flip(img, code), func(img))


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
@pytest.mark.parametrize(
    ["code", "func"],
    [
        [0, FGeometric.vflip],
        [1, FGeometric.hflip],
        [2, FGeometric.zflip],
        [-1, lambda img: FGeometric.zflip(FGeometric.vflip(FGeometric.hflip(img)))],
    ],
)
def test_random_flip_float(code, func, target):
    img = np.array(
        [
            [[0.4, 0], [0.4, 0], [0.4, 0]],
            [[0.0, 0.4], [0.4, 0], [0.4, 0]],
            [[0.0, 0.4], [0.0, 0.4], [0.4, 0]],
        ],
        dtype=np.float32,
    )
    img = convert_3d_to_target_format([img], target=target)
    assert_array_almost_equal_nulp(FGeometric.random_flip(img, code), func(img))


@pytest.mark.parametrize(
    ["input_shape", "expected_shape"],
    [[(128, 64, 100), (64, 128, 100)], [(128, 64, 100, 3), (64, 128, 100, 3)]],
)
def test_transpose(input_shape, expected_shape):
    img = np.random.randint(low=0, high=256, size=input_shape, dtype=np.uint8)
    transposed = FGeometric.transpose(img)
    assert transposed.shape == expected_shape


@pytest.mark.parametrize(
    ["input_shape", "expected_shape"],
    [[(128, 64, 100), (64, 128, 100)], [(128, 64, 100, 3), (64, 128, 100, 3)]],
)
def test_transpose_float(input_shape, expected_shape):
    img = np.random.uniform(low=0.0, high=1.0, size=input_shape).astype("float32")
    transposed = FGeometric.transpose(img)
    assert transposed.shape == expected_shape


@pytest.mark.parametrize("target", ["image", "mask"])
def test_rot90(target):
    img = np.array(
        [[[0, 1], [0, 1], [1, 0]], [[0, 1], [0, 1], [1, 0]], [[0, 1], [0, 1], [1, 0]]],
        dtype=np.uint8,
    )
    expected = np.array(
        [[[1, 0], [1, 0], [1, 0]], [[0, 1], [0, 1], [0, 1]], [[0, 1], [0, 1], [0, 1]]],
        dtype=np.uint8,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    rotated = FGeometric.rot90(img, factor=1)
    assert np.array_equal(rotated, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_rot90_float(target):
    img = np.array(
        [
            [[0.0, 0.4], [0.0, 0.4], [0.4, 0]],
            [[0.0, 0.4], [0.0, 0.4], [0.4, 0]],
            [[0.0, 0.4], [0.0, 0.4], [0.4, 0]],
        ],
        dtype=np.float32,
    )
    expected = np.array(
        [
            [[0.4, 0], [0.4, 0], [0.4, 0]],
            [[0.0, 0.4], [0.0, 0.4], [0.0, 0.4]],
            [[0.0, 0.4], [0.0, 0.4], [0.0, 0.4]],
        ],
        dtype=np.float32,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    rotated = FGeometric.rot90(img, factor=1)
    assert_array_almost_equal_nulp(rotated, expected)


def test_normalize():
    img = np.ones((100, 100, 100), dtype=np.uint8) * 127
    normalized = F.normalize(img, mean=50, std=3)
    expected = (np.ones((100, 100, 100), dtype=np.float32) * (127 - 50)) / 3
    assert_array_almost_equal_nulp(normalized, expected)


def test_normalize_float():
    img = np.ones((100, 100, 100), dtype=np.float32) * 0.4
    normalized = F.normalize(img, mean=50, std=3)
    expected = ((np.ones((100, 100, 100), dtype=np.float32) * 0.4) - 50) / 3
    assert_array_almost_equal_nulp(normalized, expected)


def test_compare_rotate_and_shift_scale_rotate(image):
    rotated_img_1 = FGeometric.rotate(image, angle=60, axes="xy")
    rotated_img_2 = FGeometric.shift_scale_rotate(
        image, angle=60, scale=1, dx=0, dy=0, dz=0, axes="xy"
    )
    assert np.array_equal(rotated_img_1, rotated_img_2)


def test_compare_rotate_float_and_shift_scale_rotate_float(float_image):
    rotated_img_1 = FGeometric.rotate(float_image, angle=60, axes="xy")
    rotated_img_2 = FGeometric.shift_scale_rotate(
        float_image, angle=60, scale=1, dx=0, dy=0, dz=0, axes="xy"
    )
    assert np.array_equal(rotated_img_1, rotated_img_2)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_center_crop(target):
    img = np.array(
        [
            [[1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1]],
            [[1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1]],
            [[1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1]],
            [[1, 1, 1, 1], [0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1]],
        ],
        dtype=np.uint8,
    )
    expected = np.array([[[1, 1], [0, 1]], [[1, 1], [0, 1]]], dtype=np.uint8)
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    cropped_img = A.center_crop(img, 2, 2, 2)
    assert np.array_equal(cropped_img, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_center_crop_float(target):
    img = np.array(
        [
            [
                [0.4, 0.4, 0.4, 0.4],
                [0.0, 0.4, 0.4, 0.4],
                [0.0, 0.0, 0.4, 0.4],
                [0.0, 0.0, 0.0, 0.4],
            ],
            [
                [0.4, 0.4, 0.4, 0.4],
                [0.0, 0.4, 0.4, 0.4],
                [0.0, 0.0, 0.4, 0.4],
                [0.0, 0.0, 0.0, 0.4],
            ],
            [
                [0.4, 0.4, 0.4, 0.4],
                [0.0, 0.4, 0.4, 0.4],
                [0.0, 0.0, 0.4, 0.4],
                [0.0, 0.0, 0.0, 0.4],
            ],
            [
                [0.4, 0.4, 0.4, 0.4],
                [0.0, 0.4, 0.4, 0.4],
                [0.0, 0.0, 0.4, 0.4],
                [0.0, 0.0, 0.0, 0.4],
            ],
        ],
        dtype=np.float32,
    )
    expected = np.array(
        [[[0.4, 0.4], [0.0, 0.4]], [[0.4, 0.4], [0.0, 0.4]]], dtype=np.float32
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    cropped_img = A.center_crop(img, 2, 2, 2)
    assert_array_almost_equal_nulp(cropped_img, expected)


def test_center_crop_with_incorrectly_large_crop_size():
    img = np.ones((4, 4, 4), dtype=np.uint8)
    with pytest.raises(ValueError) as exc_info:
        A.center_crop(img, 8, 8, 8)
    assert (
        str(exc_info.value)
        == "Requested crop size (8, 8, 8) is larger than the image size (4, 4, 4)"
    )


@pytest.mark.parametrize("target", ["image", "mask"])
def test_random_crop(target):
    img = np.array(
        [
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
            [[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]],
            [[33, 34, 35, 36], [37, 38, 39, 40], [41, 42, 43, 44], [45, 46, 47, 48]],
            [[49, 50, 51, 52], [53, 54, 55, 56], [57, 58, 59, 60], [61, 62, 63, 64]],
        ],
        dtype=np.uint8,
    )
    expected = np.array([[[18, 19], [22, 23]], [[34, 35], [38, 39]]], dtype=np.uint8)
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    cropped_img = A.random_crop(
        img,
        crop_height=2,
        crop_width=2,
        crop_depth=2,
        h_start=0.5,
        w_start=0,
        d_start=0.5,
    )
    assert np.array_equal(cropped_img, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_random_crop_float(target):
    img = np.array(
        [
            [
                [0.01, 0.02, 0.03, 0.04],
                [0.05, 0.06, 0.07, 0.08],
                [0.09, 0.1, 0.11, 0.12],
                [0.13, 0.14, 0.15, 0.16],
            ],
            [
                [0.17, 0.18, 0.19, 0.2],
                [0.21, 0.22, 0.23, 0.24],
                [0.25, 0.26, 0.27, 0.28],
                [0.29, 0.3, 0.31, 0.32],
            ],
            [
                [0.33, 0.34, 0.35, 0.36],
                [0.37, 0.38, 0.39, 0.4],
                [0.41, 0.42, 0.43, 0.44],
                [0.45, 0.46, 0.47, 0.48],
            ],
            [
                [0.49, 0.5, 0.51, 0.52],
                [0.53, 0.54, 0.55, 0.56],
                [0.57, 0.58, 0.59, 0.6],
                [0.61, 0.62, 0.63, 0.64],
            ],
        ],
        dtype=np.float32,
    )
    expected = np.array(
        [[[0.17, 0.18], [0.21, 0.22]], [[0.33, 0.34], [0.37, 0.38]]], dtype=np.float32
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    cropped_img = A.random_crop(
        img,
        crop_height=2,
        crop_width=2,
        crop_depth=2,
        h_start=0.5,
        w_start=0,
        d_start=0.0,
    )
    assert_array_almost_equal_nulp(cropped_img, expected)


def test_random_crop_with_incorrectly_large_crop_size():
    img = np.ones((4, 4, 4), dtype=np.uint8)
    with pytest.raises(ValueError) as exc_info:
        A.random_crop(
            img,
            crop_height=8,
            crop_width=8,
            crop_depth=8,
            h_start=0,
            w_start=0,
            d_start=0,
        )
    assert (
        str(exc_info.value)
        == "Requested crop size (8, 8, 8) is larger than the image size (4, 4, 4)"
    )


def test_random_crop_extrema():
    img = np.indices((4, 4, 4), dtype=np.uint8).transpose([1, 2, 3, 0])
    expected1 = np.indices((2, 2, 2), dtype=np.uint8).transpose([1, 2, 3, 0])
    expected2 = expected1 + 2
    cropped_img1 = A.random_crop(
        img,
        crop_height=2,
        crop_width=2,
        crop_depth=2,
        h_start=0.0,
        w_start=0.0,
        d_start=0.0,
    )
    cropped_img2 = A.random_crop(
        img,
        crop_height=2,
        crop_width=2,
        crop_depth=2,
        h_start=0.9999,
        w_start=0.9999,
        d_start=0.9999,
    )
    assert np.array_equal(cropped_img1, expected1)
    assert np.array_equal(cropped_img2, expected2)


def test_clip():
    img = np.array([[[-300, -20], [0, 0]], [[100, -25], [400, 20]]], dtype=np.float32)
    expected = np.array([[[0, 0], [0, 0]], [[100, 0], [255, 20]]], dtype=np.float32)
    clipped = F.clip(img, dtype=np.uint8, minval=0, maxval=255)
    assert np.array_equal(clipped, expected)


def test_clip_float():
    img = np.array(
        [[[-0.02, 10.0], [0, 0]], [[0.5, 0.002], [2.2, -0.75]]], dtype=np.float32
    )
    expected = np.array(
        [[[0, 1.0], [0, 0]], [[0.5, 0.002], [1.0, 0]]], dtype=np.float32
    )
    clipped = F.clip(img, dtype=np.float32, minval=0, maxval=1.0)
    assert_array_almost_equal_nulp(clipped, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_pad(target):
    img = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], dtype=np.uint8)
    expected = np.array(
        [
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 1, 2, 0], [0, 3, 4, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 5, 6, 0], [0, 7, 8, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        ],
        dtype=np.uint8,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    padded = FGeometric.pad(img, min_height=4, min_width=4, min_depth=4)
    assert np.array_equal(padded, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_pad_float(target):
    img = np.array(
        [[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]], dtype=np.float32
    )
    expected = np.array(
        [
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0.1, 0.2, 0], [0, 0.3, 0.4, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0.5, 0.6, 0], [0, 0.7, 0.8, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        ],
        dtype=np.float32,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    padded_img = FGeometric.pad(img, min_height=4, min_width=4, min_depth=4)
    assert_array_almost_equal_nulp(padded_img, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_rotate_from_shift_scale_rotate(target):
    img = np.array(
        [[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]], [[13, 14], [15, 16]]],
        dtype=np.uint8,
    )
    expected = np.array(
        [[[0, 0], [0, 0]], [[7, 8], [11, 12]], [[5, 6], [9, 10]], [[0, 0], [0, 0]]],
        dtype=np.uint8,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    rotated_img = FGeometric.shift_scale_rotate(
        img,
        angle=90,
        scale=1,
        dx=0,
        dy=0,
        dz=0,
        axes="xy",
        interpolation=0,
        border_mode="constant",
    )
    assert np.array_equal(rotated_img, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_rotate_float_from_shift_scale_rotate(target):
    img = np.array(
        [
            [[0.01, 0.02], [0.03, 0.04]],
            [[0.05, 0.06], [0.07, 0.08]],
            [[0.09, 0.10], [0.11, 0.12]],
            [[0.13, 0.14], [0.15, 0.16]],
        ],
        dtype=np.float32,
    )
    expected = np.array(
        [
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.07, 0.08], [0.11, 0.12]],
            [[0.05, 0.06], [0.09, 0.10]],
            [[0.0, 0.0], [0.0, 0.0]],
        ],
        dtype=np.float32,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    rotated_img = FGeometric.shift_scale_rotate(
        img,
        angle=90,
        scale=1,
        dx=0,
        dy=0,
        dz=0,
        axes="xy",
        interpolation=0,
        border_mode="constant",
    )
    assert_array_almost_equal_nulp(rotated_img, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_scale_from_shift_scale_rotate(target):
    img = np.array(
        [
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
            [[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]],
            [[33, 34, 35, 36], [37, 38, 39, 40], [41, 42, 43, 44], [45, 46, 47, 48]],
            [[49, 50, 51, 52], [53, 54, 55, 56], [57, 58, 59, 60], [61, 62, 63, 64]],
        ],
        dtype=np.uint8,
    )
    expected = np.array(
        [
            [[22, 22, 23, 23], [22, 22, 23, 23], [26, 26, 27, 27], [26, 26, 27, 27]],
            [[22, 22, 23, 23], [22, 22, 23, 23], [26, 26, 27, 27], [26, 26, 27, 27]],
            [[38, 38, 39, 39], [38, 38, 39, 39], [42, 42, 43, 43], [42, 42, 43, 43]],
            [[38, 38, 39, 39], [38, 38, 39, 39], [42, 42, 43, 43], [42, 42, 43, 43]],
        ],
        dtype=np.uint8,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    scaled_img = FGeometric.shift_scale_rotate(
        img,
        angle=0,
        scale=2,
        dx=0,
        dy=0,
        dz=0,
        axes="xy",
        interpolation=0,
        border_mode="constant",
    )
    assert np.array_equal(scaled_img, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_scale_float_from_shift_scale_rotate(target):
    img = np.array(
        [
            [
                [0.01, 0.02, 0.03, 0.04],
                [0.05, 0.06, 0.07, 0.08],
                [0.09, 0.010, 0.011, 0.012],
                [0.013, 0.014, 0.015, 0.016],
            ],
            [
                [0.017, 0.018, 0.019, 0.020],
                [0.021, 0.022, 0.023, 0.024],
                [0.025, 0.026, 0.027, 0.028],
                [0.029, 0.030, 0.031, 0.032],
            ],
            [
                [0.033, 0.034, 0.035, 0.036],
                [0.037, 0.038, 0.039, 0.040],
                [0.041, 0.042, 0.043, 0.044],
                [0.045, 0.046, 0.047, 0.048],
            ],
            [
                [0.049, 0.050, 0.051, 0.052],
                [0.053, 0.054, 0.055, 0.056],
                [0.057, 0.058, 0.059, 0.060],
                [0.061, 0.062, 0.063, 0.064],
            ],
        ],
        dtype=np.float32,
    )
    expected = np.array(
        [
            [
                [0.022, 0.022, 0.023, 0.023],
                [0.022, 0.022, 0.023, 0.023],
                [0.026, 0.026, 0.027, 0.027],
                [0.026, 0.026, 0.027, 0.027],
            ],
            [
                [0.022, 0.022, 0.023, 0.023],
                [0.022, 0.022, 0.023, 0.023],
                [0.026, 0.026, 0.027, 0.027],
                [0.026, 0.026, 0.027, 0.027],
            ],
            [
                [0.038, 0.038, 0.039, 0.039],
                [0.038, 0.038, 0.039, 0.039],
                [0.042, 0.042, 0.043, 0.043],
                [0.042, 0.042, 0.043, 0.043],
            ],
            [
                [0.038, 0.038, 0.039, 0.039],
                [0.038, 0.038, 0.039, 0.039],
                [0.042, 0.042, 0.043, 0.043],
                [0.042, 0.042, 0.043, 0.043],
            ],
        ],
        dtype=np.float32,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    scaled_img = FGeometric.shift_scale_rotate(
        img,
        angle=0,
        scale=2,
        dx=0,
        dy=0,
        dz=0,
        axes="xy",
        interpolation=0,
        border_mode="constant",
    )
    assert_array_almost_equal_nulp(scaled_img, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_shift_x_from_shift_scale_rotate(target):
    img = np.array(
        [
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
            [[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]],
            [[33, 34, 35, 36], [37, 38, 39, 40], [41, 42, 43, 44], [45, 46, 47, 48]],
            [[49, 50, 51, 52], [53, 54, 55, 56], [57, 58, 59, 60], [61, 62, 63, 64]],
        ],
        dtype=np.uint8,
    )
    expected = np.array(
        [
            [[0, 0, 0, 0], [0, 0, 0, 0], [1, 2, 3, 4], [5, 6, 7, 8]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [17, 18, 19, 20], [21, 22, 23, 24]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [33, 34, 35, 36], [37, 38, 39, 40]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [49, 50, 51, 52], [53, 54, 55, 56]],
        ],
        dtype=np.uint8,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    shifted_along_x_img = FGeometric.shift_scale_rotate(
        img,
        angle=0,
        scale=1,
        dx=0.5,
        dy=0,
        dz=0,
        axes="xy",
        interpolation=0,
        border_mode="constant",
    )
    assert np.array_equal(shifted_along_x_img, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_shift_x_float_from_shift_scale_rotate(target):
    img = np.array(
        [
            [
                [0.01, 0.02, 0.03, 0.04],
                [0.05, 0.06, 0.07, 0.08],
                [0.09, 0.010, 0.011, 0.012],
                [0.013, 0.014, 0.015, 0.016],
            ],
            [
                [0.017, 0.018, 0.019, 0.020],
                [0.021, 0.022, 0.023, 0.024],
                [0.025, 0.026, 0.027, 0.028],
                [0.029, 0.030, 0.031, 0.032],
            ],
            [
                [0.033, 0.034, 0.035, 0.036],
                [0.037, 0.038, 0.039, 0.040],
                [0.041, 0.042, 0.043, 0.044],
                [0.045, 0.046, 0.047, 0.048],
            ],
            [
                [0.049, 0.050, 0.051, 0.052],
                [0.053, 0.054, 0.055, 0.056],
                [0.057, 0.058, 0.059, 0.060],
                [0.061, 0.062, 0.063, 0.064],
            ],
        ],
        dtype=np.float32,
    )
    expected = np.array(
        [
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0.01, 0.02, 0.03, 0.04],
                [0.05, 0.06, 0.07, 0.08],
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0.017, 0.018, 0.019, 0.020],
                [0.021, 0.022, 0.023, 0.024],
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0.033, 0.034, 0.035, 0.036],
                [0.037, 0.038, 0.039, 0.040],
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0.049, 0.050, 0.051, 0.052],
                [0.053, 0.054, 0.055, 0.056],
            ],
        ],
        dtype=np.float32,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    shifted_along_x_img = FGeometric.shift_scale_rotate(
        img,
        angle=0,
        scale=1,
        dx=0.5,
        dy=0,
        dz=0,
        axes="xy",
        interpolation=0,
        border_mode="constant",
    )
    assert_array_almost_equal_nulp(shifted_along_x_img, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_shift_y_from_shift_scale_rotate(target):
    img = np.array(
        [
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
            [[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]],
            [[33, 34, 35, 36], [37, 38, 39, 40], [41, 42, 43, 44], [45, 46, 47, 48]],
            [[49, 50, 51, 52], [53, 54, 55, 56], [57, 58, 59, 60], [61, 62, 63, 64]],
        ],
        dtype=np.uint8,
    )
    expected = np.array(
        [
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
            [[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]],
        ],
        dtype=np.uint8,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    shifted_along_y_img = FGeometric.shift_scale_rotate(
        img,
        angle=0,
        scale=1,
        dx=0,
        dy=0.5,
        dz=0,
        axes="xy",
        interpolation=0,
        border_mode="constant",
    )
    assert np.array_equal(shifted_along_y_img, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_shift_y_float_from_shift_scale_rotate(target):
    img = np.array(
        [
            [
                [0.01, 0.02, 0.03, 0.04],
                [0.05, 0.06, 0.07, 0.08],
                [0.09, 0.010, 0.011, 0.012],
                [0.013, 0.014, 0.015, 0.016],
            ],
            [
                [0.017, 0.018, 0.019, 0.020],
                [0.021, 0.022, 0.023, 0.024],
                [0.025, 0.026, 0.027, 0.028],
                [0.029, 0.030, 0.031, 0.032],
            ],
            [
                [0.033, 0.034, 0.035, 0.036],
                [0.037, 0.038, 0.039, 0.040],
                [0.041, 0.042, 0.043, 0.044],
                [0.045, 0.046, 0.047, 0.048],
            ],
            [
                [0.049, 0.050, 0.051, 0.052],
                [0.053, 0.054, 0.055, 0.056],
                [0.057, 0.058, 0.059, 0.060],
                [0.061, 0.062, 0.063, 0.064],
            ],
        ],
        dtype=np.float32,
    )
    expected = np.array(
        [
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [
                [0.01, 0.02, 0.03, 0.04],
                [0.05, 0.06, 0.07, 0.08],
                [0.09, 0.010, 0.011, 0.012],
                [0.013, 0.014, 0.015, 0.016],
            ],
            [
                [0.017, 0.018, 0.019, 0.020],
                [0.021, 0.022, 0.023, 0.024],
                [0.025, 0.026, 0.027, 0.028],
                [0.029, 0.030, 0.031, 0.032],
            ],
        ],
        dtype=np.float32,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    shifted_along_y_img = FGeometric.shift_scale_rotate(
        img,
        angle=0,
        scale=1,
        dx=0,
        dy=0.5,
        dz=0,
        axes="xy",
        interpolation=0,
        border_mode="constant",
    )
    assert_array_almost_equal_nulp(shifted_along_y_img, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_shift_z_from_shift_scale_rotate(target):
    img = np.array(
        [
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
            [[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]],
            [[33, 34, 35, 36], [37, 38, 39, 40], [41, 42, 43, 44], [45, 46, 47, 48]],
            [[49, 50, 51, 52], [53, 54, 55, 56], [57, 58, 59, 60], [61, 62, 63, 64]],
        ],
        dtype=np.uint8,
    )
    expected = np.array(
        [
            [[0, 0, 1, 2], [0, 0, 5, 6], [0, 0, 9, 10], [0, 0, 13, 14]],
            [[0, 0, 17, 18], [0, 0, 21, 22], [0, 0, 25, 26], [0, 0, 29, 30]],
            [[0, 0, 33, 34], [0, 0, 37, 38], [0, 0, 41, 42], [0, 0, 45, 46]],
            [[0, 0, 49, 50], [0, 0, 53, 54], [0, 0, 57, 58], [0, 0, 61, 62]],
        ],
        dtype=np.uint8,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    shifted_along_y_img = FGeometric.shift_scale_rotate(
        img,
        angle=0,
        scale=1,
        dx=0,
        dy=0,
        dz=0.5,
        axes="xy",
        interpolation=0,
        border_mode="constant",
    )
    assert np.array_equal(shifted_along_y_img, expected)


@pytest.mark.parametrize("target", ["image", "image_4_channels"])
def test_shift_z_float_from_shift_scale_rotate(target):
    img = np.array(
        [
            [
                [0.01, 0.02, 0.03, 0.04],
                [0.05, 0.06, 0.07, 0.08],
                [0.09, 0.010, 0.011, 0.012],
                [0.013, 0.014, 0.015, 0.016],
            ],
            [
                [0.017, 0.018, 0.019, 0.020],
                [0.021, 0.022, 0.023, 0.024],
                [0.025, 0.026, 0.027, 0.028],
                [0.029, 0.030, 0.031, 0.032],
            ],
            [
                [0.033, 0.034, 0.035, 0.036],
                [0.037, 0.038, 0.039, 0.040],
                [0.041, 0.042, 0.043, 0.044],
                [0.045, 0.046, 0.047, 0.048],
            ],
            [
                [0.049, 0.050, 0.051, 0.052],
                [0.053, 0.054, 0.055, 0.056],
                [0.057, 0.058, 0.059, 0.060],
                [0.061, 0.062, 0.063, 0.064],
            ],
        ],
        dtype=np.float32,
    )
    expected = np.array(
        [
            [
                [0, 0, 0.01, 0.02],
                [0, 0, 0.05, 0.06],
                [0, 0, 0.09, 0.010],
                [0, 0, 0.013, 0.014],
            ],
            [
                [0, 0, 0.017, 0.018],
                [0, 0, 0.021, 0.022],
                [0, 0, 0.025, 0.026],
                [0, 0, 0.029, 0.030],
            ],
            [
                [0, 0, 0.033, 0.034],
                [0, 0, 0.037, 0.038],
                [0, 0, 0.041, 0.042],
                [0, 0, 0.045, 0.046],
            ],
            [
                [0, 0, 0.049, 0.050],
                [0, 0, 0.053, 0.054],
                [0, 0, 0.057, 0.058],
                [0, 0, 0.061, 0.062],
            ],
        ],
        dtype=np.float32,
    )
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    shifted_along_z_img = FGeometric.shift_scale_rotate(
        img,
        angle=0,
        scale=1,
        dx=0,
        dy=0,
        dz=0.5,
        axes="xy",
        interpolation=0,
        border_mode="constant",
    )
    assert_array_almost_equal_nulp(shifted_along_z_img, expected)


@pytest.mark.parametrize(["alpha", "expected"], [(1.5, 190), (3, 255)])
def test_random_contrast(alpha, expected):
    img = np.ones((100, 100, 100), dtype=np.uint8) * 127
    img = F.brightness_contrast_adjust(img, alpha=alpha)
    assert img.dtype == np.dtype("uint8")
    assert (img == expected).all()


@pytest.mark.parametrize(["alpha", "expected"], [(1.5, 0.6), (3, 1.0)])
def test_random_contrast_float(alpha, expected):
    img = np.ones((100, 100, 100), dtype=np.float32) * 0.4
    expected = np.ones((100, 100, 100), dtype=np.float32) * expected
    img = F.brightness_contrast_adjust(img, alpha=alpha)
    assert img.dtype == np.dtype("float32")
    assert_array_almost_equal_nulp(img, expected)


@pytest.mark.parametrize(["alpha", "expected"], [(1.5, 1500), (3, 3000)])
def test_random_contrast_int16(alpha, expected):
    img = np.ones((100, 100, 100), dtype=np.int16) * 1000
    expected = np.ones((100, 100, 100), dtype=np.int16) * expected
    img = F.brightness_contrast_adjust(img, alpha=alpha)
    assert img.dtype == np.dtype("int16")
    assert_array_almost_equal_nulp(img, expected)


@pytest.mark.parametrize(["beta", "expected"], [(-0.5, 50), (0.25, 125)])
def test_random_brightness(beta, expected):
    img = np.ones((100, 100, 100), dtype=np.uint8) * 100
    img = F.brightness_contrast_adjust(img, beta=beta)
    assert img.dtype == np.dtype("uint8")
    assert (img == expected).all()


@pytest.mark.parametrize(["beta", "expected"], [(0.2, 0.48), (-0.1, 0.36)])
def test_random_brightness_float(beta, expected):
    img = np.ones((100, 100, 100), dtype=np.float32) * 0.4
    expected = np.ones_like(img) * expected
    img = F.brightness_contrast_adjust(img, beta=beta)
    assert img.dtype == np.dtype("float32")
    assert_array_almost_equal_nulp(img, expected, 3)


@pytest.mark.parametrize(["beta", "expected"], [(-0.5, 50), (0.25, 125)])
def test_random_brightness_int16(beta, expected):
    img = np.ones((100, 100, 100), dtype=np.int16) * 100
    img = F.brightness_contrast_adjust(img, beta=beta)
    assert img.dtype == np.dtype("int16")
    assert (img == expected).all()


@pytest.mark.parametrize(["gamma", "expected"], [(1, 127), (0.8, 48)])
def test_gamma_transform(gamma, expected):
    img = np.ones((100, 100, 100), dtype=np.uint8) * 127
    img = F.gamma_transform(img, gamma=gamma)
    assert img.dtype == np.dtype("uint8")
    assert (img == expected).all()


@pytest.mark.parametrize(["gamma", "expected"], [(1, 0.4), (10, 0.00010486)])
def test_gamma_transform_float(gamma, expected):
    img = np.ones((100, 100, 100), dtype=np.float32) * 0.4
    expected = np.ones((100, 100, 100), dtype=np.float32) * expected
    img = F.gamma_transform(img, gamma=gamma)
    assert img.dtype == np.dtype("float32")
    assert np.allclose(img, expected)


@pytest.mark.parametrize(["gamma", "expected"], [(1, 1000), (0.5, 31)])
def test_gamma_transform_int16(gamma, expected):
    img = np.ones((100, 100, 100), dtype=np.int16) * 1000
    expected = np.ones((100, 100, 100), dtype=np.int16) * expected
    img = F.gamma_transform(img, gamma=gamma)
    assert img.dtype == np.dtype("int16")
    assert np.allclose(img, expected)


@pytest.mark.parametrize(
    ["dtype", "min_val", "max_val"],
    [
        (np.uint8, 0, 255),
        (np.uint16, 0, 65535),
        (np.uint32, 0, 4294967295),
        (np.int16, -32768, 32767),
    ],
)
def test_to_float_without_max_value_specified(dtype, min_val, max_val):
    img = np.ones((50, 50, 50), dtype=dtype)
    expected = (img.astype("float32") - min_val) / (max_val - min_val)
    assert_array_almost_equal_nulp(F.to_float(img), expected)


@pytest.mark.parametrize("max_value", [255.0, 65535.0, 4294967295.0])
def test_to_float_with_max_value_specified(max_value):
    img = np.ones((50, 50, 50), dtype=np.uint16)
    expected = img.astype("float32") / max_value
    assert_array_almost_equal_nulp(
        F.to_float(img, min_value=0, max_value=max_value), expected
    )


def test_to_float_unknown_dtype():
    img = np.ones((50, 50, 50), dtype=np.int64)
    with pytest.raises(RuntimeError) as exc_info:
        F.to_float(img)
    assert str(exc_info.value) == (
        "Can't infer the minimum and maximum value for dtype int64. You need to specify the minimum and maximum value manually by "
        "passing the min_value and max_value arguments"
    )


@pytest.mark.parametrize("max_value", [255.0, 65535.0, 4294967295.0])
def test_to_float_unknown_dtype_with_max_value(max_value):
    img = np.ones((50, 50, 50), dtype=np.int64)
    expected = img.astype("float32") / max_value
    assert_array_almost_equal_nulp(
        F.to_float(img, min_value=0, max_value=max_value), expected
    )


@pytest.mark.parametrize(
    ["dtype", "min_val", "max_val"],
    [
        (np.uint8, 0, 255),
        (np.uint16, 0, 65535),
        (np.uint32, 0, 4294967295),
        (np.int16, -32768, 32767),
    ],
)
def test_from_float_without_max_value_specified(dtype, min_val, max_val):
    img = np.ones((50, 50, 50), dtype=np.float32)
    expected = (img * (max_val - min_val) + min_val).astype(dtype)
    assert_array_almost_equal_nulp(F.from_float(img, np.dtype(dtype)), expected)


@pytest.mark.parametrize("max_value", [255.0, 65535.0, 4294967295.0])
def test_from_float_with_max_value_specified(max_value):
    img = np.ones((50, 50, 50), dtype=np.float32)
    expected = (img * max_value).astype(np.uint32)
    assert_array_almost_equal_nulp(
        F.from_float(img, dtype=np.uint32, min_value=0, max_value=max_value), expected
    )


@pytest.mark.parametrize("target", ["image", "mask"])
def test_scale(target):
    img = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]], dtype=np.uint8)
    expected = np.array(
        [
            [[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4]],
            [[1, 1, 2, 2], [1, 1, 2, 2], [3, 3, 4, 4], [3, 3, 4, 4]],
            [[5, 5, 6, 6], [5, 5, 6, 6], [7, 7, 8, 8], [7, 7, 8, 8]],
            [[5, 5, 6, 6], [5, 5, 6, 6], [7, 7, 8, 8], [7, 7, 8, 8]],
        ],
        dtype=np.uint8,
    )

    img, expected = convert_3d_to_target_format([img, expected], target=target)
    scaled = FGeometric.scale(img, scale=2, interpolation=0)
    assert np.array_equal(scaled, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_longest_max_size(target):
    img = np.arange(1, (4 * 4 * 8) + 1, dtype=np.uint8).reshape(4, 4, 8)
    expected = np.array(
        [[[1, 3, 6, 8], [25, 27, 30, 32]], [[97, 99, 102, 104], [121, 123, 126, 128]]],
        dtype=np.uint8,
    )

    img, expected = convert_3d_to_target_format([img, expected], target=target)
    scaled = FGeometric.longest_max_size(img, max_size=4, interpolation=1)
    assert np.array_equal(scaled, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_smallest_max_size(target):
    img = np.arange(1, (4 * 4 * 8) + 1, dtype=np.uint8).reshape(4, 4, 8)
    expected = np.array(
        [[[1, 3, 6, 8], [25, 27, 30, 32]], [[97, 99, 102, 104], [121, 123, 126, 128]]],
        dtype=np.uint8,
    )

    img, expected = convert_3d_to_target_format([img, expected], target=target)
    scaled = FGeometric.smallest_max_size(img, max_size=2, interpolation=1)
    assert np.array_equal(scaled, expected)


def test_from_float_unknown_dtype():
    img = np.ones((50, 50, 50), dtype=np.float32)
    with pytest.raises(RuntimeError) as exc_info:
        F.from_float(img, np.dtype(np.int64))
    assert str(exc_info.value) == (
        "Can't infer the minimum and maximum value for dtype int64. You need to specify the minimum and maximum value manually by passing "
        "the min_value and max_value arguments"
    )


@pytest.mark.parametrize("target", ["image", "mask"])
def test_resize_default_interpolation(target):
    img = np.array(
        [
            [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
            [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
            [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
            [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
        ],
        dtype=np.uint8,
    )
    expected = np.array([[[1, 1], [4, 4]], [[1, 1], [4, 4]]], dtype=np.uint8)
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    resized_img = FGeometric.resize(img, 2, 2, 2)
    height, width, depth = resized_img.shape[:3]
    assert height == 2
    assert width == 2
    assert depth == 2
    assert np.array_equal(resized_img, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_resize_nearest_interpolation(target):
    img = np.array(
        [
            [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
            [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
            [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
            [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
        ],
        dtype=np.uint8,
    )
    expected = np.array([[[1, 1], [4, 4]], [[1, 1], [4, 4]]], dtype=np.uint8)
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    resized_img = FGeometric.resize(img, 2, 2, 2, interpolation=0)
    height, width, depth = resized_img.shape[:3]
    assert height == 2
    assert width == 2
    assert depth == 2
    assert np.array_equal(resized_img, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_resize_different_height_and_width(target):
    img = np.ones((50, 50, 50), dtype=np.uint8)
    img = convert_3d_to_target_format([img], target=target)
    resized_img = FGeometric.resize(img, height=20, width=30, depth=50)
    height, width, depth = resized_img.shape[:3]
    assert height == 20
    assert width == 30
    assert depth == 50


@pytest.mark.parametrize("target", ["image", "mask"])
def test_resize_default_interpolation_float(target):
    img = (
        np.array(
            [
                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
            ],
            dtype=np.float32,
        )
        * 0.1
    )
    expected = np.array([[[1, 1], [4, 4]], [[1, 1], [4, 4]]], dtype=np.float32) * 0.1
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    resized_img = FGeometric.resize(img, 2, 2, 2)
    height, width, depth = resized_img.shape[:3]
    assert height == 2
    assert width == 2
    assert depth == 2
    assert_array_almost_equal_nulp(resized_img, expected)


@pytest.mark.parametrize("target", ["image", "mask"])
def test_resize_nearest_interpolation_float(target):
    img = (
        np.array(
            [
                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]],
            ],
            dtype=np.float32,
        )
        * 0.1
    )
    expected = np.array([[[1, 1], [4, 4]], [[1, 1], [4, 4]]], dtype=np.float32) * 0.1
    img, expected = convert_3d_to_target_format([img, expected], target=target)
    resized_img = FGeometric.resize(img, 2, 2, 2, interpolation=0)
    height, width, depth = resized_img.shape[:3]
    assert height == 2
    assert width == 2
    assert depth == 2
    assert np.array_equal(resized_img, expected)


def test_bbox_vflip():
    assert FGeometric.bbox_vflip((0.1, 0.2, 0.3, 0.6, 0.5, 0.8), 100, 200, 100) == (
        0.1,
        0.5,
        0.3,
        0.6,
        0.8,
        0.8,
    )


def test_bbox_hflip():
    assert FGeometric.bbox_hflip((0.1, 0.2, 0.3, 0.6, 0.5, 0.8), 100, 200, 100) == (
        0.4,
        0.2,
        0.3,
        0.9,
        0.5,
        0.8,
    )


def test_bbox_zflip():
    assert np.isclose(
        FGeometric.bbox_zflip((0.1, 0.2, 0.3, 0.6, 0.5, 0.8), 100, 200, 100),
        (0.1, 0.2, 0.2, 0.6, 0.5, 0.7),
    ).all()


@pytest.mark.parametrize(
    ["code", "func"],
    [
        [0, FGeometric.bbox_vflip],
        [1, FGeometric.bbox_hflip],
        [2, FGeometric.bbox_zflip],
        [
            -1,
            lambda bbox, rows, cols, slices: FGeometric.bbox_zflip(
                FGeometric.bbox_vflip(
                    FGeometric.bbox_hflip(bbox, rows, cols, slices), rows, cols, slices
                ),
                rows,
                cols,
                slices,
            ),
        ],
    ],
)
def test_bbox_flip(code, func):
    rows, cols, slices = 100, 200, 100
    bbox = [0.1, 0.2, 0.3, 0.6, 0.5, 0.8]
    assert FGeometric.bbox_flip(bbox, code, rows, cols, slices) == func(
        bbox, rows, cols, slices
    )


def test_crop_bbox_by_coords():
    cropped_bbox = A.crop_bbox_by_coords(
        (0.5, 0.2, 0.3, 0.9, 0.7, 0.9),
        (18, 18, 0, 82, 82, 100),
        64,
        64,
        100,
        100,
        100,
        100,
    )
    assert cropped_bbox == (0.5, 0.03125, 0.3, 1.125, 0.8125, 0.9)


def test_bbox_center_crop():
    cropped_bbox = A.bbox_center_crop(
        (0.5, 0.2, 0.5, 0.9, 0.7, 0.9), 64, 64, 64, 100, 100, 100
    )
    assert cropped_bbox == (0.5, 0.03125, 0.5, 1.125, 0.8125, 1.125)


def test_bbox_crop():
    cropped_bbox = A.bbox_crop(
        (0.5, 0.2, 0.5, 0.9, 0.7, 0.9), 24, 24, 24, 64, 64, 64, 100, 100, 100
    )
    assert cropped_bbox == (0.65, -0.1, 0.65, 1.65, 1.15, 1.65)


def test_bbox_random_crop():
    cropped_bbox = A.bbox_random_crop(
        (0.5, 0.2, 0.5, 0.9, 0.7, 0.9), 80, 80, 80, 0.2, 0.1, 0.1, 100, 100, 100
    )
    assert cropped_bbox == (0.6, 0.2, 0.6, 1.1, 0.825, 1.1)


def test_bbox_rot90():
    assert FGeometric.bbox_rot90(
        (0.1, 0.2, 0.5, 0.3, 0.4, 0.6), 0, "xy", 100, 100, 300
    ) == (0.1, 0.2, 0.5, 0.3, 0.4, 0.6)
    assert FGeometric.bbox_rot90(
        (0.1, 0.2, 0.5, 0.3, 0.4, 0.6), 1, "xy", 100, 100, 300
    ) == (0.2, 0.7, 0.5, 0.4, 0.9, 0.6)
    assert FGeometric.bbox_rot90(
        (0.1, 0.2, 0.5, 0.3, 0.4, 0.6), 2, "xy", 100, 100, 300
    ) == (0.7, 0.6, 0.5, 0.9, 0.8, 0.6)
    assert FGeometric.bbox_rot90(
        (0.1, 0.2, 0.5, 0.3, 0.4, 0.6), 3, "xy", 100, 100, 300
    ) == (0.6, 0.1, 0.5, 0.8, 0.3, 0.6)


def test_bbox_transpose():
    assert np.allclose(
        FGeometric.bbox_transpose((0.7, 0.1, 0.5, 0.8, 0.4, 0.6), 0, 100, 200, 300),
        (0.1, 0.7, 0.5, 0.4, 0.8, 0.6),
    )
    assert np.allclose(
        FGeometric.bbox_transpose((0.7, 0.1, 0.5, 0.8, 0.4, 0.6), 1, 100, 200, 300),
        (0.6, 0.2, 0.5, 0.9, 0.3, 0.6),
    )


@pytest.mark.parametrize(
    ["bboxes", "min_area", "min_area_visibility", "target"],
    [
        (
            [
                (0.1, 0.5, 0.3, 1.1, 0.9, 0.6),
                (-0.1, 0.5, 0.3, 0.8, 0.9, 0.6),
                (0.1, 0.5, 0.3, 0.8, 0.9, 0.6),
            ],
            0,
            0,
            [
                (0.1, 0.5, 0.3, 1.0, 0.9, 0.6),
                (0.0, 0.5, 0.3, 0.8, 0.9, 0.6),
                (0.1, 0.5, 0.3, 0.8, 0.9, 0.6),
            ],
        ),
        (
            [(0.1, 0.5, 0.3, 0.8, 0.9, 0.6), (0.4, 0.5, 0.3, 0.5, 0.6, 0.6)],
            150,
            0,
            [(0.1, 0.5, 0.3, 0.8, 0.9, 0.6)],
        ),
        (
            [(0.1, 0.5, 0.3, 0.8, 0.9, 0.6), (0.4, 0.9, 0.3, 0.5, 1.6, 0.6)],
            0,
            0.75,
            [(0.1, 0.5, 0.3, 0.8, 0.9, 0.6)],
        ),
        (
            [(0.1, 0.5, 0.3, 0.8, 0.9, 0.6), (0.4, 0.7, 0.3, 0.5, 1.1, 0.6)],
            0,
            0.7,
            [(0.1, 0.5, 0.3, 0.8, 0.9, 0.6), (0.4, 0.7, 0.3, 0.5, 1.0, 0.6)],
        ),
    ],
)
def test_filter_bboxes(bboxes, min_area, min_area_visibility, target):
    filtered_bboxes = filter_bboxes(
        bboxes,
        min_planar_area=min_area,
        min_area_visibility=min_area_visibility,
        rows=100,
        cols=100,
        slices=100,
    )
    assert filtered_bboxes == target


@pytest.mark.parametrize(
    [
        "bboxes",
        "img_width",
        "img_height",
        "img_depth",
        "min_width",
        "min_height",
        "min_depth",
        "target",
    ],
    [
        [
            [
                (0.1, 0.1, 0.3, 0.9, 0.9, 0.6),
                (0.1, 0.1, 0.3, 0.2, 0.9, 0.6),
                (0.1, 0.1, 0.3, 0.9, 0.2, 0.6),
                (0.1, 0.1, 0.3, 0.2, 0.2, 0.6),
            ],
            100,
            100,
            100,
            20,
            20,
            0,
            [(0.1, 0.1, 0.3, 0.9, 0.9, 0.6)],
        ],
        [
            [
                (0.1, 0.1, 0.3, 0.9, 0.9, 0.6),
                (0.1, 0.1, 0.3, 0.2, 0.9, 0.6),
                (0.1, 0.1, 0.3, 0.9, 0.2, 0.6),
                (0.1, 0.1, 0.3, 0.2, 0.2, 0.6),
            ],
            100,
            100,
            100,
            20,
            0,
            0,
            [(0.1, 0.1, 0.3, 0.9, 0.9, 0.6), (0.1, 0.1, 0.3, 0.9, 0.2, 0.6)],
        ],
        [
            [
                (0.1, 0.1, 0.3, 0.9, 0.9, 0.6),
                (0.1, 0.1, 0.3, 0.2, 0.9, 0.6),
                (0.1, 0.1, 0.3, 0.9, 0.2, 0.6),
                (0.1, 0.1, 0.3, 0.2, 0.2, 0.6),
            ],
            100,
            100,
            100,
            0,
            20,
            0,
            [(0.1, 0.1, 0.3, 0.9, 0.9, 0.6), (0.1, 0.1, 0.3, 0.2, 0.9, 0.6)],
        ],
    ],
)
def test_filter_bboxes_by_min_width_height(
    bboxes, img_width, img_height, img_depth, min_width, min_height, min_depth, target
):
    filtered_bboxes = filter_bboxes(
        bboxes,
        cols=img_width,
        rows=img_height,
        slices=img_depth,
        min_width=min_width,
        min_height=min_height,
        min_depth=min_depth,
    )
    assert filtered_bboxes == target


def test_fun_max_size():
    target_width = 50

    img = np.empty((50, 25, 30), dtype=np.uint8)
    out = FGeometric.smallest_max_size(img, target_width, interpolation=1)

    assert out.shape == (100, target_width, 60)


def test_is_rgb_image():
    image = np.ones((5, 5, 5, 3), dtype=np.uint8)
    assert F.is_rgb_image(image)

    multispectral_image = np.ones((5, 5, 5, 4), dtype=np.uint8)
    assert not F.is_rgb_image(multispectral_image)

    gray_image = np.ones((5, 5, 5), dtype=np.uint8)
    assert not F.is_rgb_image(gray_image)

    gray_image = np.ones((5, 5, 5, 1), dtype=np.uint8)
    assert not F.is_rgb_image(gray_image)


def test_is_grayscale_image():
    image = np.ones((5, 5, 5, 3), dtype=np.uint8)
    assert not F.is_grayscale_image(image)

    multispectral_image = np.ones((5, 5, 5, 4), dtype=np.uint8)
    assert not F.is_grayscale_image(multispectral_image)

    gray_image = np.ones((5, 5, 5), dtype=np.uint8)
    assert F.is_grayscale_image(gray_image)

    gray_image = np.ones((5, 5, 5, 1), dtype=np.uint8)
    assert F.is_grayscale_image(gray_image)


def test_is_multispectral_image():
    image = np.ones((5, 5, 5, 3), dtype=np.uint8)
    assert not is_multispectral_image(image)

    multispectral_image = np.ones((5, 5, 5, 4), dtype=np.uint8)
    assert is_multispectral_image(multispectral_image)

    gray_image = np.ones((5, 5, 5), dtype=np.uint8)
    assert not is_multispectral_image(gray_image)

    gray_image = np.ones((5, 5, 5, 1), dtype=np.uint8)
    assert not is_multispectral_image(gray_image)

def test_posterize_checks():
    img = np.random.random([100, 100, 100])
    with pytest.raises(TypeError) as exc_info:
        F.posterize(img, 4)
    assert (
        str(exc_info.value)
        == "dtype must be one of ('uint8', 'uint16', 'int16', 'int32'), got float64"
    )

    img = np.random.randint(0, 256, [100, 100, 100], dtype=np.uint8)
    with pytest.raises(TypeError) as exc_info:
        F.posterize(img, [1, 2, 3])
    assert (
        str(exc_info.value)
        == "If bits is iterable, then image must be RGB or Multispectral"
    )


def test_equalize_checks():
    img = np.random.randint(0, 255, [50, 50, 10], dtype=np.uint8)

    mask = np.random.randint(0, 1, [50, 50, 10, 3], dtype=bool)
    with pytest.raises(ValueError) as exc_info:
        F.equalize(img, mask=mask)
    assert str(
        exc_info.value
    ) == "Wrong mask shape. Image shape: {}. Mask shape: {}".format(
        img.shape, mask.shape
    )

    img = np.random.random([50, 50, 10])
    with pytest.raises(TypeError) as exc_info:
        F.equalize(img, mask=mask)
    assert str(exc_info.value) == "Image must have int or uint type"

@pytest.mark.parametrize("dtype", ["float32", "uint8"])
def test_downscale_ones(dtype):
    img = np.ones((100, 100, 10), dtype=dtype)
    downscaled = F.downscale(img, scale=0.5)
    assert np.all(downscaled == img)


def test_downscale_random():
    img = np.random.rand(100, 100, 10)
    downscaled = F.downscale(img, scale=0.5)
    assert downscaled.shape == img.shape
    downscaled = F.downscale(img, scale=1)
    assert np.all(img == downscaled)


def test_maybe_process_by_channel():
    image = np.random.randint(0, 256, (50, 50, 50, 6), np.uint8)

    for i in range(1, image.shape[-1] + 1):
        before = image[:, :, :i]
        after = FGeometric.rotate(before, angle=0, axes="xy")
        assert before.shape == after.shape
