# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import serializeraw


def load_driver(
        textstyle,
        headlines,
        fontheader,
        fontcontent,
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        pages,
):
    expected = serializeraw.load_doctextstyle(textstyle)
    headlines = serializeraw.load_headlines(headlines, pages=pages)

    fontstore = serializeraw.create_fontstore(
        fontheader,
        fontcontent,
        pages=pages,
    )
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textpositions,
        sizeandborders,
        headerfooter,
        fontheader,
        fontcontent,
        pages=pages,
    )

    data = protocol.driver(
        navigators=navigators,
        fontstore=fontstore,
        headlines=headlines,
        style=expected,
    )
    return data
