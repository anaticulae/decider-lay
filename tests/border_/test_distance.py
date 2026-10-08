# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupmes.path
import hoverpower
import pytest
import serializeraw
import utilotest

import decider_border.features.distance


@pytest.mark.parametrize('page, expected', [
    pytest.param(0, 0),
    pytest.param(5, 3, id='5_3', marks=pytest.mark.xfail(reason='???')),
])
@utilotest.requires(hoverpower.DOCU007_PDF)
def test_border_distances_linting(page, expected):
    source = hoverpower.link(hoverpower.DOCU007_PDF)
    area = groupmes.path.area(source)
    distance = groupmes.path.distance(source)
    dumped_findings = decider_border.features.distance.work(
        area,
        distance,
        pages=page,
    )
    findings = serializeraw.load_findings(dumped_findings[0])
    assert len(findings) == expected, findings
