# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import protocol
import pytest
import serializeraw
import utilatest

import decider_textstyle
import decider_textstyle.text.space
import tests.textstyle_


@utilatest.requires(power.BACHELOR056_PDF)
def test_textspace_bachelor56page9(td, mp):
    source = power.link(power.BACHELOR056_PDF)
    with mp.context() as context:
        maxwidth = lambda height: 10  # smallest gap to ensure findings
        context.setattr(decider_textstyle.text.space, "MAXWIDTH", maxwidth)
        tests.textstyle_.run(
            f'-i {source} --text --pages=5:10',
            mp=mp,
        )
    findings = serializeraw.load_findings(
        decider_textstyle.path.text(td.tmpdir),
        msgids=(7770, 7771),
        pages=(9,),
    )
    # single merged line
    assert len(findings) == 1  # TODO: VALIDATED


@pytest.mark.xfail(reason='improve figure extractor')
@utilatest.requires(power.MASTER075_PDF)
def test_textspace_master75page23(td, mp):
    """Regression test; do not detect any holes in figure captions."""
    source = power.link(power.MASTER075_PDF)
    tests.textstyle_.run(
        f'-i {source} --text --pages=10:25',
        mp=mp,
    )
    findings = serializeraw.load_findings(
        decider_textstyle.path.text(td.tmpdir),
        msgids=7770,
    )
    findings = protocol.select(findings, pages=23, msgid=7770)
    assert not findings


@utilatest.requires(power.MASTER075_PDF)
def test_textspace_diss170page58_skip_text_hole(td, mp):
    """Regression test; do not detect any holes in table."""
    source = power.link(power.MASTER075_PDF)
    tests.textstyle_.run(
        f'-i {source} --text --pages=50:60',
        mp=mp,
    )
    findings = serializeraw.load_findings(
        decider_textstyle.path.text(td.tmpdir),
        msgids=7770,
    )
    findings = protocol.select(findings, pages=58, msgid=7770)
    assert not findings


@pytest.mark.xfail(reason='broken headlines extractor')
@utilatest.requires(power.MASTER091B_PDF)
def test_multiple_textspace_master91b(td, mp):
    source = power.link(power.MASTER091B_PDF)
    tests.textstyle_.run(
        f'-i {source} --text --pages=14:17',
        mp=mp,
    )
    findings = serializeraw.load_findings(
        decider_textstyle.path.text(td.tmpdir),
        msgids={7770, 7771},
    )
    # merge multiple 7770 in a line into a single 7771
    assert not protocol.select(findings, pages=16, msgid=7770)
    findings = protocol.select(findings, pages=16, msgid=7771)
    assert len(findings) == 1  # VALIDATED
