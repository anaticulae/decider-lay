# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror
import serializeraw

import decider_textstyle.text.fonts


def work(
    textstyle: str,
    worddist: str,
    chardist: str,
) -> protoerror.ResultType:
    textstyle = serializeraw.load_doctextstyle(textstyle)
    worddist = serializeraw.load_document_worddist(worddist)
    chardist = serializeraw.load_document_chardist(chardist)
    driver = protoerror.driver(
        textstyle=textstyle,
        worddist=worddist,
        chardist=chardist,
    )
    user, developer = protoerror.run(
        modulename=[
            decider_textstyle.text.fonts,
        ],
        driver=driver,
    )
    return user, developer
