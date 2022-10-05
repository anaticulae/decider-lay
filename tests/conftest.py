# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import utila
import writers

import decider_lay

PACKAGE = decider_lay.PACKAGE

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

WORKER = 6

RESOURCES = [
    (power.BACHELOR032_PDF, '0:10'),
    (power.BACHELOR051_PDF, '25:40'),
    (power.DISS157_PDF, '70:80'),
    (power.DISS170_PDF, '30:70'),
    (power.DISS172_PDF, '20:40'),
    (power.DISS266_PDF, '0:90'),
    (power.DOCU035_PDF, '0:10'),
    (power.MASTER075_PDF, '0:25'),
    (power.MASTER078_PDF, '0:10'),
    (power.MASTER091B_PDF, '0:20'),
    (power.MASTER098_PDF, '0:10,43:65,88:97'),
    (power.MASTER110_PDF, '0:70'),
    (power.MASTER116_PDF, '0:50,75:115'),
    (power.MASTER155_PDF, '0:25'),
    (power.TECH024_PDF, '0:15'),
    power.BACHELOR056_PDF,
    power.BACHELOR063_PDF,
    power.BACHELOR076_PDF,
    power.BACHELOR090_PDF,
    power.BOOK007_PDF,
    power.DOCU007_PDF,
    power.HOME025_PDF,
    power.MASTER072_PDF,
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    print_resources(resources)
    genex.extract(
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
        utila.log(f'source: {source}, pages: {page:8}')
