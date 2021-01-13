# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import decider_textstyle
import tests.textstyle_


@utilatest.longrun
def test_textstyle_formula_master116_page22(testdir, monkeypatch):
    """Ensure that formulas are not treated as font size errors."""
    source = power.link(power.MASTER116_PDF)
    cmd = f'-i {source}  --text --pages=21,22'
    tests.textstyle_.run(cmd, monkeypatch=monkeypatch)
    path = decider_textstyle.path.text(testdir.tmpdir)
    findings = serializeraw.load_findings(
        path,
        msgids={7550, 7551, 7555},
        pages=22,
    )
    # HINT: COLUMBSCHES is detected as font face error. This may change in
    # the future. TODO: MAY SKIP MATH IN TEXT IN THE FUTURE
    assert len(findings) == 15
