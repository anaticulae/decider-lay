# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import protocol
import utila

SKIP = {
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
            if typ not in SKIP:
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

TODO:
"""


def check_7771_text_hole_line(linter: callable, driver):  # pylint:disable=W0613
    pass
