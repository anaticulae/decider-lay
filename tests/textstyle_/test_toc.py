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
import utilotest

import decider_textstyle.path
import tests.textstyle_


def decide_text_toc(source, td, mp, msgids: str = None):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    tests.textstyle_.run(
        f'--toc -i {td.tmpdir} -i {source}',
        mp=mp,
    )
    path = decider_textstyle.path.toc(td.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


@pytest.mark.xfail(reason='incomplete impl.')
def test_decider_toc_bachelor32p1(td, mp):
    source = hoverpower.BACHELOR032_PDF
    findings = decide_text_toc(
        source,
        td,
        mp,
    )
    assert findings
    # assert 0
