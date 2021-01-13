# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import doctextstyle
import doctextstyle.cli
import utila

import decider_textstyle

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'headlines',
        inputs=[
            utila.ResultFile(doctextstyle.PROCESS, 'textstyle'),
            utila.ResultFile('words', 'headlines_headlines'),
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'oneline_fonts_header'),
            utila.ResultFile('rawmaker', 'oneline_fonts_content'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=('user', 'developer'),
    ),
    utila.create_step(
        'text',
        inputs=[
            utila.ResultFile(doctextstyle.PROCESS, 'textstyle'),
            utila.ResultFile('words', 'headlines_headlines'),
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'oneline_fonts_header'),
            utila.ResultFile('rawmaker', 'oneline_fonts_content'),
            utila.ResultFile(
                'magic',
                'content_content',
                optional=True,
            ),
        ],
        output=('user', 'developer'),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_textstyle.ROOT,
        featurepackage='decider_textstyle.features',
        config=utila.FeaturePackConfig(
            description=DESCRIPTION,
            multiprocessed=True,
            pages=True,
            name=decider_textstyle.PROCESS,
            version=decider_textstyle.__version__,
        ),
    )
