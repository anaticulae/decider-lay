# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import typing

import protocol
import utila

import decider_textstyle.headlines.data
import decider_textstyle.headlines.improve
import decider_textstyle.headlines.rules
import decider_textstyle.headlines.style


def work(
        textstyle: str,
        headlines: str,
        text: str,
        textpositions: str,
        fontheader: str,
        fontcontent: str,
        sizeandborders: str,
        headerfooter: str,
        pages: tuple = None,
) -> typing.Tuple[str, str]:
    data = decider_textstyle.headlines.data.load_driver(
        textstyle,
        headlines,
        fontheader,
        fontcontent,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        pages,
    )
    if not data.headlines:  # pylint:disable=E1101
        utila.error('no headlines given')
    if not data.navigators:  # pylint:disable=E1101
        utila.error('no navigators given')

    linter = protocol.from_modules([  # pylint:disable=E1101
        decider_textstyle.headlines.improve,
        decider_textstyle.headlines.rules,
        decider_textstyle.headlines.style,
    ])

    if data.navigators and data.headlines:  # pylint:disable=E1101
        linter.run(driver=data)
    else:
        utila.error('could not run --headlines linter')

    result = linter.result(unique=True)
    user, developer = protocol.dump_result(result)
    return user, developer
