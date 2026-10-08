# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw

import decider_textstyle
import tests.textstyle_


@pytest.mark.xfail(
    reason='improve algo leads to fewer findings which are not disabled anymore.'
)
def test_textstyle_diss157_disable_huge_finding_count(td, mp):
    source = hoverpower.link(hoverpower.DISS157_PDF)
    cmd = f'-i {source}  --text --pages=70:80'
    tests.textstyle_.run(cmd, mp=mp)
    path = decider_textstyle.path.text(td.tmpdir)
    findings = serializeraw.load_findings(
        path,
        pages=77,
    )
    assert findings
    findings = serializeraw.load_findings(
        path,
        msgids={7550, 7551, 7555},
        pages=77,
    )
    assert not findings
