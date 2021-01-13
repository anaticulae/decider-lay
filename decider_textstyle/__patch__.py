# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import protocol


def select_pages(findings: iamraw.Findings, pages) -> iamraw.Findings:
    if pages is None:
        return findings
    pages = {pages} if isinstance(pages, int) else pages
    findings = [
        finding for finding in findings if finding.location.page in pages
    ]
    return findings


protocol.select_pages = select_pages
