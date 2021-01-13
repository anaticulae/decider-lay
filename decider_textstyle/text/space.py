# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw

SOLUTION_7770 = """\
Loch im Textbild erhalten

TODO:
"""


def maxwidth(height: float) -> float:  # pylint:disable=W0613
    return 25.0


def check_7770_text_hole_simple(linter: callable, driver):
    for page in driver.wordspaces:
        pagenumber, pagecontent = page.page, page.content
        for _, line in pagecontent:
            for space in line:
                width = space[2] - space[0]  # x1 - x0
                height = space[3] - space[1]  # y1 - y0
                if width <= maxwidth(height):
                    continue
                location = iamraw.BoundingLocation.fromtuple(
                    bounding=space,
                    page=pagenumber,
                )
                linter(location=location)


SOLUTION_7771 = """\
Zeile äußerst löcherig

TODO:
"""


def check_7771_text_hole_line(linter: callable, driver):  # pylint:disable=W0613
    pass
