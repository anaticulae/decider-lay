# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import protocol
import pytest
import serializeraw
import utilatest

import decider_textstyle.path
import tests.textstyle_

NO_STYLE = iamraw.DocTextStyle()


def decide_text_style(
    source,
    pages,
    testdir,
    monkeypatch,
    style=None,
    msgids=None,
):
    source = power.link(source)
    if style:
        tests.textstyle_.write_docstyle(style, testdir.tmpdir)
    tests.textstyle_.run(
        f'--text -i {testdir.tmpdir} -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.text(testdir.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


@utilatest.nightly
def test_decider_text_master72_2_20_fontsize(testdir, monkeypatch):
    style = iamraw.DocTextStyle(text_size=12.0)
    pages = '2:20'
    findings = decide_text_style(
        power.MASTER072_PDF,
        pages,
        testdir,
        monkeypatch,
        style,
    )
    # no text family error, cause only whitespace error is detected
    assert not protocol.count_findings(findings, 7551)
    # text size
    assert not protocol.count_findings(findings, 7550)


@utilatest.longrun
def test_decider_text_master72_2_10_fontfamily(testdir, monkeypatch):
    # Hint: adjust text_family after text parser change
    style = iamraw.DocTextStyle(text_family=-1702503278)
    pages = '2:10'
    findings = decide_text_style(
        power.MASTER072_PDF,
        pages,
        testdir,
        monkeypatch,
        style,
    )
    # not correct, but indicates that algo changed
    assert not protocol.count_findings(findings, 7551)


@utilatest.longrun
def test_decider_text_bachelor76_4_10_bold_font(testdir, monkeypatch):
    pages = '2:10'
    findings = decide_text_style(
        power.BACHELOR076_PDF,
        pages,
        testdir,
        monkeypatch,
        NO_STYLE,
    )
    # five words marked bold
    assert protocol.count_findings(findings, msgid=7555) == 5


@pytest.mark.xfail(reason='long time broken, don\'t know why')
@utilatest.nightly
def test_decider_textstyle_merge_connected_findings(testdir, monkeypatch):
    """Merge more than one line with the same finding into a single finding."""
    pages = '18:22'
    findings = decide_text_style(
        power.MASTER072_PDF,
        pages,
        testdir,
        monkeypatch,
        msgids=7550,
    )
    assert len(findings) == 1, len(findings)


def test_textstyle_warning_in_wordfigure_bachelor51_pag30(testdir, monkeypatch):
    """Regression test that figure text is not detected as text style error.

    This was an error cause figure was not extracted correctly and
    therefore magic does not detect these region as figure region.
    """
    # 28: is required, cause we require the first headline
    pages = '28:31'
    findings = decide_text_style(
        power.BACHELOR051_PDF,
        pages,
        testdir,
        monkeypatch,
        msgids=7550,
    )
    # select page 30
    findings = protocol.select_pages(findings, 30)
    assert not findings


@pytest.mark.xfail(reason='bad formula parser')
def test_textstyle_master110_page29(testdir, monkeypatch):
    """Investigate text style errors, especially in connection with formulas."""
    pages = '20:30'
    findings = decide_text_style(
        power.MASTER110_PDF,
        pages,
        testdir,
        monkeypatch,
        msgids={7550, 7551},
    )
    # select page 29
    findings = protocol.select_pages(findings, 29)
    # invalid formula detection produces math style error
    assert len(findings) == 8  # may change in the future
