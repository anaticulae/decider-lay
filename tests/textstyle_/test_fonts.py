# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import decider_textstyle.path
import tests.textstyle_


def decide_text_fonts(source, testdir, monkeypatch, msgids: str = None):
    utilatest.fixture_requires(source)
    source = power.link(source)
    tests.textstyle_.run(
        f'--fonts -i {testdir.tmpdir} -i {source}',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.fonts(testdir.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


def test_decider_fonts_diss266_text_distance_invalid(testdir, monkeypatch):
    source = power.DISS266_PDF
    findings = decide_text_fonts(
        source,
        testdir,
        monkeypatch,
        msgids=7581,
    )
    assert len(findings) == 1


def test_decider_fonts_master072_text_distance_valid(testdir, monkeypatch):
    source = power.MASTER072_PDF
    findings = decide_text_fonts(
        source,
        testdir,
        monkeypatch,
        msgids=7581,
    )
    assert findings
    # assert not findings # TODO: ENABLE LATER
