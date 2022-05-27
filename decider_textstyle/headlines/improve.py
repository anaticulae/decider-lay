# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import utila

import decider_textstyle.utils

HEADLINE_WIDTH_LENGTH_MIN = configo.HV_PERCENT_PLUS(default=70)

SOLUTION_7560 = """\
Korrigiere Überschrift

Teilen Sie die Überschrift um ein besseres Layout zu erreichen.
"""


def check_7560_split_headline(linter: callable, driver):
    # TODO: CHANGE TYPE FROM ERROR TO STLYE HINT?
    if not driver.style:
        utila.error('improve: require document style; skip')
        return
    headlines = utila.flatten(driver.headlines)
    for headline in headlines:
        containero = utila.crange(headline.container)
        if len(containero) == 1:
            # single headline
            continue
        navigator = utila.select_page(driver.navigators, headline.page)
        # TODO: SUPPORT ROTATED PAGES
        min_pagewidth = driver.style.page_width * HEADLINE_WIDTH_LENGTH_MIN
        text = navigator[containero[0]:containero[-1]]
        width = [utila.rect_width(item.bounding) for item in text]
        width = [item for item in width if item < min_pagewidth]
        if not width:
            # no width length error
            continue
        location = decider_textstyle.utils.box_fromheadline(
            headline,
            driver.navigators,
        )
        linter(
            location=location,
            chapter=headline.title,
        )
