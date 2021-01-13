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
import protocol
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


def page_chunks(items):
    if not items:
        return []
    result = []
    page = None
    for item in items:
        if item[0] != page:
            result.append([item[0], [item[2]]])
            page = item[0]
        else:
            result[-1][1].append(item[2])
    return result


def merge_lintings(items):
    """Merge lintings which are neighbors and lint the same error.

    1. Group by page
    2. Group by message id
    3. Merge equal neighbors
    """
    ranged, notranged = utila.partition(
        key=lambda x: x.location.shortcut == 'r',
        items=items,
    )
    result = []
    result.extend(notranged)

    paged = protocol.bypage(ranged)
    for page in paged:
        msgid = protocol.byid(page)
        for messagegroup in msgid.values():
            merged = merge_equal_finding_id(messagegroup)
            result.extend(merged)
    return result


def merge_equal_finding_id(findings):
    if not findings:
        return []
    findings = sorted(findings, key=lambda x: x.location.line)
    result = [findings[0]]
    for item in findings[1:]:
        before = result[-1]
        linebefore = before.location.line
        if before.location.line_end is not None:
            linebefore = before.location.line_end
        if item.msgid != before.msgid:
            result.append(item)
            continue
        if item.solution.description != before.solution.description:
            result.append(item)
            continue
        if item.location.line != linebefore + 1:
            result.append(item)
            continue
        before.location.line_end = linebefore + 1
    # update finding number
    for finding in result:
        finding.number = protocol.finding.hash_finding(finding)
    return result
