# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo

import decider_lay
import decider_textstyle.__patch__

ROOT = decider_lay.ROOT

__version__ = decider_lay.__version__

PROCESS = 'decider_textstyle'

configo.cloud_lookup(PROCESS)
