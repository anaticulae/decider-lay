# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import power
import pytest
import serializeraw
import utila
import utilatest

import decider_border.detection.hits
import decider_border.path
import tests.border_


@pytest.mark.parametrize('source', [
    pytest.param(power.link(power.TECH024_PDF), id='technical24'),
])
def test_border_cli_decider_simple(source, testdir, monkeypatch):
    root = testdir.tmpdir
    detected = tests.border_.extract_border_hits(root, source, monkeypatch)
    assert detected
    loaded = serializeraw.load_findings(
        decider_border.path.border_user(testdir.tmpdir))
    assert loaded


@pytest.mark.parametrize('source, validate', [
    pytest.param(power.link(power.DOCU35_PDF), [4, 4], id='twine'),
    pytest.param(power.link(power.MASTER078_PDF), [6, 8], id='master78'),
])
@utilatest.longrun
def test_border_cli_decider_list(
        source,
        validate,
        testdir,
        monkeypatch,
):  # pylint:disable=W0621
    """Run `border` to extract common BoundingBox and check pages
    against this common box."""
    with patch_zero_border_tolerance(monkeypatch):
        detected_hits = tests.border_.extract_border_hits(
            testdir.tmpdir,
            source,
            monkeypatch,
        )
    assert detected_hits
    # validated
    assert len(detected_hits) >= len(validate), (
        f'expected hits: {validate}\ncurrent: {len(detected_hits)}\n'
        f'hits: {detected_hits}')
    loaded = serializeraw.load_findings(
        decider_border.path.border_user(testdir.tmpdir))
    assert loaded


def validate_leftright(hits):
    expected_hits = []
    # text at bottom and
    expected_hits.append(0)
    # symbol at right top
    # TODO: reduce after extracting symbol as one
    expected_hits.extend([0] * 16)

    hits = utila.flatten(item.hits for item in hits)
    assert len(hits) >= len(expected_hits), (
        f'expected hits: {expected_hits}\n current: {len(hits)}\n')


@pytest.mark.parametrize('source, validate', [
    pytest.param(
        power.link(power.BOOK007_PDF),
        validate_leftright,
        id='leftright',
    ),
])
@utilatest.longrun
def test_border_cli_decider_complex_validation(
        source,
        validate,
        testdir,
        monkeypatch,
):  # pylint:disable=W0621
    """Ensure to run border detection and load linter result later."""
    root = testdir.tmpdir
    with patch_zero_border_tolerance(monkeypatch):
        detected = tests.border_.extract_border_hits(root, source, monkeypatch)
    validate(detected)
    loaded = serializeraw.load_findings(
        decider_border.path.border_user(testdir.tmpdir))
    assert loaded


@contextlib.contextmanager
def patch_zero_border_tolerance(monkeypatch):
    with monkeypatch.context() as context:
        context.setattr(decider_border.detection.hits, 'BORDER_LEFT', 0)
        context.setattr(decider_border.detection.hits, 'BORDER_RIGHT', 0)
        context.setattr(decider_border.detection.hits, 'BORDER_TOP', 0)
        context.setattr(decider_border.detection.hits, 'BORDER_BOTTOM', 0)
        yield


def test_border_included_pdf_page_as_image(testdir, monkeypatch):
    """Do not detect included pdf pages as bounding error."""
    source = power.link(power.MASTER116_PDF)
    root = testdir.tmpdir
    extracted = tests.border_.extract_border_hits(
        root,
        source,
        monkeypatch=monkeypatch,
        pages='2',
    )
    hits = utila.select_page(extracted, page=2).hits
    assert not hits


def test_border_whitespace_only(testdir, monkeypatch):
    """Do not detect included pdf pages as bounding error."""
    source = power.link(power.BACHELOR076_PDF)
    root = testdir.tmpdir
    extracted = tests.border_.extract_border_hits(
        root,
        source,
        monkeypatch=monkeypatch,
        pages='0',
    )
    hits = utila.select_page(extracted, page=0).hits
    assert not hits
