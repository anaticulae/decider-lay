# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import serializeraw
import utila
import utilatest

import decider_border
import decider_border.cli

# pylint:disable=C0103
run = functools.partial(
    utilatest.run_command,
    main=decider_border.cli.main,
    process=decider_border.PROCESS,
    success=True,
)
fail = functools.partial(
    utilatest.run_command,
    main=decider_border.cli.main,
    process=decider_border.PROCESS,
    success=False,
)


def extract_border_hits(
    root: str,
    source: str,
    monkeypatch,
    pages: str = '0:10',
) -> iamraw.PageContentHits:
    cmd = f'-i {source} -o {root} --pages={pages}'
    run(cmd, monkeypatch=monkeypatch)
    outputfile = decider_border.path.decider_border_hits(root)
    dumped = utila.file_read(outputfile)
    detected_hits = serializeraw.load_hits(dumped)
    return detected_hits
