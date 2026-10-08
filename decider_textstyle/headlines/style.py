# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import string

import configos
import configos.holyvalue.access
import doctextstyle.parser
import iamraw
import protoerror
import utilo

import decider_textstyle.headlines.utils

FONT_SIZE_ERROR = string.Template("""\
$headline falsch formatiert

Die Schriftgröße **{{current}}** der $headline „{{title}}“ weicht von der \
erwarteten Schriftgröße **{{expected}}** ab.
""")

FONT_FAMILY_ERROR = string.Template("""\
$headline falsch formatiert

Die Schriftart **{{current}}** der $headline „{{title}}“ weicht von der \
erwarteten Schriftart **{{expected}}** ab.
""")

FONT_DIST_BEFORE_ERROR = string.Template("""\
$headline falsch formatiert

Der Abstand **{{current}}** vor der $headline „{{title}}“ weicht vom \
erwarteten Abstand **{{expected}}** ab.
""")

FONT_DIST_AFTER_ERROR = string.Template("""\
$headline falsch formatiert

Der Abstand **{{current}}** nach der $headline „{{title}}“ weicht vom \
erwarteten Abstand **{{expected}}** ab.
""")

HEADLINE_DIFF_REL_MAX = configos.HV_PERCENT_PLUS(default=10)

HEADLINE_DIFF_ABS_MAX = configos.HolyTable(
    items=[
        (8, 0.5),
        (12, 1.0),
        (20, 2.5),
        (25, 5),
        (50, 5),
    ],
    strategy=utilo.Strategy.LINEARISE,
)

WHITESPACE_LINTING = configos.holyvalue.access.HV_BOOL(default=False)

LEVEL_1 = 1

SOLUTION_7500 = FONT_SIZE_ERROR.substitute(headline='Hauptüberschrift')


def check_7500_check_h1_font_size(linter: callable, driver):
    # TODO: HANDLE HIGH NOTES CORRECLTY
    if not driver.style.h1_size:
        return
    validate_headline_size(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_1,
        driver.style.h1_size,
    )


SOLUTION_7501 = FONT_FAMILY_ERROR.substitute(headline='Hauptüberschrift')


def check_7501_check_h1_font_family(linter: callable, driver):
    if not driver.style.h1_family:
        return
    validate_headlines_family(
        linter,
        driver.navigators,
        driver.fontstore,
        driver.headlines,
        LEVEL_1,
        driver.style.h1_family,
    )


SOLUTION_7502 = FONT_DIST_BEFORE_ERROR.substitute(headline='Hauptüberschrift')


def check_7502_check_h1_distance_before(linter: callable, driver):
    if not driver.style.h1_before:
        return
    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_1,
        driver.style.h1_before,
        check_before=True,
    )


SOLUTION_7503 = FONT_DIST_AFTER_ERROR.substitute(headline='Hauptüberschrift')


def check_7503_check_h1_distance_after(linter: callable, driver):
    if not driver.style.h1_after:
        return
    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_1,
        driver.style.h1_after,
        check_before=False,
    )


LEVEL_2 = 2

SOLUTION_7510 = FONT_SIZE_ERROR.substitute(headline='Teilüberschrift')


def check_7510_check_h2_font_size(linter: callable, driver):
    # TODO: HANDLE HIGH NOTES CORRECTLY
    if not driver.style.h2_size:
        return
    validate_headline_size(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_2,
        driver.style.h2_size,
    )


SOLUTION_7511 = FONT_FAMILY_ERROR.substitute(headline='Teilüberschrift')


def check_7511_check_h2_font_family(linter: callable, driver):
    if not driver.style.h2_family:
        return
    validate_headlines_family(
        linter,
        driver.navigators,
        driver.fontstore,
        driver.headlines,
        LEVEL_2,
        driver.style.h2_family,
    )


SOLUTION_7512 = FONT_DIST_BEFORE_ERROR.substitute(headline='Teilüberschrift')


def check_7512_check_h2_distance_before(linter: callable, driver):
    if not driver.style.h2_before:
        return
    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_2,
        driver.style.h2_before,
        check_before=True,
    )


