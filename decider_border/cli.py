#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import protoerror
import utilo

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
    utilo.create_step(
        'distance',
        [
            utilo.ResultFile('groupme', 'area_area'),
            utilo.ResultFile('groupme', 'distance_distance'),
        ],
        ('user', 'developer'),
    ),
    utilo.create_step(
        'detection',
        [
            utilo.ResultFile('rawmaker', 'border_boundingboxes'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'border_leftright'),
            utilo.ResultFile('pagenumber', 'result_result'),
        ],
        ('hits', 'user', 'developer'),
    )
]


def main():
    hook = protoerror.integrate(
        root=decider_border.ROOT,
        features='decider_border.features',
    )
    utilo.featurepack(
        workplan=WORKPLAN,
        root=decider_border.ROOT,
        featurepackage='decider_border.features',
        config=utilo.FeaturePackConfig(
            cli_hook=hook,
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_border.PROCESS,
            pages=True,
            version=decider_border.__version__,
        ),
    )
