# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

import contextlib
import functools
import math
import typing

import iamraw
import protocol
import serializeraw
import utila

# TODO: HOLY VALUE, ADJUST THIS HOLY VALUES
BORDER_LEFT = 25
BORDER_RIGHT = 25
BORDER_TOP = 25
BORDER_BOTTOM = 25


def work(
        border_boxes: str,
        border_pages: str,
        border_leftright: str,
        pages: tuple = None,
) -> typing.Tuple[str, str, str]:
    utila.call('work: border detection')
    boxes = serializeraw.load_boundingboxes(border_boxes, pages=pages)
    border_pages = serializeraw.load_pageborders(border_pages, pages=pages)

    page_sizes = {item.page: item.size for item in border_pages}
    border_leftright = serializeraw.load_leftright_border(border_leftright)
    expected = BorderExpected(border_leftright)

    hits = boxes_outside_border(boxes, page_sizes, expected)
    utila.debug(hits)

    dumped = serializeraw.dump_hits(hits)

    linter = protocol.from_module(__name__)
    linting(hits, linter)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return dumped, user, developer


def linting(hits, linter: protocol.Linter):
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        for page in hits:
            call = functools.partial(
                linter.add_finding,
                msgid=checker.msgid,
            )
            for hit in page.hits:
                checker(call, hit, page=page.page)


# TODO: ADD DIFFERENT BORDER CHECKER LINTER FOR DIFFRENT AREAS, footenote,
# pagecontent, cropbox, etc.

SOLUTION_2020 = """\
Objekt beschreibt Seitenrand

Passen Sie die Formatierung an, so dass der Inhalt nicht mehr in den
Seitenrad ragt.
"""


def check_2020_content_inside_box(linter, item, page):  # pylint:disable=W0613
    """Ensure that content fits in detected content box."""
    assert isinstance(page, int), type(page)
    _, bounding = item
    assert isinstance(bounding, tuple), type(bounding)
    location = iamraw.BoundingLocation.fromtuple(
        bounding=bounding,
        page=page,
    )
    linter(location=location)


class BorderExpected:

    def __init__(self, expected):
        self.expected = expected

    def __call__(self, page) -> tuple:
        with contextlib.suppress(KeyError):
            return self.expected[page]
        utila.error(f'no expected page size: {page}')
        return None


def boxes_outside_border(
        boxes,
        page_sizes: dict,
        expected: BorderExpected,
        tol=None,
) -> iamraw.PageContentHits:
    """Determine `boxes` which are outside out of `border`."""
    if tol is None:
        tol = (BORDER_LEFT, BORDER_RIGHT, BORDER_TOP, BORDER_BOTTOM)
    result = []

    # x0 y0 x1 y1
    for page in boxes:
        pagesize = page_sizes[page.page]
        border_box = expected(page.page)
        if not border_box:
            continue
        valid = utila.roundme((
            border_box[0] - tol[0],  # x0
            border_box[2] - tol[2],  # y0
            pagesize.width - border_box[1] + tol[1],  # x1
            pagesize.height - border_box[3] + tol[3],  # y1
        ))
        hits = []
        for index, bounding in page.boundings:
            # BOUNDING:     'left, top,   right, bottom'
            # move bounding to center of page to make approach more robust
            rounded_bounding = round_small(bounding)
            if utila.rectangle_inside(valid, rounded_bounding):
                # all items in the box
                continue
            if covers_complete_page(bounding, pagesize):
                continue
            if utila.rectangle_size(rounded_bounding) <= 50:  # TODO: HOLY VALUE
                # white space pdf printer errors
                # TODO: USE THIS INFORMATION FOR EXPERT LINTING
                continue
            hits.append((index, bounding))
        result.append(
            iamraw.PageContentHit(
                border=border_box,
                hits=hits,
                page=page.page,
            ))
    return result


def covers_complete_page(bounding: tuple, page) -> bool:
    """Bounding covers the complete page."""
    expected = (0, 0, page.width, page.height)
    return utila.nears(bounding, expected, diff=5.0)  # TODO: HOLY VALUE


def round_small(item: utila.Rectangle) -> utila.Rectangle:
    """Round border in direction to the center of the rectangle to get a
    `smaller` rectangle which fit in more parent rectangles."""
    # round to move coordinate in center direction of page
    rounding = [
        math.ceil,  # x0
        math.ceil,  # y0
        math.floor,  # x1
        math.floor,  # y1
    ]
    result = [method(item[index]) for index, method in enumerate(rounding)]
    # rounding to the middle can flip min and max. Therefore we have to
    # ensure x0/x1 and y0/y1 constraint.
    result = ensure_bounding(item)
    return tuple(result)


def ensure_bounding(item):
    """ensure x0/x1 and y0/y1 constraint."""
    result = (
        min(item[0], item[2]),
        min(item[1], item[3]),
        max(item[0], item[2]),
        max(item[1], item[3]),
    )
    return utila.roundme(result)
