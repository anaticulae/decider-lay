# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import protoerror
import utilo
import utilotest

import tests.border_


@utilotest.requires(hoverpower.BACHELOR056_PDF)
def test_border_repeating_element(td, mp):
    """Verify that duplicated hits on page border are valid.

    Ensure `maxdiff` is big enough to cover boxes which contains single
    page number 1,2,3 and 21,22,23 together.
    """
    source = hoverpower.link(hoverpower.BACHELOR056_PDF)
    tests.border_.run(f'-i {source}', mp=mp)
    findings = protoerror.findings_from_path(td.tmpdir)
    findings = utilo.flat([item.content for item in findings])
    findings = protoerror.select_findings(findings, 2020)
    assert len(findings) == 8  # TODO: NOT VALIDATED


@utilotest.requires(hoverpower.MASTER155_PDF)
def test_decider_border_merge_pagewarning(td, mp):
    """Merge more than 10 bounding lintings into a single page linting."""
    source = hoverpower.link(hoverpower.MASTER155_PDF)
    tests.border_.run(f'-i {source} --detection', mp=mp)
    findings = protoerror.select(
        protoerror.findings_from_path(td.tmpdir),
        pages=1,
        msgid=2020,
    )
    # deactivate normal bounding checker
    assert not findings
    findings = protoerror.select(
        protoerror.findings_from_path(td.tmpdir),
        pages=1,
        msgid=2025,
    )
    # ensure that single page bounding error is raised
    assert len(findings) == 1


@utilotest.requires(hoverpower.DISS172_PDF)
def test_decider_pagenumber_hits(td, mp):
    source = hoverpower.link(hoverpower.DISS172_PDF)
    tests.border_.run(f'-i {source} --detection', mp=mp)
    findings = protoerror.findings_from_path(td.tmpdir, msgid=2026)
    assert len(findings) == 1
