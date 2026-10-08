# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror
import utilo

import decider_textstyle.text.data
import decider_textstyle.text.space
import decider_textstyle.text.style


def work(  # pylint:disable=R0913,R0914
    textstyle: str,
    headliner: str,
    textx: str,
    textpositions: str,
    sizeandborders: str,
    headerfooter: str,
    fontheader: str,
    fontcontent: str,
    wordspaces: str,
    magiccontent: str,
    pages: tuple = None,
) -> protoerror.ResultType:
    driver = decider_textstyle.text.data.load_driver(
        textstyle,
        headliner,
        textx,
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
        utilo.error('could not run --text linter')
        return protoerror.RESULT_EMPTY
    user, developer = protoerror.run(
        modulename=[
            decider_textstyle.text.space,
            decider_textstyle.text.style,
        ],
        driver=driver,
    )
    return user, developer
