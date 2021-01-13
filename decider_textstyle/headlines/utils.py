# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import iamraw
import texmex
import utila


def container_start(item):
    with contextlib.suppress(TypeError):
        return item[0]
    return item


def containers(item) -> tuple:
    with contextlib.suppress(TypeError):
        return tuple(range(item[0], item[1] + 1))
    return (item,)


def container_textsizes(items):
    result = []
    for item in items:
        sizes = textsizes(item.style)
        result.extend(sizes)
    result = sorted(result)
    return result


def container_textfamily(items, skip_whitespaces: bool = True):
    families, positions = [], []
    for item in items:
        family, position = textfamily(item, skip_whitespaces=skip_whitespaces)
        families.extend(family)
        positions.extend(position)
    return families, positions


def textsizes(style: texmex.TextInfo) -> utila.Floats:
    sizes = [item.size for item in style.content]
    sizes = utila.make_unique(sizes)
    result = sorted(sizes)
    return result


def textfamily(
        item: texmex.TextInfo,
        skip_whitespaces: bool = True,
) -> utila.Ints:
    fonts = []
    positions = []
    for style in item.style.content:
        if skip_whitespaces:
            # do not lint the font of white spaces. Use this linting only
            # for expert linting, if you want to inform about failure in
            # using words or orther style mechanism.
            if not item.text[style.start:style.end].strip():
                continue
        fonts.append(style.font)
        positions.append((style.start, style.end))
    if len(utila.make_unique(fonts)) == 1:
        fonts = utila.make_unique(fonts)
        positions = [(0, len(item.text))]
    return fonts, positions


def headline_location(headline, chars: list = None) -> iamraw.RangedLocation:
    containers_ = containers(headline.container)
    # TODO: REPLACE TOKEN WITH CHAR
    location = iamraw.RangedLocation(
        page=headline.page,
        line=containers_[0],
        line_end=containers_[-1],
    )
    if chars:
        location.token = chars[0][0]
        location.token_end = chars[0][1]
    return location
