# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import protoerror
import pytest
import serializeraw
import utilotest

import decider_textstyle.path
import tests.textstyle_

NO_STYLE = iamraw.DocTextStyle()


def decide_text_style(
    source,
    pages,
    td,
    mp,
    style=None,
    msgids=None,
):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    if style:
        tests.textstyle_.write_docstyle(style, td.tmpdir)
    tests.textstyle_.run(
        f'--text -i {td.tmpdir} -i {source} --pages={pages}',
        mp=mp,
    )
    path = decider_textstyle.path.text(td.tmpdir)
    findings = serializeraw.load_findings(path, msgids=msgids)
    return findings


@utilotest.nightly
def test_decider_text_master72_2_20_fontsize(td, mp):
    style = iamraw.DocTextStyle(text_size=12.0)
    pages = '2:20'
    findings = decide_text_style(
        hoverpower.MASTER072_PDF,
        pages,
        td,
        mp,
        style,
    )
    # no text family error, cause only whitespace error is detected
    assert not protoerror.count_findings(findings, 7551)
    # text size
    assert not protoerror.count_findings(findings, 7550)


@utilotest.longrun
def test_decider_text_master72_2_10_fontfamily(td, mp):
    # Hint: adjust text_family after text parser change
    style = iamraw.DocTextStyle(text_family=-1702503278)
    pages = '2:10'
    findings = decide_text_style(
        hoverpower.MASTER072_PDF,
        pages,
        td,
        mp,
        style,
    )
    # not correct, but indicates that algo changed
    assert not protoerror.count_findings(findings, 7551)


@utilotest.longrun
def test_decider_text_bachelor76_4_10_bold_font(td, mp):
    pages = '2:10'
    findings = decide_text_style(
        hoverpower.BACHELOR076_PDF,
        pages,
        td,
        mp,
        NO_STYLE,
    )
    # five words marked bold
    assert protoerror.count_findings(findings, msgid=7555) == 5


@pytest.mark.xfail(reason='long time broken, don\'t know why')
@utilotest.nightly
def test_decider_textstyle_merge_connected_findings(td, mp):
    """Merge more than one line with the same finding into a single finding."""
    pages = '18:22'
    findings = decide_text_style(
        hoverpower.MASTER072_PDF,
        pages,
        td,
        mp,
        msgids=7550,
    )
    assert len(findings) == 1, len(findings)


def test_textstyle_warning_in_wordfigure_bachelor51_pag30(td, mp):
    """Regression test that figure text is not detected as text style error.

    This was an error cause figure was not extracted correctly and
    therefore magic does not detect these region as figure region.
    """
    # 28: is required, cause we require the first headline
    pages = '28:31'
    findings = decide_text_style(
        hoverpower.BACHELOR051_PDF,
        pages,
        td,
        mp,
        msgids=7550,
    )
    # select page 30
    findings = protoerror.select_pages(findings, 30)
    assert not findings


@pytest.mark.xfail(reason='bad formula parser')
def test_textstyle_master110_page29(td, mp):
    """Investigate text style errors, especially in connection with formulas."""
    pages = '20:30'
    findings = decide_text_style(
        hoverpower.MASTER110_PDF,
        pages,
        td,
        mp,
        msgids={7550, 7551},
    )
    # select page 29
    findings = protoerror.select_pages(findings, 29)
    # invalid formula detection produces math style error
    assert len(findings) == 8  # may change in the future
