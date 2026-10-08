# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import iamraw
import protoerror
import utilo

MORE_THAN = configos.HV_INT_PLUS(default=10)

SOLUTION_7550 = """\
Schriftgröße des Texts weicht ab

Die erkannte Schriftgröße **{{current}}** weicht von \
der erwarteten Schriftgröße **{{expected}}**.
"""


@protoerror.disable_perpage(morethan=MORE_THAN)
def check_7550_text_size(linter: callable, driver):
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

Die erkannte Schriftart **{{current}}** weicht von \
der erwarteten Schriftart **{{expected}}** ab.
"""


@protoerror.disable_perpage(morethan=MORE_THAN)
def check_7551_text_family(linter: callable, driver):
    if not driver.style.text_family:
        utilo.error('7551: no text family given - driver')
        return
    chunks = driver.text_chunks
    expected = driver.fontstore[driver.style.text_family]
    if not expected:
        utilo.error('7551: no text family given - fontstore')
        return
    expected = expected.name
    for page, line, item in chunks:
        if not item:
            continue
        for style in item.style:
            if style.font == iamraw.NO_FONT:
                utilo.error(f'no font for {page} {line} {item}')
                continue
            current = driver.fontstore[style.font].name
            if current == expected:
                continue
            current_text = item.text[style.start:style.end]
            if not current_text.strip():
                # TODO: INTRODUCE FLAG TO LINT WHITESPACE ALSO
                # only white spaces
                continue
            if 'math' in expected.lower():
                # TODO: SHRINK THIS SKIP TO FORMULAS AFTER IMPROVING
                # FORMULA COLLECTOR
                # math fonts seams to be always correct
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
Unzulässige Markierung

Der Text weist unnötige optische Auszeichnungen auf. Diese verändern den \
Grauwert des Texts und stören den Lesefluss. Es wird empfohlen \
ästhetische Auszeichnungen zu verwenden.

{darstellung/grauwert#text-grauwert}
{darstellung/grauwert#asthetische-auszeichnung}
"""


@protoerror.disable_perpage(morethan=MORE_THAN)
def check_7555_text_bold(linter: callable, driver):
    chunks = driver.text_chunks
    for page, line, item in chunks:
        if not item:
            continue
        for style in item.style:
            if style.font == iamraw.NO_FONT:
                utilo.error(f'no font for {page} {line} {item}')
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
