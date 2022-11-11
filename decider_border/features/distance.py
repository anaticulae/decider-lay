# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
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

import math

import configo
import groupme.feature.distance
import iamraw
import protocol
import utila

DISTANCE_BEFORE_MN = configo.HV_FLOAT_PLUS(default=10.0)

DISTANCE_AFTER_MIN = configo.HV_FLOAT_PLUS(default=10.0)


def work(
    area: str,
    xdistances: str,
    pages: tuple = None,
) -> tuple[str, str]:
    driver = create_driver(
        area=area,
        distances=xdistances,
        pages=pages,
    )
    user, developer = protocol.run(modulename=__name__, driver=driver)
    return user, developer


def create_driver(area, distances, pages):
    area = groupme.feature.area.load_area(area, pages=pages)
    distances = groupme.feature.distance.load_distance(distances, pages=pages)
    result = protocol.driver(
        area=area,
        distances=distances,
    )
    return result


SOLUTION_3030 = """\
Abstand vor dem Objekt zu gering

Der Abstand nach dem Text und vor dem Objekt ist zu gering.

Erkannter Abstand: {{distance}}
Mindestabstand: {{min_distance}}

# IF WORD
# TODO: SHOW DISTANCE AND MINDISTANCE
# IF LATEX
"""


def check_3030_text_before_to_near(linter, driver):
    for page in driver.distances:
        area = utila.select_page(driver.area, page.page)
        bounds = utila.flat(list(area.border.values()))
        for item, bounding in zip(page.content, bounds):
            location = iamraw.BoundingLocation.fromtuple(
                bounding=bounding,
                page=page.page,
            )
            if item.before is None:
                # page starts with object, no text before object
                continue
            if math.fabs(item.before) > DISTANCE_BEFORE_MN:
                continue
            linter(
                location=location,
                distance=item.before,
                min_distance=DISTANCE_AFTER_MIN,
            )


SOLUTION_3031 = """\
Abstand nach dem Objekt zu gering

Der Abstand nach dem Objekt und vor dem Text ist zu gering.

Erkannter Abstand: {{distance}}
Mindestabstand: {{min_distance}}
"""


def check_3031_text_after_to_near(linter, driver):
    for page in driver.distances:
        area = utila.select_page(driver.area, page.page)
        bounds = utila.flat(list(area.border.values()))
        for item, bounding in zip(page.content, bounds):
            location = iamraw.BoundingLocation.fromtuple(
                bounding=bounding,
                page=page.page,
            )
            if item.after is None:
                # page ends with object, no text after object
                continue
            if math.fabs(item.after) > DISTANCE_AFTER_MIN:
                continue
            linter(
                location=location,
                distance=item.after,
                min_distance=DISTANCE_AFTER_MIN,
            )
