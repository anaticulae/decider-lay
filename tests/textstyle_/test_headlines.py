# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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


def decide_headline_style(source, pages, style, testdir, monkeypatch):
    tests.textstyle_.write_docstyle(style, testdir.tmpdir)
    tests.textstyle_.run(
        f'--headlines -i {testdir.tmpdir} -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.headlines(testdir.tmpdir)
    findings = serializeraw.load_findings(path)
    return findings


@pytest.mark.xfail(reason='failing magic/list parer')
@utilatest.longrun
def test_decider_headlines_master72_2_20(testdir, monkeypatch):
    source = power.link(power.MASTER072_PDF)
    pages = '2:20'
    findings = decide_headline_style(
        source,
        pages,
        MASTER_72_DOCSTYLE,
        testdir,
        monkeypatch,
    )
    # no font size error
    assert not findings


@pytest.mark.xfail(reason='failing magic/list parer')
@utilatest.longrun
def test_decider_headlines_master72_all(testdir, monkeypatch):
    source = power.link(power.MASTER072_PDF)
    pages = '3:65'
    findings = decide_headline_style(
        source,
        pages,
        MASTER_72_DOCSTYLE,
        testdir,
        monkeypatch,
    )
    # no font size error
    assert not findings


@utilatest.longrun
def test_decider_headlines_bachelor76(testdir, monkeypatch):
    # TODO: EXTEND THIS TESTS, specify expected findings
    source = power.link(power.BACHELOR076_PDF)
    pages = '4:67'
    findings = decide_headline_style(
        source,
        pages,
        BACHELOR_76_DOCSTYLE,
        testdir,
        monkeypatch,
    )
    # TODO: IMPROVE HEADLINE EXTRACTOR
    expected = 32  # not correct, but indicates that algo changed
    # TODO: FILTER EXPECTED FINDINGS AND MAKE TEST MORE CONCRETE
    assert len(findings) == expected


@utilatest.longrun
def test_decider_headlines_chapter_on_new_page(testdir, monkeypatch):
    source = power.link(power.BACHELOR076_PDF)
    pages = '0:42'
    findings = decide_headline_style(
        source,
        pages,
        NO_STYLE,
        testdir,
        monkeypatch,
    )
    no_new_page_start = protocol.select_findings(findings, 7540)
    assert len(no_new_page_start) == 2, str(no_new_page_start)


@utilatest.longrun
def test_chapter_on_new_page_with_decoration(testdir, monkeypatch):
    source = power.link(power.MASTER110_PDF)
    pages = '18:20'
    findings = decide_headline_style(
        source,
        pages,
        NO_STYLE,
        testdir,
        monkeypatch,
    )
    new_chapter_page_start_error = protocol.select_findings(findings, 7540)
    assert not new_chapter_page_start_error


def test_headlines_bachelor63_page17(testdir, monkeypatch):
    """Do not parse font size error for white spaces in first level
    headlines. Regression test after fixing docstyle extractor."""
    source = power.link(power.BACHELOR063_PDF)
    pages = 17
    tests.textstyle_.run(
        f'--headlines -i {testdir.tmpdir} -i {source} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.headlines(testdir.tmpdir)
    findings = serializeraw.load_findings(path, msgids={7500, 7510, 7520})
    assert not findings


@utilatest.longrun
def test_headlines_bachelor90_page17_divide_headline(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    tests.textstyle_.run(
        f'--headlines -i {testdir.tmpdir} -i {source} --pages=17',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.headlines(testdir.tmpdir)
    findings = serializeraw.load_findings(path, msgids={7560})
    assert findings


def test_headlines_bachelor90_all_divide_headline(testdir, monkeypatch):
    source = power.link(power.BACHELOR090_PDF)
    tests.textstyle_.run(
        f'--headlines -i {testdir.tmpdir} -i {source}',
        monkeypatch=monkeypatch,
    )
    path = decider_textstyle.path.headlines(testdir.tmpdir)
    findings = serializeraw.load_findings(path, msgids={7560})
    pages = [finding.location.page for finding in findings]
    assert pages == [15, 17, 64]
