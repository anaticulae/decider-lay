# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import decider_border


def border_user(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_border.PROCESS,
        'detection_user',
        prefix,
    )


def decider_border_hits(path: str, prefix: str = '') -> str:
    return utila.pathconnector(
        path,
        decider_border.PROCESS,
        'detection_hits',
        prefix,
    )
