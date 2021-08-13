# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections

import configo
import iamraw
import protocol
import utila

VALID_AREA = {
    None,
    iamraw.PageContentType.BLOCKQUOTE,
    iamraw.PageContentType.TEXT,
}

SOLUTION_7770 = """\
Loch im Textbild erhalten

Fügen Sie Trennungen ein um das Schriftbild zu verbessern.
"""


@protocol.disable_perpage(morethan=10)  # TODO HOLY VALUE
def check_7770_text_hole_simple(linter: callable, driver):
    skipper = driver.magiccontent_oneline
    for page in driver.wordspaces:
        pagenumber, pagecontent = page.page, page.content
        for linenumber, line in pagecontent:
            typ = skipper(pagenumber, linenumber)
            if typ not in VALID_AREA:
                # skip hole checker in captions and formula
                continue
            for space in line:
                width = utila.rectangle_width(space)
                height = utila.rectangle_height(space)
                if width <= MAXWIDTH(height):
                    continue
                location = iamraw.BoundingLocation.fromtuple(
                    bounding=space,
                    page=pagenumber,
                    line=linenumber,
                )
                linter(location=location)


MAXWIDTH = configo.HolyTable(  # TODO: ADJUST LATER
    items=[
        (0, 15.0),
        (9, 15.0),
        (12, 25.0),
        (30, 35.0),
    ],
    strategy=utila.Strategy.LOWER,
    left_outranges_none=False,
    right_outranges_none=False,
)

SOLUTION_7771 = """\
Zeile äußerst löcherig

Fügen Sie eine Trennung ein um das Schriftbild zu verbessern.
"""


def check_7771_text_hole_line(linter: callable, driver):  # pylint:disable=W0613
    # TODO: REWORK THIS AS DECORATOR OR SPECIAL METHOD
    baselinter = linter.func.__self__  # DIRTY

    todo = []

    def unite_text_hole(items):
        unite, result = utila.partition(
            items=items,
            key=lambda x: x.msgid == 7770,
        )
        pagegroup = groupby_x(unite, selector=lambda x: x.location.page)
        for page, content in pagegroup.items():
            linegroup = groupby_x(content, selector=lambda x: x.location.line)
            for line, linecontent in linegroup.items():
                if len(linecontent) <= 2:
                    # nothing todo, its a single or double hole
                    result.extend(linecontent)
                    continue
                todo.append((page, line, linecontent))
        return result

    baselinter.check_findings(unite_text_hole)
    for page, line, items in todo:
        boundings = utila.flatten([item.location.value for item in items])
        location = iamraw.BoundingLocation.fromtuple(
            bounding=tuple(boundings),
            page=page,
            line=line,
        )
        linter(location=location)


def groupby_x(items, selector) -> dict:
    # TODO: MOVE TO UTILA
    collected = collections.defaultdict(list)
    for item in items:
        collected[selector(item)].append(item)
    result = dict(collected)
    return result
