# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import protoerror
import utilo

import decider_textstyle

DESCRIPTION = ''

WORKPLAN = [
    utilo.create_step(
        'headlines',
        inputs=[
            utilo.ResultFile('doctextstyle', 'textstyle'),
            utilo.ResultFile('headlines', 'result_result'),
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'oneline_fonts_header'),
            utilo.ResultFile('rawmaker', 'oneline_fonts_content'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        'text',
        inputs=[
            utilo.ResultFile('doctextstyle', 'textstyle'),
            utilo.ResultFile('headlines', 'result_result'),
            utilo.ResultFile('rawmaker', 'oneline_text_text'),
            utilo.ResultFile('rawmaker', 'oneline_text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'hefopa_result'),
            utilo.ResultFile('rawmaker', 'oneline_fonts_header'),
            utilo.ResultFile('rawmaker', 'oneline_fonts_content'),
            utilo.ResultFile('textflow', 'wordspace_wordspace', optional=True),
            utilo.ResultFile('magic', 'oneline_content', optional=True),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        'fonts',
        inputs=[
            utilo.ResultFile('doctextstyle', 'textstyle'),
            utilo.ResultFile('spacestation', 'worddist_worddist'),
            utilo.ResultFile('spacestation', 'chardist_chardist'),
        ],
        output=protoerror.ResultDefault,
    ),
    utilo.create_step(
        'toc',
        inputs=[
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('groupme', 'hefopa_result'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('rawmaker', 'fonts_header'),
            utilo.ResultFile('rawmaker', 'fonts_content'),
            utilo.ResultFile('reftable', 'toc_toc'),
        ],
        output=protoerror.ResultDefault,
    ),
]


def main():
    hook = protoerror.integrate(
        root=decider_textstyle.ROOT,
        features=[
            'decider_textstyle.features',
            'decider_textstyle.headlines',
            'decider_textstyle.text',
        ],
    )
    utilo.featurepack(
        workplan=WORKPLAN,
        root=decider_textstyle.ROOT,
        featurepackage='decider_textstyle.features',
        config=utilo.FeaturePackConfig(
            cli_hook=hook,
            description=DESCRIPTION,
            multiprocessed=True,
            name=decider_textstyle.PROCESS,
            pages=True,
            version=decider_textstyle.__version__,
        ),
    )
