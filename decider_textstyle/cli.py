# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protocol
import utila

import decider_textstyle

DESCRIPTION = ''

WORKPLAN = [
    utila.create_step(
        'headlines',
        inputs=[
            utila.ResultFile('doctextstyle', 'textstyle'),
            utila.ResultFile('words', 'headlines_headlines'),
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'oneline_fonts_header'),
            utila.ResultFile('rawmaker', 'oneline_fonts_content'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        'text',
        inputs=[
            utila.ResultFile('doctextstyle', 'textstyle'),
            utila.ResultFile('words', 'headlines_headlines'),
            utila.ResultFile('rawmaker', 'oneline_text_text'),
            utila.ResultFile('rawmaker', 'oneline_text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'oneline_fonts_header'),
            utila.ResultFile('rawmaker', 'oneline_fonts_content'),
            utila.ResultFile('textflow', 'wordspace_wordspace', optional=True),
            utila.ResultFile('magic', 'oneline_content', optional=True),
        ],
        output=protocol.ResultDefault,
    ),
    utila.create_step(
        'fonts',
        inputs=[
            utila.ResultFile('doctextstyle', 'textstyle'),
            utila.ResultFile('spacestation', 'worddist_worddist'),
            utila.ResultFile('spacestation', 'chardist_chardist'),
        ],
        output=protocol.ResultDefault,
    ),
]


def main():
    hook = protocol.integrate(
        root=decider_textstyle.ROOT,
        features=[
            'decider_textstyle.features',
            'decider_textstyle.headlines',
            'decider_textstyle.text',
        ],
    )
    utila.featurepack(
        workplan=WORKPLAN,
        root=decider_textstyle.ROOT,
        featurepackage='decider_textstyle.features',
        config=utila.FeaturePackConfig(
            cli_hook=hook,
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_textstyle.PROCESS,
            pages=True,
            version=decider_textstyle.__version__,
        ),
    )
