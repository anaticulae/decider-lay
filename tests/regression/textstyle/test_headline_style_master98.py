# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilotest

import decider_textstyle.headlines.style
import decider_textstyle.path
import tests.textstyle_


@utilotest.requires(hoverpower.MASTER098_PDF)
def test_headline_font_family_validation_page6(td, mp):
    """The headline text is formatted in Times New Roman.

    The whitespace between text and number is formatted in Arial. In
    normal mode, this is not a problem and we skip this. Therefore no
    linting must occur.
    """
    source = hoverpower.link(hoverpower.MASTER098_PDF)
    cmd = f'-i {source}  --headlines --pages=6'
    tests.textstyle_.run(cmd, mp=mp)
    path = decider_textstyle.path.headlines(td.tmpdir)
    loaded = serializeraw.load_findings(path, msgids={7501})
    assert not loaded

    with mp.context() as context:
        # run linter in ``expert`` mode
        context.setattr(
            decider_textstyle.headlines.style,
            'WHITESPACE_LINTING',
            True,
        )
        tests.textstyle_.run(cmd, mp=mp)
    loaded = serializeraw.load_findings(path, msgids={7501})
    assert len(loaded) == 1


@pytest.mark.xfail(reason='invalid font hashing?')
@utilotest.requires(hoverpower.MASTER098_PDF)
def test_headline_font_family_char_marker(td, mp):
    """Ensure that linting is marked to wrong character and not to the
    whole line."""
    source = hoverpower.link(hoverpower.MASTER098_PDF)
    cmd = f'-i {source}  --headlines --pages=6'
    path = decider_textstyle.path.headlines(td.tmpdir)

    with mp.context() as context:
        # run linter in ``expert`` mode
        context.setattr(
            decider_textstyle.headlines.style,
            'WHITESPACE_LINTING',
            True,
        )
        tests.textstyle_.run(cmd, mp=mp)

    # Analyze linter result
    loaded = serializeraw.load_findings(path, msgids={7501})
    assert len(loaded) == 1
    char_finding_location = loaded[0].location
    # TODO: REPLACE TOKEN WITH CHAR
    assert char_finding_location.token == 1
    assert char_finding_location.token_end == 3
    # Arial as wrong font was detected
    assert 'Arial' in loaded[0].solution.description
