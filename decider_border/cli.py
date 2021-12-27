#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import protocol
import utila

import decider_border

DESCRIPTION = """\
The border_decider detects overlapping content to different extracted
border. There are four types of border.

1. The crop-border which contains the every element in the document.
2. The left-right border describes the border in books which is different
   for the left page and the right page.
3. The page border excludes page number on the bottom of the page.
4. The footer border excludes the area of the footer.
"""

WORKPLAN = [
    utila.create_step(
        'distance',
        [
            utila.ResultFile('groupme', 'area_area'),
            utila.ResultFile('groupme', 'distance_distance'),
        ],
        ('user', 'developer'),
    ),
    utila.create_step(
        'detection',
        [
            utila.ResultFile('rawmaker', 'border_boundingboxes'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'border_leftright'),
            utila.ResultFile('groupme', 'pagenumbers_pagenumbers'),
        ],
        ('hits', 'user', 'developer'),
    )
]


def main():
    hook = protocol.integrate(
        root=decider_border.ROOT,
        features='decider_border.features',
    )
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_border.ROOT,
        featurepackage='decider_border.features',
        config=utila.FeaturePackConfig(
            cli_hook=hook,
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_border.PROCESS,
            pages=True,
            version=decider_border.__version__,
        ),
    )
