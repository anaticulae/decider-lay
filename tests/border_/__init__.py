# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import iamraw
import serializeraw
import utilo
import utilotest

import decider_border

run, fail = utilotest.create_cli_runner(decider_border)


def extract_border_hits(
    root: str,
    source: str,
    mp,
    pages: str = '0:10',
) -> iamraw.PageContentHits:
    utilotest.fixture_requires(source)
    source = hoverpower.link(source)
    cmd = f'-i {source} -o {root} --pages={pages}'
    run(cmd, mp=mp)
    outputfile = decider_border.path.decider_border_hits(root)
    dumped = utilo.file_read(outputfile)
    detected_hits = serializeraw.load_hits(dumped)
    return detected_hits
