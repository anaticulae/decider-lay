# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib


class MagicSkipper:

    def __init__(self, magiccontent):
        self.content = {
            item.page: {number: typ for number, typ in item.content
                       } for item in magiccontent
        }

    def __call__(self, page, line):
        with contextlib.suppress(KeyError):
            return self.content[page][line]
        return None
