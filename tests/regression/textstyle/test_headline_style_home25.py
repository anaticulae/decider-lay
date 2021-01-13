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

import decider_textstyle
import tests.textstyle_


def test_headline_size_validation_page4(testdir, monkeypatch):
    """Verify that extracted headline container line to text line. If
    the mapping is wrong, the wrong text size is selected and an
    incorrect linting is fired."""
    source = power.link(power.HOME025_PDF)
    cmd = f'-i {source}  --headlines --pages=4'
    tests.textstyle_.run(cmd, monkeypatch=monkeypatch)
    path = decider_textstyle.path.headlines(testdir.tmpdir)
    loaded = serializeraw.load_findings(path, msgids={7500, 7510, 7520})
    assert not loaded
