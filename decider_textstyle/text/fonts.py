# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import utila

SOLUTION_7580 = """\
Standardschriftgröße anpassen

Bitte anpassen
"""


def check_7580_general_text_size(linter: callable, driver):  # pylint:disable=W0613
    pass


SOLUTION_7581 = """\
Zeilenabstand anpassen

Der Zeilenabstand **{{distance}}pt/{{percent}}%** der Standardschrift \
unterscheidet sich vom idealen Zeilenabstand von 100-150%.

{darstellung/schriftbild#zeilenabstand}
"""

# text distance between 100 and 150 percent is a good choice
TEXT_DISTANCE_VALID_MIN = configo.HV_PERCENT_PLUS(default=100.0)

TEXT_DISTANCE_VALID_MAX = configo.HV_PERCENT_PLUS(default=150.0)


def check_7581_general_text_distance(linter: callable, driver):
    textsize = driver.textstyle.text_size
    current_distance = driver.textstyle.text_distance
    percent = current_distance / textsize
    inside = utila.isinside(
        value=percent,
        left=TEXT_DISTANCE_VALID_MIN,
        right=TEXT_DISTANCE_VALID_MAX,
    )
    if inside:
        return
    percent = utila.roundme(percent * 100.0)
    linter(distance=current_distance, percent=percent)


SOLUTION_7582 = """\
Schriftart anpassen

Bitte anpassen
"""


def check_7582_general_text_family(linter: callable, driver):  # pylint:disable=W0613
    pass


SOLUTION_7583 = """\
Wordabstand anpassen

Bitte anpassen
"""


def check_7583_general_text_wordwidth(linter: callable, driver):  # pylint:disable=W0613
    pass


SOLUTION_7584 = """\
Zeichenabstand anpassen

Bitte anpassen
"""


def check_7584_general_text_charwidth(linter: callable, driver):  # pylint:disable=W0613
    pass
