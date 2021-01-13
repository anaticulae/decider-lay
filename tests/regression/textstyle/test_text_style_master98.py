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


def test_textsize_in_table_page55(testdir, monkeypatch):
    """Verify that normal text size check does not run in table data."""
    # TODO: ADD TABLE CONTENT STYLE CHECKER
    source = power.link(power.MASTER098_PDF)
    cmd = f'-i {source}  --text --pages=51:55'
    tests.textstyle_.run(cmd, monkeypatch=monkeypatch)
    path = decider_textstyle.path.text(testdir.tmpdir)
    loaded = serializeraw.load_findings(path, msgids={7550})
    loaded = [item for item in loaded if item.location.page == 54]
    assert not loaded
