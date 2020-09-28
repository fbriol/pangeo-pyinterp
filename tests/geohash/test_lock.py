# Copyright (c) 2020 CNES
#
# All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE file.
import tempfile
import os
import pickle
import pytest
import pyinterp.geohash as geohash


def test_lock_thread():
    lck = geohash.lock.ThreadSynchronizer()
    assert not lck.lock.locked()
    with lck:
        assert lck.lock.locked()
    assert not lck.lock.locked()
    with pytest.raises(TypeError):
        pickle.dumps(lck)


def test_lock_process() -> None:
    path = tempfile.NamedTemporaryFile().name
    assert not os.path.exists(path)
    lck = geohash.lock.ProcessSynchronizer(path)
    assert not os.path.exists(path)
    assert not lck.lock.locked()
    with lck:
        assert lck.lock.locked()
        lck2 = geohash.lock.ProcessSynchronizer(path, timeout=0.5)
        try:
            with lck2:
                assert False
        except geohash.lock.LockError:
            pass
        assert os.path.exists(path)
    assert not os.path.exists(path)
    assert isinstance(pickle.loads(pickle.dumps(lck)),
                      geohash.lock.ProcessSynchronizer)
    assert isinstance(str(lck), str)