# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import utilotest

import tests.textstyle_


def test_decider_textstyle_cli_help(mp):
    tests.textstyle_.run('--help', mp=mp)


@utilotest.nightly
@utilotest.requires(hoverpower.MASTER072_PDF)
def test_decider_textstyle_master72(td, mp):  # pylint:disable=W0613
    source = hoverpower.link(hoverpower.MASTER072_PDF)
    tests.textstyle_.run(f'-i {source}', mp=mp)
