# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import serializeraw
import utila

import decider_textstyle.toc.split


def work(
    textx: str,
    textpositions: str,
    headerfooter: str,
    sizeborder: str,
    fontheader: str,
    fontcontent: str,
    tocx: str,
    pages: tuple = None,
) -> protocol.ResultType:
    if (pages := tocpages(toc=tocx, pages=pages)) is False:  # pylint:disable=compare-to-zero
        return protocol.RESULT_EMPTY
    tocx = serializeraw.load_toc(tocx)
    ptcns = serializeraw.ptcn_fromfile(
        text=textx,
        textpositions=textpositions,
        sizeandborder=sizeborder,
        headerfooter=headerfooter,
        fontheader=fontheader,
        fontcontent=fontcontent,
        pages=pages,
    )
    splitted = decider_textstyle.toc.split.split(  # pylint:disable=W0612
        toc=tocx,
        ptcns=ptcns,
    )
    return protocol.RESULT_EMPTY


def tocpages(toc: str, pages: str):
    if not utila.exists(toc):
        utila.error(f'missing {toc}, skip decider_textstyle --toc')
        return False
    toc = serializeraw.load_toc(toc)
    if not toc:
        return False
    toc: list = utila.flat(toc)
    toc_pages = utila.make_unique(item.raw_location for item in toc)
    result = tuple(item for item in toc_pages if not utila.should_skip(
        page=item,
        pages=pages,
    ))
    return result
