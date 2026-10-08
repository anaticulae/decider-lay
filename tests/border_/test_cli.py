# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import decider_border.detection.hits
import decider_border.path
import tests.border_


@pytest.mark.parametrize('source', [
    pytest.param(hoverpower.TECH024_PDF, id='tech024'),
])
def test_border_cli_decider_simple(source, td, mp):
    root = td.tmpdir
    detected = tests.border_.extract_border_hits(root, source, mp)
    assert detected
    loaded = serializeraw.load_findings(
        decider_border.path.border_user(td.tmpdir))
    assert loaded


@pytest.mark.parametrize('source, validate', [
    pytest.param(hoverpower.DOCU035_PDF, [4, 4], id='docu035'),
    pytest.param(hoverpower.MASTER078_PDF, [6, 8], id='master078'),
])
@utilotest.longrun
def test_border_cli_decider_list(
    source,
    validate,
    td,
    mp,
):  # pylint:disable=W0621
    """Run `border` to extract common BoundingBox and check pages
    against this common box."""
    with patch_zero_border_tolerance(mp):
        detected_hits = tests.border_.extract_border_hits(
            td.tmpdir,
            source,
            mp,
        )
    assert detected_hits
    # validated
    assert len(detected_hits) >= len(validate), (
        f'expected hits: {validate}\ncurrent: {len(detected_hits)}\n'
        f'hits: {detected_hits}')
    loaded = serializeraw.load_findings(
        decider_border.path.border_user(td.tmpdir))
    assert loaded


def validate_leftright(hits):
    expected_hits = []
    # text at bottom and
    expected_hits.append(0)
    # symbol at right top
    # TODO: reduce after extracting symbol as one
    expected_hits.extend([0] * 16)

    hits = utilo.flat(item.hits for item in hits)
    assert len(hits) >= len(expected_hits), (
        f'expected hits: {expected_hits}\n current: {len(hits)}\n')


@pytest.mark.parametrize('source, validate', [
    pytest.param(hoverpower.BOOK007_PDF, validate_leftright, id='book007'),
])
@utilotest.longrun
def test_border_cli_decider_complex_validation(
    source,
    validate,
    td,
    mp,
):  # pylint:disable=W0621
    """Ensure to run border detection and load linter result later."""
    root = td.tmpdir
    with patch_zero_border_tolerance(mp):
        detected = tests.border_.extract_border_hits(root, source, mp)
    validate(detected)
    loaded = serializeraw.load_findings(
        decider_border.path.border_user(td.tmpdir))
    assert loaded


@contextlib.contextmanager
def patch_zero_border_tolerance(mp):
    with mp.context() as context:
        context.setattr(decider_border.detection.hits, 'BORDER_LEFT', 0)
        context.setattr(decider_border.detection.hits, 'BORDER_RIGHT', 0)
        context.setattr(decider_border.detection.hits, 'BORDER_TOP', 0)
        context.setattr(decider_border.detection.hits, 'BORDER_BOTTOM', 0)
        yield


def test_border_included_pdf_page_as_image(td, mp):
    """Do not detect included pdf pages as bounding error."""
    source = hoverpower.MASTER116_PDF
    root = td.tmpdir
    extracted = tests.border_.extract_border_hits(
        root,
        source,
        mp=mp,
        pages='2',
    )
    hits = utilo.select_page(extracted, page=2).hits
    assert not hits


def test_border_whitespace_only(td, mp):
    """Do not detect included pdf pages as bounding error."""
    source = hoverpower.BACHELOR076_PDF
    root = td.tmpdir
    extracted = tests.border_.extract_border_hits(
        root,
        source,
        mp=mp,
        pages='0',
    )
    hits = utilo.select_page(extracted, page=0).hits
    assert not hits
