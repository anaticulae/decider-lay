# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilotest

import tests.border_


@pytest.mark.usefixtures('td')
@utilotest.requires(hoverpower.DISS266_PDF)
def test_decider_border_diss266(mp, capsys):
    """We have only one rotated page. Therefore we have no expected page
    size and have to skip this."""
    source = hoverpower.link(hoverpower.DISS266_PDF)
    tests.border_.run(f'-i {source}', mp=mp)
    assert 'no expected page size' in utilotest.stderr(capsys)
