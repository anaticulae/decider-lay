# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import operator

import iamraw
import texmex.style
import utila

import decider_textstyle.headlines.utils as dthu


def text_chunks(  # pylint:disable=R0912,R0914,R1260,W0613
        headlines,
        navigators,
        magiccontent: list = None,
        sync: bool = False,
        yieldnone: bool = False,
        magicvalid=None,
) -> list:
    """\
    yieldnone yield none-TextInfo-elements with None
    """
    if not magicvalid:
        magicvalid = [iamraw.PageContentType.TEXT]
    magiccontent = magiccontent if magiccontent else []
    # TODO: SO BAD
    headlines = utila.flatten(headlines)

    visited = utila.Single()

    flat = []
    for headline in headlines:
        # mark contaienr id as visited
        for container in dthu.containers(headline.container):
            visited.contains((headline.page, container))
        position = (
            headline.page,
            dthu.container_start(headline.container),
        )
        flat.append((*position, headline))

    for magicpage in magiccontent:
        for line, content in magicpage.content:
            location = (magicpage.page, line)
            if visited.contains(location):
                continue
            if content in magicvalid:
                # Do not skip valid magic content, Text for example
                continue
            flat.append((*location, None))

    for navigator in navigators:
        for index, line in enumerate(navigator):
            location = (navigator.page, index)
            if visited.contains(location):
                continue
            flat.append((*location, line))

    # sort by page and line
    flat = sorted(flat, key=operator.itemgetter(0, 1))

    if sync:
        # TODO: WHY SHOULD WE DO THIS?
        # TODO: ADD DOCU HERE
        while flat and not isinstance(flat[0][2], iamraw.Headline):
            # sync to first headline
            flat = flat[1:]

    if yieldnone:
        flat = [
            item if isinstance(item[2], texmex.style.TextInfo) else
            (item[0], item[1], None) for item in flat
        ]
    return flat
