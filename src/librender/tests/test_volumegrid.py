import mitsuba
import pytest
import enoki as ek

import numpy as np
import os

def test01_numpy_conversion(variant_scalar_rgb):
    from mitsuba.render import VolumeGrid

    a = np.random.rand(4, 8, 16, 3).astype(np.float32)
    grid = VolumeGrid(a)
    assert np.allclose(a, np.array(grid))
    assert np.allclose(np.max(a), grid.max())
    assert np.allclose(a.shape[:3], grid.size())
    assert np.allclose(a.shape[3], grid.channel_count())

    # Don't ask for computation of the maximum value
    grid = VolumeGrid(a, False)
    assert np.allclose(a, np.array(grid))
    assert np.allclose(grid.max(), 0.0)
    assert np.allclose(a.shape[:3], grid.size())
    assert np.allclose(a.shape[3], grid.channel_count())


def test02_read_write(variant_scalar_rgb, tmpdir):
    from mitsuba.render import VolumeGrid

    tmp_file = os.path.join(str(tmpdir), "out.vol")
    grid = np.random.rand(4, 8, 16, 3).astype(np.float32)
    VolumeGrid(grid).write(tmp_file)
    loaded = VolumeGrid(tmp_file)
    assert np.allclose(np.array(loaded), grid)
    assert np.allclose(loaded.max(), np.max(grid))
    assert np.allclose(grid.shape[:3], loaded.size())
    assert np.allclose(grid.shape[3], loaded.channel_count())