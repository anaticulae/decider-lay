# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider_textstyle.utils

SOLUTION_7540 = """\
Kapitel beginnt nicht auf neuer Seite

Das Kapitel „{{chapter}}“ beginnt nicht auf einer neuen Seite. Fügen \
Sie vor dem Kapitelstart einen Seitenumbruch ein.

{WORD}
Passen Sie dazu die **Formatvorlage der Überschriften** Level 1 an oder \
verwenden Sie einen **manuellen Seitenumbruch**.
{END}

* TODO: Article with explaination
{WORD}
* Formatvorlage anpassen
* Manueller Seitenumbruch
{END}
"""


def check_7540_chapter_on_new_page(linter: callable, driver):
    headlines = [
        headline for headline in utila.iflat(driver.headlines)
        if headline.level == 1
    ]
    for headline in headlines:
        start = utila.cstart(headline.container)
        if start == 0:  # pylint:disable=C2001
            # chapter starts at page begin
            # TODO: CHECK FOR HEADER OR PAGE NUMBER BEFORE HEADLINE? MAY
            # BE NOT ZERO?
            continue
        if headline.decoration is not None:
            # Chapter-X-Pattern is detected before headline start
            continue
        navigator = utila.select_page(
            driver.navigators,
            page=headline.page,
        )
        location = decider_textstyle.utils.box_fromrange(
            crange=headline.container,
            navigator=navigator,
        )
        linter(
            location=location,
            chapter=headline.title,
        )
