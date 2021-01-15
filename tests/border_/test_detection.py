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
import utila

import tests.border_


def test_border_repeating_element(testdir, monkeypatch):
    """Verify that duplicated hits on page border are valid.

    Ensure `maxdiff` is big enough to cover boxes which contains single
    page number 1,2,3 and 21,22,23 together.
    """
    source = power.link(power.BACHELOR056_PDF)
    tests.border_.run(f'-i {source}', monkeypatch=monkeypatch)
    findings = protocol.findings_from_path(testdir.tmpdir)
    findings = utila.flatten([item.content for item in findings])
    findings = protocol.select_findings(findings, 2020)
    assert len(findings) == 8  # TODO: NOT VALIDATED
