# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import utila

import decider_textstyle.text.data
import decider_textstyle.text.space
import decider_textstyle.text.style


def work(  # pylint:disable=R0913,R0914
        textstyle: str,
        headlines: str,
        text: str,
        textpositions: str,
        sizeandborders: str,
        headerfooter: str,
        fontheader: str,
        fontcontent: str,
        wordspaces: str,
        magiccontent: str,
        pages: tuple = None,
) -> protocol.ResultType:
    driver = decider_textstyle.text.data.load_driver(
        textstyle,
        headlines,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        fontheader,
        fontcontent,
        wordspaces,
        magiccontent,
        pages=pages,
    )
    if not driver:
        utila.error('could not run --text linter')
        return protocol.RESULT_EMPTY
    user, developer = protocol.run(
        modulename=[
            decider_textstyle.text.space,
            decider_textstyle.text.style,
        ],
        driver=driver,
    )
    return user, developer
