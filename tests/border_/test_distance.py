# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import groupme.path
import power
import pytest
import serializeraw

import decider_border.features.distance


@pytest.mark.parametrize('page, expected', [
    pytest.param(0, 0),
    pytest.param(5, 3, id='5_3', marks=pytest.mark.xfail(reason='???')),
])
def test_border_distances_linting(page, expected):
    area = groupme.path.area(power.link(power.DOCU007_PDF))
    distance = groupme.path.distance(power.link(power.DOCU007_PDF))
    dumped_findings = decider_border.features.distance.work(
        area,
        distance,
        pages=page,
    )
    findings = serializeraw.load_findings(dumped_findings[0])
    assert len(findings) == expected, findings
