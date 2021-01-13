# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import decider_textstyle
import tests.textstyle_


@utilatest.longrun
def test_font_family_bachelor90_page13(testdir, monkeypatch):
    """This is a regression test for false detected level 2 headline
    style judging. Before this patch, there was a mix of loading oneline
    text with normal font header. Therefore the style current headline
    style was judged wrongly."""
    source = power.link(power.BACHELOR090_PDF)
    cmd = f'-i {source}  --headlines --pages=13'
    tests.textstyle_.run(cmd, monkeypatch=monkeypatch)
    path = decider_textstyle.path.headlines(testdir.tmpdir)
    loaded = serializeraw.load_findings(path, msgids={7511})
    assert not loaded
