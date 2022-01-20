# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import utila

import decider_textstyle.headlines.data
import decider_textstyle.headlines.improve
import decider_textstyle.headlines.rules
import decider_textstyle.headlines.style


def work(
    textstyle: str,
    headliner: str,
    textx: str,
    textpositions: str,
    fontheader: str,
    fontcontent: str,
    sizeandborders: str,
    headerfooter: str,
    pages: tuple = None,
) -> protocol.ResultType:
    driver = decider_textstyle.headlines.data.load_driver(
        textstyle,
        headliner,
        fontheader,
        fontcontent,
        textx,
        textpositions,
        sizeandborders,
        headerfooter,
        pages,
    )
    if not driver.headlines:  # pylint:disable=E1101
        utila.error('no headlines given')
    if not driver.navigators:  # pylint:disable=E1101
        utila.error('no navigators given')

    if not driver.navigators or not driver.headlines:  # pylint:disable=E1101
        utila.error('could not run --headlines linter')
        return protocol.RESULT_EMPTY

    user, developer = protocol.run(
        modulename=[
            decider_textstyle.headlines.improve,
            decider_textstyle.headlines.rules,
            decider_textstyle.headlines.style,
        ],
        driver=driver,
    )
    return user, developer
