# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilo
import utilotest
import writers
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import decider_lay

PACKAGE = decider_lay.PACKAGE

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

RESOURCES = [
    (hoverpower.BACHELOR032_PDF, '0:10'),
    (hoverpower.BACHELOR051_PDF, '25:40'),
    (hoverpower.DISS157_PDF, '70:80'),
    (hoverpower.DISS170_PDF, '30:70'),
    (hoverpower.DISS172_PDF, '20:40'),
    (hoverpower.DISS266_PDF, '0:90'),
    (hoverpower.DOCU035_PDF, '0:10'),
    (hoverpower.MASTER075_PDF, '0:25'),
    (hoverpower.MASTER078_PDF, '0:10'),
    (hoverpower.MASTER091B_PDF, '0:20'),
    (hoverpower.MASTER098_PDF, '0:10,43:65,88:97'),
    (hoverpower.MASTER110_PDF, '0:70'),
    (hoverpower.MASTER116_PDF, '0:50,75:115'),
    (hoverpower.MASTER155_PDF, '0:25'),
    (hoverpower.TECH024_PDF, '0:15'),
    hoverpower.BACHELOR056_PDF,
    hoverpower.BACHELOR063_PDF,
    hoverpower.BACHELOR076_PDF,
    hoverpower.BACHELOR090_PDF,
    hoverpower.BOOK007_PDF,
    hoverpower.DOCU007_PDF,
    hoverpower.HOME025_PDF,
    hoverpower.MASTER072_PDF,
]
WORKER = utilotest.worker_count(6, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(resources):
    print_resources(resources)
    gennex.extract(
        files=resources,
        full=True,
        worker=WORKER,
    )


def install():
    # generate docs after project is installed properly
    writers.generate()


def print_resources(resources):
    for item in resources:
        try:
            source, page = item
        except ValueError:
            source, page, = item, 'all'
        utilo.log(f'source: {source}, pages: {page:8}')
