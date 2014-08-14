#!/usr/bin/env python3
# -*- mode: python; -*-
#
#
# Copyright 2014 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
maasclient
===============

Python3 bindings for MAAS

"""

from setuptools import setup, find_packages

import os
import sys

VERSION = '0.2'

REQUIREMENTS = [
    "requests"
]

TEST_REQUIREMENTS = list(REQUIREMENTS)
TEST_REQUIREMENTS.extend(["mock", "nose"])

if sys.argv[-1] == 'clean':
    print("Cleaning up ...")
    os.system('rm -rf maasclient.egg-info build dist')
    sys.exit()

if sys.argv[-1] == 'version':
    print(VERSION)
    sys.exit()

setup(name='maasclient',
      version=VERSION,
      description="Python 3 bindings for MAAS",
      long_description=__doc__,
      author='Canonical Solutions Engineering',
      author_email='ubuntu-dev@lists.ubuntu.com',
      url='https://github.com/Ubuntu-Solutions-Engineering/maasclient',
      license="AGPLv3+",
      packages=find_packages(exclude=["test"]))
