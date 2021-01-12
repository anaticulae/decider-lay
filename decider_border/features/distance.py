# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Distance Linter
===============

Inform user about to few or to much distance between textual and non
textual ojects(table, images, diagrams).

# TODO: SUPPORT DIFFERENT EDITORS(word/latex)
# TODO: EXTEND MESSAGE WITH TABELLE, BILD, FORMEL etc.
"""

import functools
import math
import typing

import configo
import groupme.feature.distance
import iamraw
import protocol
import utila

MIN_DISTANCE_BEFORE = configo.HV_FLOAT_PLUS(10.0)
MIN_DISTANCE_AFTER = configo.HV_FLOAT_PLUS(10.0)


def work(
        area: str,
        distances: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    area = groupme.feature.area.load_area(area, pages=pages)
    distances = groupme.feature.distance.load_distance(distances, pages=pages)

    linter = protocol.from_module(__name__)
    linting(area, distances, linter)

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer


def linting(areas, distances, linter: protocol.Linter):
    checkers = protocol.parse_checkers(__name__)
    for checker in checkers:
        for page in distances:
            area = utila.select_page(areas, page.page)
            bounds = utila.flatten([item for item in area.border.values()])
            call = functools.partial(
                linter.add_finding,
                msgid=checker.msgid,
            )
            for item, bound in zip(page.content, bounds):
                checker(call, item, bound, page=page.page)


SOLUTION_3030 = """\
Abstand vor dem Object zu gering

Der Abstand nach dem Text und vor dem Objekt ist zu gering.

Erkannter Abstand: {{distance}}
Mindestabstand: {{min_distance}}

# IF WORD
# TODO: SHOW DISTANCE AND MINDISTANCE
# IF LATEX
"""


def check_3030_text_before_to_near(linter, item, bound, page):  # pylint:disable=W0613
    assert isinstance(page, int), type(page)
    location = iamraw.BoundingLocation.fromtuple(
        bounding=bound,
        page=page,
    )
    if item.before is None:
        # page starts with object, no text before object
        return
    if math.fabs(item.before) <= MIN_DISTANCE_BEFORE:
        linter(
            location=location,
            distance=item.before,
            min_distance=MIN_DISTANCE_AFTER.value,
        )


SOLUTION_3031 = """\
Abstand nach dem Objekt zu gering

Der Abstand nach dem Objekt und vor dem Text ist zu gering.

Erkannter Abstand: {{distance}}
Mindestabstand: {{min_distance}}
"""


def check_3031_text_after_to_near(linter, item, bound, page):  # pylint:disable=W0613
    assert isinstance(page, int), type(page)
    location = iamraw.BoundingLocation.fromtuple(
        bounding=bound,
        page=page,
    )
    if item.after is None:
        # page ends with object, no text after object
        return
    if math.fabs(item.after) <= MIN_DISTANCE_AFTER:
        linter(
            location=location,
            distance=item.after,
            min_distance=MIN_DISTANCE_AFTER.value,
        )
