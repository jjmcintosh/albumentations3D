import io
import os
import subprocess
import re
from pkg_resources import DistributionNotFound, get_distribution
from setuptools import find_packages, setup

INSTALL_REQUIRES = [
    "numpy>=1.11.1",
    "scipy>=1.10.0",
    "scikit-image>=0.16.1",
    "PyYAML",
    "qudida>=0.0.4",
    "pydicom",
    "setuptools",
]

# If none of packages in first installed, install second package
CHOOSE_INSTALL_REQUIRES = [
    (
        (
            "opencv-python>=4.1.1",
            "opencv-contrib-python>=4.1.1",
            "opencv-contrib-python-headless>=4.1.1",
        ),
        "opencv-python-headless>=4.1.1",
    )
]


def get_version():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(current_dir, "dicaugment", "__init__.py")
    with io.open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)


def get_long_description():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(base_dir, "README.md"), encoding="utf-8") as f:
        return f.read()


def choose_requirement(mains, secondary):
    """If some version of main requirement installed, return main,
    else return secondary.

    """
    chosen = secondary
    for main in mains:
        try:
            name = re.split(r"[!<>=]", main)[0]
            get_distribution(name)
            chosen = main
            break
        except DistributionNotFound:
            pass

    return str(chosen)


def get_install_requirements(install_requires, choose_install_requires):
    for mains, secondary in choose_install_requires:
        install_requires.append(choose_requirement(mains, secondary))

    return install_requires


setup(
    name="DICaugment",
    version="{{VERSION_PLACEHOLDER}}",
    description="3D medical image augmentation library",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="J. McIntosh, M. Mehdi Farhangi",
    license="MIT",
    url="https://github.com/DIDSR/dicaugment",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    package_data={"": ["data/kernels/*.npy"]},
    install_requires=get_install_requirements(
        INSTALL_REQUIRES, CHOOSE_INSTALL_REQUIRES
    ),
    extras_require={
        "tests": ["pytest"],
        "torch": ["torch", "torchvision", "torchaudio"],
        "tensorflow": ["tensorflow"],
        "develop": ["pytest", "torch", "tensorflow"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
