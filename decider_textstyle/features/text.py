# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os
import typing

import iamraw
import iamraw.fonts
import protocol
import serializeraw
import utila

import decider_textstyle.utils


def work(  # pylint:disable=R0913,R0914
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
) -> typing.Tuple[str, str]:
    linter = protocol.from_module(__name__)

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
        linter.run(driver=data)
    else:
        utila.error('could not run --text linter')

    result = linter.result(unique=True)

    result = decider_textstyle.utils.merge_lintings(result)

    user, developer = protocol.dump_result(result)
    return user, developer


SOLUTION_7550 = """\
Schriftgröße des Texts weicht ab

Die erkannte Schriftgröße **{{current}}** weicht von
der erwarteten Schriftgröße **{{expected}}**.
"""


def check_7550_check_text_size(linter: callable, driver):
    if not driver.style.text_size:
        return
    chunks = driver.text_chunks
    expected = driver.style.text_size
    for page, line, item in chunks:
        if not item:
            continue
        textsize = item.style.textsize()
        if textsize == expected:
            continue

        location = iamraw.RangedLocation(page=page, line=line)
        # TODO: CHECK FOR SINGLE CHAR OR WORDS TO BIG, BUT EXCLUDE HIGHNOTES
        linter(location=location, expected=expected, current=textsize)


SOLUTION_7551 = """\
Schriftart des Texts weicht ab

Die erkannte Schriftart **{{current}}** weicht von
der erwarteten Schriftart **{{expected}}** ab.
"""


def check_7551_check_text_family(linter: callable, driver):
    if not driver.style.text_family:
        return
    chunks = driver.text_chunks
    expected = driver.fontstore[driver.style.text_family]
    if not expected:
        return
    expected = expected.name
    for page, line, item in chunks:
        if not item:
            continue
        for style in item.style:
            if style.font == iamraw.NO_FONT:
                utila.error(f'no font for {page} {line} {item}')
                continue
            current = driver.fontstore[style.font].name
            if current == expected:
                continue
            location = iamraw.RangedLocation(
                page=page,
                line=line,
                token=style.start,
                token_end=style.end,
            )
            # TODO: CHECK FOR SINGLE CHAR OR WORDS TO BIG, BUT EXCLUDE HIGHNOTES
            linter(location=location, expected=expected, current=current)


SOLUTION_7555 = """\
Text: Unzulässige Markierung

Der Text weist unnötige Hervorhebungen auf. Es ist nicht nötig den Leser
durch typografische Veränderungen auf besonders `wichtige` Punkte
hinzuweisen. Dies erschwert den Lesefluss.

TODO: SIEHE ARTIKEL THEISSEN
"""


def check_7555_text_bold(linter: callable, driver):
    chunks = driver.text_chunks
    for page, line, item in chunks:
        if not item:
            continue
        for style in item.style:
            if style.font == iamraw.NO_FONT:
                utila.error(f'no font for {page} {line} {item}')
                continue
            current = driver.fontstore[style.font]
            if current.weight != iamraw.fonts.Weight.BOLD:
                # TODO: EXCLUDE TABLE HEADLINES ETC.
                continue
            location = iamraw.RangedLocation(
                page=page,
                line=line,
                token=style.start,
                token_end=style.end,
            )
            # TODO: CHECK FOR SINGLE CHAR OR WORDS TO BIG, BUT EXCLUDE HIGHNOTES
            linter(location=location)
