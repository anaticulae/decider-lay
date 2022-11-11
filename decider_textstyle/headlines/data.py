# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import serializeraw
import utila


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
    if headlines:
        for group in headlines.groups:
            for headline in group.headlines:
                if headline.page == -1:
                    utila.error(f'remove invalid headline: {headline}')
            # remove none page adjusted headlines
            group.headlines = [
                item for item in group.headlines if item.page >= 0
            ]
    fontstore = serializeraw.create_fontstore(
        fontheader,
        fontcontent,
        pages=pages,
    )
    navigators = serializeraw.ptcn_fromfile(
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
