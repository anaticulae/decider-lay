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
import tests
import tests.textstyle_

MASTER_72_DOCSTYLE = iamraw.DocTextStyle(
    h1_size=15.96,
    h1_after=135.93 - 88.67,
    h2_size=14.04,
    h2_before=190.37 - 125.73,
    h2_after=224.01 - 190.37,
)

BACHELOR_76_DOCSTYLE = iamraw.DocTextStyle(
    h1_after=132.18 - 92.87,
    h1_size=15.96,
    h2_after=529.1 - 485.39,
    h2_before=485.39 - 426.84,
    h2_size=12.96,
)

# disable font style linting
NO_STYLE = iamraw.DocTextStyle()


def decide_headline_style(source, pages, style, td, mp):
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    tests.textstyle_.write_docstyle(style, td.tmpdir)
    tests.textstyle_.run(
        f'--headlines -i {td.tmpdir} -i {source} --pages={pages}',
        mp=mp,
    )
    path = decider_textstyle.path.headlines(td.tmpdir)
    findings = serializeraw.load_findings(path)
    return findings


@pytest.mark.xfail(reason='failing magic/list parer')
@utilotest.nightly
def test_decider_headlines_master72_2_20_fontsize(td, mp):
    source = hoverpower.MASTER072_PDF
    pages = '2:20'
    findings = decide_headline_style(
        source,
        pages,
        MASTER_72_DOCSTYLE,
        td,
        mp,
    )
    # no font size error
    assert not protoerror.count_findings(findings, 7500)
    assert not protoerror.count_findings(findings, 7510)
    assert not protoerror.count_findings(findings, 7520)
    assert not findings


@pytest.mark.xfail(reason='failing magic/list parer')
@utilotest.nightly
def test_decider_headlines_master72_all(td, mp):
    source = hoverpower.MASTER072_PDF
    pages = '3:65'
    findings = decide_headline_style(
        source,
        pages,
        MASTER_72_DOCSTYLE,
        td,
        mp,
    )
    # no font size error
    assert not findings


@utilotest.longrun
def test_decider_headlines_bachelor76(td, mp):
    # TODO: EXTEND THIS TESTS, specify expected findings
    source = hoverpower.BACHELOR076_PDF
    pages = '4:67'
    findings = decide_headline_style(
        source,
        pages,
        BACHELOR_76_DOCSTYLE,
        td,
        mp,
    )
    # TODO: IMPROVE HEADLINE EXTRACTOR
    expected = (31, 32, 33)  # not correct, but indicates that algo changed
    # TODO: FILTER EXPECTED FINDINGS AND MAKE TEST MORE CONCRETE
    assert len(findings) in expected


@utilotest.longrun
def test_decider_headlines_chapter_on_new_page(td, mp):
    source = hoverpower.BACHELOR076_PDF
    pages = '0:42'
    findings = decide_headline_style(
        source,
        pages,
        NO_STYLE,
        td,
        mp,
    )
    no_new_page_start = protoerror.select_findings(findings, 7540)
    assert len(no_new_page_start) == 2, str(no_new_page_start)


@utilotest.longrun
def test_chapter_on_new_page_with_decoration(td, mp):
    source = hoverpower.MASTER110_PDF
    pages = '18:20'
    findings = decide_headline_style(
        source,
        pages,
        NO_STYLE,
        td,
        mp,
    )
    new_chapter_page_start_error = protoerror.select_findings(findings, 7540)
    assert not new_chapter_page_start_error


@utilotest.requires(hoverpower.BACHELOR063_PDF)
def test_headlines_bachelor63_page17(td, mp):
    """Do not parse font size error for white spaces in first level headlines.

    Regression test after fixing docstyle extractor.
    """
    source = hoverpower.link(hoverpower.BACHELOR063_PDF)
    pages = 17
    tests.textstyle_.run(
        f'--headlines -i {td.tmpdir} -i {source} --pages={pages}',
        mp=mp,
    )
    path = decider_textstyle.path.headlines(td.tmpdir)
    findings = serializeraw.load_findings(path, msgids={7500, 7510, 7520})
    assert not findings


@utilotest.longrun
@utilotest.requires(hoverpower.BACHELOR090_PDF)
def test_headlines_bachelor90_page17_divide_headline(td, mp):
    source = hoverpower.link(hoverpower.BACHELOR090_PDF)
    tests.textstyle_.run(
        f'--headlines -i {td.tmpdir} -i {source} --pages=17',
        mp=mp,
    )
    path = decider_textstyle.path.headlines(td.tmpdir)
    findings = serializeraw.load_findings(path, msgids={7560})
    assert findings


@utilotest.requires(hoverpower.BACHELOR090_PDF)
def test_headlines_bachelor90_all_divide_headline(td, mp):
    source = hoverpower.link(hoverpower.BACHELOR090_PDF)
    tests.textstyle_.run(
        f'--headlines -i {td.tmpdir} -i {source}',
        mp=mp,
    )
    path = decider_textstyle.path.headlines(td.tmpdir)
    findings = serializeraw.load_findings(path, msgids={7560})
    pages = [finding.location.page for finding in findings]
    assert pages == [15, 17, 64]
