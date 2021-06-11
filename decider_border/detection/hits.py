# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import iamraw
import utila

# TODO: HOLY VALUE, ADJUST THIS HOLY VALUES
BORDER_LEFT = 25
BORDER_RIGHT = 25
BORDER_TOP = 25
BORDER_BOTTOM = 25


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
    pagesizes: dict,
    expected: BorderExpected,
    tol=None,
) -> iamraw.PageContentHits:
    """Determine `boxes` which are outside out of `border`."""
    result = []
    # x0 y0 x1 y1
    for page in boxes:
        pagesize = pagesizes[page.page]
        borderbox = expected(page.page)
        if not borderbox:
            continue
        contentbox = contentbox_valid(borderbox, pagesize, tol=tol)
        hits = []
        for index, bounding in page.boundings:
            if contentbox_inside(bounding, contentbox, pagesize):
                continue
            hits.append((index, bounding))
        result.append(
            iamraw.PageContentHit(
                border=borderbox,
                hits=hits,
                page=page.page,
            ))
    return result


def boxes_repeating(
    pagecontenthits: iamraw.PageContentHits,
    required_ratio: float = 0.6,
) -> set:
    count_min = int(len(pagecontenthits) * required_ratio)
    collected = []
    for page in pagecontenthits:
        collected.extend(utila.make_unique([item[1] for item in page.hits]))
    clustered = utila.same_area_cluster(
        collected,
        max_difference=2.5,
        selector=lambda x: x,
    )
    result = {
        cluster.center for cluster in clustered if len(cluster) >= count_min
    }
    return result


def hits_unique(
    pagecontenthits: iamraw.PageContentHits,
    repeating: set,
) -> iamraw.PageContentHits:
    """Remove `repeating` hits."""
    result = []
    for page in pagecontenthits:
        selected = [
            hit for hit in page.hits if not hits_match(hit[1], repeating)
        ]
        result.append(
            iamraw.PageContentHit(
                border=page.border,
                hits=selected,
                page=page.page,
            ))
    return result


def hits_match(
        bounding: tuple,
        hits: set,
        maxdiff: float = 10.0,  # TODO: HOLY VALUE
) -> bool:
    return any([utila.nears(bounding, item, diff=maxdiff) for item in hits])


def contentbox_valid(border_box, pagesize, tol=None) -> tuple:
    if tol is None:
        tol = (BORDER_LEFT, BORDER_RIGHT, BORDER_TOP, BORDER_BOTTOM)
    valid = utila.roundme((
        border_box[0] - tol[0],  # x0
        border_box[2] - tol[2],  # y0
        pagesize.width - border_box[1] + tol[1],  # x1
        pagesize.height - border_box[3] + tol[3],  # y1
    ))
    return valid


def contentbox_inside(bounding, contentbox, pagesize) -> bool:
    # BOUNDING:     'left, top,   right, bottom'
    # move bounding to center of page to make approach more robust
    rounded_bounding = utila.rectangle_roundsmall(bounding)
    if utila.rectangle_inside(contentbox, rounded_bounding):
        # all items in the box
        return True
    if covers_completepage(bounding, pagesize):
        return True
    if utila.rectangle_size(rounded_bounding) <= 50:  # TODO: HOLY VALUE
        # white space pdf printer errors
        # TODO: USE THIS INFORMATION FOR EXPERT LINTING
        return True
    return False


def covers_completepage(bounding: tuple, page) -> bool:
    """Bounding covers the complete page."""
    expected = (0, 0, page.width, page.height)
    return utila.nears(bounding, expected, diff=5.0)  # TODO: HOLY VALUE