SOLUTION_7513 = FONT_DIST_AFTER_ERROR.substitute(headline='Teilüberschrift')


def check_7513_check_h2_distance_after(linter: callable, driver):
    if not driver.style.h2_after:
        return
    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_2,
        driver.style.h2_after,
        check_before=False,
    )


LEVEL_3 = 3

SOLUTION_7520 = FONT_SIZE_ERROR.substitute(headline='Unterüberschrift')


def check_7520_check_h3_font_size(linter: callable, driver):
    # TODO: HANDLE HIGH NOTES CORRECLTY
    if not driver.style.h3_size:
        return
    validate_headline_size(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_3,
        driver.style.h3_size,
    )


SOLUTION_7521 = FONT_FAMILY_ERROR.substitute(headline='Unterüberschrift')


def check_7521_check_h3_font_family(linter: callable, driver):
    if not driver.style.h3_family:
        return
    validate_headlines_family(
        linter,
        driver.navigators,
        driver.fontstore,
        driver.headlines,
        LEVEL_3,
        driver.style.h3_family,
    )


SOLUTION_7522 = FONT_DIST_BEFORE_ERROR.substitute(headline='Unterüberschrift')


def check_7522_check_h3_distance_before(linter: callable, driver):
    if not driver.style.h3_before:
        return
    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_3,
        driver.style.h3_before,
        check_before=True,
    )


SOLUTION_7523 = FONT_DIST_AFTER_ERROR.substitute(headline='Unterüberschrift')


def check_7523_check_h3_distance_after(linter: callable, driver):
    if not driver.style.h3_after:
        return
    validate_headline_distance(
        linter,
        driver.navigators,
        driver.headlines,
        LEVEL_3,
        driver.style.h3_after,
        check_before=False,
    )


H1_FONT_SIZE_MAX = configos.HV_FLOAT_PLUS(default=48.0)

H2_FONT_SIZE_MAX = configos.HV_FLOAT_PLUS(default=30.0)

SOLUTION_7535 = """\
Erwartete Schriftgröße der Kapitel zu groß

Die erwartete Schriftgröße der Kapitel {{current}}pt überschreitet die \
maximal empfohlene Schriftgröße von {{max_font_size}}pt.

TODO: ADD ARTICLE
"""


def check_7535_headline_h1_too_huge(linter: callable, driver):
    style: iamraw.DocTextStyle = driver.style
    if style.h1_size is None:
        return
    if style.h1_size <= H1_FONT_SIZE_MAX:
        return
    linter(
        location=protoerror.OVERVIEW,
        current=style.h1_size,
        max_font_size=H1_FONT_SIZE_MAX,
    )


SOLUTION_7536 = """\
Erwartete Schriftgröße der Abschnitte zu groß

Die erwartete Schriftgröße der Abschnitte {{current}}pt überschreitet \
die maximal empfohlene Schriftgröße von {{max_font_size}}pt.

TODO: ADD ARTICLE
"""


def check_7536_headline_h2_too_huge(linter: callable, driver):
    style: iamraw.DocTextStyle = driver.style
    if style.h2_size is None:
        return
    if style.h2_size <= H2_FONT_SIZE_MAX:
        return
    linter(
        location=protoerror.OVERVIEW,
        current=style.h2_size,
        max_font_size=H2_FONT_SIZE_MAX,
    )


def validate_headline_size(
    linter,
    navigators,
    headlines,
    level,
    expected_size,
):
    flats = utilo.flat(headlines)
    headlines = [item for item in flats if item.level == level]
    for headline in headlines:
        containero = utilo.crange(headline.container)
        navigator = utilo.select_page(navigators, headline.page)
        try:
            lines_selected = [navigator[index] for index in containero]
        except IndexError:
            msg = f'headline size: {containero} out of bounds on page: {navigator.page}'
            utilo.error(msg)
            continue
        textsizes_ = decider_textstyle.headlines.utils.container_textsizes(
            lines_selected)
        maxdiff = HEADLINE_DIFF_ABS_MAX(expected_size)
        if all((utilo.near(item, expected_size, diff=maxdiff)
                for item in textsizes_)):
            continue
        # font size diff
        location = iamraw.RangedLocation(
            page=headline.page,
            line=containero[0],
            line_end=containero[-1],
        )
        linter(
            title=headline.title,
            location=location,
            expected=expected_size,
            current=', '.join([f'{item}' for item in textsizes_]),
        )


