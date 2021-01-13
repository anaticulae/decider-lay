# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import pathconnector as connect

import decider_textstyle


def headlines(path: str, prefix: str = '') -> str:
    return connect(path, decider_textstyle.PROCESS, 'headlines_user', prefix)


def text(path: str, prefix: str = '') -> str:
    return connect(path, decider_textstyle.PROCESS, 'text_user', prefix)
