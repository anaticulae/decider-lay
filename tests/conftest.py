# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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
    (power.MASTER116_PDF, '0:50,75:115'),
    (power.BACHELOR076_PDF, ':'),
    (power.BACHELOR056_PDF, '0:20'),
    (power.DISS266_PDF, '0:90'),
    (power.DOCU35_PDF, '0:10'),
    (power.BOOK007_PDF, '0:10'),
    (power.MASTER078_PDF, '0:10'),
    (power.DOCU07_PDF, '0:10'),
    (power.TECH024_PDF, '0:15'),
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    print_resources(resources)
    genex.extract(
        files=resources + [power.REPOSITORY],
        destination=power.generated(),
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
