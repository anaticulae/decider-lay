# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utilatest

import tests.textstyle_


def test_decider_textstyle_cli_help(monkeypatch):
    tests.textstyle_.run('--help', monkeypatch=monkeypatch)


@utilatest.longrun
def test_decider_textstyle_master72(testdir, monkeypatch):
    source = power.link(power.MASTER072_PDF)
    tests.textstyle_.run(f'-i {source}', monkeypatch=monkeypatch)
