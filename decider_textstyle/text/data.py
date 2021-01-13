# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import protocol
import serializeraw
import utila

import decider_textstyle


def load_driver(
        textstyle: str,
        headlines: str,
        text: str,
        textpositions: str,
        sizeandborders: str,
        headerfooter: str,
        fontheader: str,
        fontcontent: str,
        magiccontent: str,
        pages: tuple = None,
):
    expected = serializeraw.load_doctextstyle(textstyle)
    headlines = serializeraw.load_headlines(headlines, pages=pages)

    fontstore = serializeraw.create_fontstore(
        fontheader,
        fontcontent,
        pages=pages,
    )
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text=text,
        textpositions=textpositions,
        sizeandborderpath=sizeandborders,
        headerfooterpath=headerfooter,
        fontheader=fontheader,
        fontcontent=fontcontent,
        pages=pages,
    )

    if os.path.exists(magiccontent):
        magiccontent = serializeraw.load_types(magiccontent, pages=pages)
    else:
        utila.error('no magic content')
        magiccontent = []

    if not headlines:
        utila.error('no headlines given')
    if not navigators:
        utila.error('no navigators given')

    if navigators and headlines:
        # TODO: DO WE REALY REQUIRE HEADLINES?
        chunks = decider_textstyle.utils.text_chunks(
            headlines,
            navigators,
            magiccontent=magiccontent,
            sync=True,  # TODO: REMOVE?
            yieldnone=True,
        )
        data = protocol.driver(
            text_chunks=chunks,
            fontstore=fontstore,
            headlines=headlines,
            style=expected,
        )
        return data
    return None
