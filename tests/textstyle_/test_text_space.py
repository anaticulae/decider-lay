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
import decider_textstyle.text.space
import tests.textstyle_


def test_textspace_bachelor56page9(testdir, monkeypatch):
    source = power.link(power.BACHELOR056_PDF)
    with monkeypatch.context() as context:
        maxwidth = lambda height: 10  # smallest gap to ensure findings
        context.setattr(decider_textstyle.text.space, "MAXWIDTH", maxwidth)
        tests.textstyle_.run(
            f'-i {source} --text --pages=5:10',
            monkeypatch=monkeypatch,
        )
    findings = serializeraw.load_findings(
        decider_textstyle.path.text(testdir.tmpdir),
        msgids=7770,
    )
    findings = protocol.select_pages(findings, 9)
    assert len(findings) == 5  # TODO: NOT VALIDATED


def test_textspace_master75page23(testdir, monkeypatch):
    """Regression test; do not detect any holes in figure captions."""
    source = power.link(power.MASTER075_PDF)
    tests.textstyle_.run(
        f'-i {source} --text --pages=10:25',
        monkeypatch=monkeypatch,
    )
    findings = serializeraw.load_findings(
        decider_textstyle.path.text(testdir.tmpdir),
        msgids=7770,
    )
    findings = protocol.select(findings, pages=23, msgid=7770)
    assert not findings


def test_textspace_diss170page58_skip_text_hole(testdir, monkeypatch):
    """Regression test; do not detect any holes in table."""
    source = power.link(power.MASTER075_PDF)
    tests.textstyle_.run(
        f'-i {source} --text --pages=50:60',
        monkeypatch=monkeypatch,
    )
    findings = serializeraw.load_findings(
        decider_textstyle.path.text(testdir.tmpdir),
        msgids=7770,
    )
    findings = protocol.select(findings, pages=58, msgid=7770)
    assert not findings
