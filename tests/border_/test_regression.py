# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utilatest

import tests.border_


@pytest.mark.usefixtures('testdir')
def test_decider_border_diss266(monkeypatch, capsys):
    """We have only one rotated page. Therefore we have no expected page
    size and have to skip this."""
    source = power.link(power.DISS266_PDF)
    tests.border_.run(f'-i {source}', monkeypatch=monkeypatch)
    assert 'no expected page size' in utilatest.stderr(capsys)
