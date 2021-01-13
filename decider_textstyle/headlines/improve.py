# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import utila

import decider_textstyle.headlines.utils

# TODO: HOLY VALUE
HEADLINE_MIN_WIDTH_LENGTH = configo.HV_PERCENT_PLUS(70).value

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
    navigators = driver.navigators
    for headline in headlines:
        containers_ = decider_textstyle.headlines.utils.containers(
            headline.container)
        navigator = utila.select_page(navigators, headline.page)
        location = iamraw.RangedLocation(
            page=headline.page,
            line=containers_[0],
            line_end=containers_[-1],
        )
        if location.line == location.line_end:
            # single headline
            continue
        # TODO: SUPPORT ROTATED PAGES
        min_pagewidth = driver.style.page_width * HEADLINE_MIN_WIDTH_LENGTH
        text = navigator[location.line:location.line_end]
        width = [item.bounding[2] - item.bounding[0] for item in text]
        width = [item for item in width if item < min_pagewidth]
        if not width:
            # no width length error
            continue
        linter(
            location=location,
            chapter=headline.title,
        )
