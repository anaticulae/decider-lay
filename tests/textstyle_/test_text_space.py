# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import serializeraw

import decider_textstyle
import tests.textstyle_


def test_textspace_bachelor56page9(testdir, monkeypatch):
    source = power.link(power.BACHELOR056_PDF)
    tests.textstyle_.run(
        f'-i {source} --text --pages=5:10',
        monkeypatch=monkeypatch,
    )
    findings = serializeraw.load_findings(
        decider_textstyle.path.text(testdir.tmpdir),
        msgids=7770,
    )
    findings = protocol.select_pages(findings, 9)
    assert findings  # TODO: NOT VALIDATED
