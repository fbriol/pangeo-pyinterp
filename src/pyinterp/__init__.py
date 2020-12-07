# Copyright (c) 2020 CNES
#
# All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.
from . import version
from .axis import TemporalAxis
from .binning import Binning2D
from .core import Axis
from .grid import Grid2D, Grid3D, Grid4D
from .interpolator.spline import spline
from .interpolator.bivariate import bivariate
from .interpolator.quadrivariate import quadrivariate
from .interpolator.trivariate import trivariate
from .rtree import RTree
__version__ = version.release()
__date__ = version.date()
del version