def validate_headlines_family(
    linter,
    navigators,
    fontstore,
    headlines,
    level,
    expected_family,
):
    flats = utilo.flat(headlines)
    headlines = [item for item in flats if item.level == level]
    if not fontstore[expected_family]:
        utilo.error(f'no expected headline family: {expected_family}')
        return
    expected_family = fontstore[expected_family].name
    for headline in headlines:
        finding = validate_headline_family(
            headline,
            navigators,
            fontstore,
            expected_family,
        )
        if not finding:
            continue
        font, position = finding
        linter(
            title=headline.title,
            location=decider_textstyle.headlines.utils.headline_location(
                headline,
                position,
            ),
            expected=expected_family,
            current=font,
        )


def validate_headline_family(headline, navigators, fontstore, expected_family):  # pylint:disable=R0914
    containero = utilo.crange(headline.container)
    navigator = utilo.select_page(navigators, headline.page)
    try:
        lines_selected = [navigator[index] for index in containero]
    except IndexError:
        msg = f'headline family: {containero} out of bounds on page: {navigator.page}'
        utilo.error(msg)
        return None
    textfamily_ = []
    skip_whitespaces = not WHITESPACE_LINTING
    analyzed = decider_textstyle.headlines.utils.container_textfamily(
        lines_selected,
        skip_whitespaces=skip_whitespaces,
    )
    for item in analyzed[0]:
        headline_family = fontstore[item]
        if headline_family:
            textfamily_.append(headline_family.name)
        else:
            utilo.error(f'headline: font not found {item}')
    matched = [item == expected_family for item in textfamily_]
    if all(matched):
        return None
    # select invalid text families
    positions = [
        position for position, valid in zip(analyzed[1], matched) if not valid
    ]
    textfamilies = [item for item in textfamily_ if item != expected_family]
    # font family diff
    current = utilo.from_tuple(textfamilies, ', ')
    return current, positions


def validate_headline_distance(  # pylint:disable=R1260
    linter,
    navigators,
    headlines,
    level,
    expected_distance,
    check_before: bool = True,
):
    flats = utilo.flat(headlines)
    headlines = [item for item in flats if item.level == level]
    for headline in headlines:
        containero = utilo.crange(headline.container)
        navigator = utilo.select_page(navigators, headline.page)
        distances = doctextstyle.parser.textdistances(navigator)
        if check_before:
            # TODO: SOLVE THIS ISSUE
            try:
                before = distances[containero[0]][0]
            except IndexError:
                utilo.error(f'validate headline distance: {containero} '
                            f'before out of bounds {len(distances)}')
                continue
            if before is None:
                continue
            if utilo.pnear(
                    expected_distance,
                    before,
                    abs_tol=HEADLINE_DIFF_ABS_MAX(expected_distance),
                    rel_tol=HEADLINE_DIFF_REL_MAX,
            ):
                continue
            if before > 100.0:
                utilo.error(f'distance to high: {before}, use table etc.')
                # TODO: USE FIGURES, TABLES ETC.
                continue
        else:
            # TODO: SOLVE THIS ISSUE
            try:
                after = distances[containero[-1]][1]
            except IndexError:
                utilo.error(f'validate headline distance: {containero} '
                            f'after out of bounds {len(distances)}')
                continue
            if after is None:
                continue
            if utilo.pnear(
                    expected_distance,
                    after,
                    abs_tol=HEADLINE_DIFF_ABS_MAX(expected_distance),
                    rel_tol=HEADLINE_DIFF_REL_MAX,
            ):
                continue
            if after > 100.0:
                utilo.error(f'distance to high: {after}, use table etc.')
                # TODO: USE FIGURES, TABLES ETC.
                continue
        # distance diff
        location = iamraw.RangedLocation(
            page=headline.page,
            line=containero[0],
            line_end=containero[-1],
        )
        linter(
            title=headline.title,
            location=location,
            expected=expected_distance,
            current=before if check_before else after,
        )
