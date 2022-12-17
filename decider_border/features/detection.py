# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""common border validator
=======================

Detect the common border of selected `pages` as a expected correct page
border. Validate every page against this common border. Keep in mind to
decide between left and right page. In some printings there are two
different border **We do not support them yet**.

Some pdf-writer produces a massive amout of empty strings as a result of
miss-using `what you see is what you get`-editors. In some cases there
are a lot of `hit the box` errors.

* TODO: SUPPORT DIFFERENT LEFT AND RIGHT PAGE
* TODO: MARK EMPTY STRING LAYOUT ERRORS.
"""

import configo
import iamraw
import protocol
import serializeraw
import utila

import decider_border.detection.hits

MULTIPLE_BOUNDING_ERROR_COUNT = configo.HV_INT_PLUS(default=10)

PAGENUMBER_ERROR_MIN = configo.HV_INT_PLUS(default=5)


def work(
    border_boxes: str,
    border_pages: str,
    border_leftright: str,
    pagenumbers: str,
    pages: tuple = None,
) -> tuple[str, str, str]:
    utila.call('work: border detection')
    # create driver
    driver = create_driver(
        border_boxes,
        border_pages,
        border_leftright,
        pagenumbers,
        pages,
    )
    # evaluate lintings
    user, developer = protocol.run(modulename=__name__, driver=driver)
    # dump hits
    dumped = serializeraw.dump_hits(driver.hits)
    return dumped, user, developer


def create_driver(
    border_boxes,
    border_pages,
    border_leftright,
    pagenumbers,
    pages,
):
    boxes = serializeraw.load_boundingboxes(border_boxes, pages=pages)
    border_pages = serializeraw.load_pageborders(border_pages, pages=pages)
    pagesizes = {item.page: item.size for item in border_pages}
    border_leftright = serializeraw.load_leftright_border(border_leftright)
    expected = decider_border.detection.hits.BorderExpected(border_leftright)
    pagenumbers = load_pagenumbers(pagenumbers, pages=pages)
    # run detector
    hits, hits_pagenumbers = decider_border.detection.hits.boxes_outside_border(
        boxes,
        pagesizes,
        expected,
        pagenumbers=pagenumbers,
    )
    utila.debug(hits)
    result = protocol.driver(
        hits=hits,
        hits_pagenumbers=hits_pagenumbers,
    )
    return result


def load_pagenumbers(pagenumbers, pages: tuple = None) -> dict:
    # bounding boxes of detected pagenumbers
    pagenumbers = serializeraw.load_pagenumbers(pagenumbers, pages=pages)
    if isinstance(pagenumbers, tuple):
        pagenumbers = pagenumbers[0] + pagenumbers[1]
    result = {page.pdfpage: tuple(page.bounding) for page in pagenumbers}  # pylint:disable=E1101
    return result


# TODO: ADD DIFFERENT BORDER CHECKER LINTER FOR DIFFRENT AREAS, footenote,
# pagecontent, cropbox, etc.

SOLUTION_2020 = """\
Objekt beschreibt Seitenrand

Passen Sie die Formatierung an, so dass der Inhalt nicht mehr in den \
Seitenrad ragt.
"""

BOXES_HIT_COUNT_MAX = configo.HV_INT_PLUS(default=1000)


def check_2020_content_inside_box(linter, driver):
    """Ensure that content fits in detected content box."""
    hits: iamraw.PageContentHits = driver.hits
    if len(driver.hits_pagenumbers) < PAGENUMBER_ERROR_MIN:
        hits.extend(driver.hits_pagenumbers)
    hitcount = len(utila.flat([item[1] for item in hits]))
    if hitcount > BOXES_HIT_COUNT_MAX:
        # TODO: ENABLE AFTER boxes_repeating PERFORMS FASTER
        for item in hits:
            utila.debug(len(item[1]))
        protocol.skip_method(f'too many box hits: {hitcount}')
        return
    # determine multi page hits
    repeating = decider_border.detection.hits.boxes_repeating(hits)
    # remove multi page hits
    unique = decider_border.detection.hits.hits_unique(hits, repeating)
    for page in unique:
        if len(page.hits) > MULTIPLE_BOUNDING_ERROR_COUNT:
            # switch to 2025
            continue
        for _, bounding in page.hits:
            location = iamraw.BoundingLocation.fromtuple(
                bounding=bounding,
                page=page.page,
            )
            linter(location=location)


SOLUTION_2025 = """\
Seitenrand überprüfen

{{number}} Objekte auf Seite {{page}} ragen in den erwarteten Seitenrand. \
Überprüfen Sie ob dies so gewollt ist.
"""


def check_2025_multiple_bounding_error(linter, driver):
    """Ensure that content fits in detected content box."""
    hits: iamraw.PageContentHits = driver.hits
    hitcount = len(utila.flat([item[1] for item in hits]))
    if hitcount > BOXES_HIT_COUNT_MAX:
        # TODO: ENABLE AFTER boxes_repeating PERFORMS FASTER
        protocol.skip_method(f'too many box hits: {hitcount}')
        return
    # determine multi page hits
    repeating = decider_border.detection.hits.boxes_repeating(hits)
    # remove multi page hits
    unique = decider_border.detection.hits.hits_unique(hits, repeating)
    for page in unique:
        if len(page.hits) <= MULTIPLE_BOUNDING_ERROR_COUNT:
            continue
        bounding = utila.rect_max([bound for _, bound in page.hits])
        location = iamraw.BoundingLocation.fromtuple(
            bounding=bounding,
            page=page.page,
        )
        linter(
            number=len(page.hits),
            page=page.page,
            location=location,
        )


SOLUTION_2026 = """\
Seitenzahl beschreibt den Seitenrand

{{number}} Seitenzahlen beschreiben den Seitenrand.
"""


def check_2026_pagenumber_bounding(linter, driver):
    if len(driver.hits_pagenumbers) < PAGENUMBER_ERROR_MIN:
        return
    linter(
        number=len(driver.hits_pagenumbers),
        location=protocol.OVERVIEW,
    )
