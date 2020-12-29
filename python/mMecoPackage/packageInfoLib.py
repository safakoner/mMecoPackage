#
# Copyright 2020 Safak Oner.
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ----------------------------------------------------------------------------------------------------
# DESCRIPTION
# ----------------------------------------------------------------------------------------------------
## @package mMecoPackage                       @brief [ PACKAGE   ] - Operate on Meco packages.
## @dir     mMecoPackage/python                @brief [ DIRECTORY ] - Python path.
## @dir     mMecoPackage/python/mMecoPackage   @brief [ DIRECTORY ] - Python package.
## @file    mMecoPackage/packageInfoLib.py     @brief [ FILE      ] - Package info module.
## @package mMecoPackage.packageInfoLib        @brief [ MODULE    ] - Package info module.



#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
## [ str ] - Name of the package.
NAME                = 'mMecoPackage'

## [ str ] - Version of the package.
VERSION             = '1.0.0'

## [ str ] - Description about the package.
DESCRIPTION         = 'Operate on Meco packages'

## [ list of str ] - Keywords to find this package.
KEYWORDS            = ['meco', 'package']

## [ list of str ] - Platforms which this package meant to be used on.
PLATFORMS           = ['Linux', 'Darwin', 'Windows']

## [ list of dict ] - Documentations about the package, keys of dict instances are: title, url.
DOCUMENTS           = [{'title':'Developer Reference  - Online', 'url':'https://meco.safakoner.com/'},
                       {'title':'Python API Reference - Online', 'url':'https://meco.api.safakoner.com/'}
                       ]

## [ list of str ] - Applications which this package meant to be initialized for.
APPLICATIONS        = ['all']

## [ list of str ] - Python versions supported by this package.
PYTHON_VERSIONS     = ['2', '3']

## [ bool ] - Whether this package is active (in use).
IS_ACTIVE           = True

## [ bool ] - Whether this package is external (third party).
IS_EXTERNAL         = False

## [ list of str ] - E-mail addresses of the developers.
DEVELOPERS          = ['safak@safakoner.com']

## [ list of str ] - Dependent packages.
DEPENDENT_PACKAGES  = ['mCore',
                       'mFileSystem',
                       'mMeco',
                       'mMecoSettings'
                       ]

## [ list of str ] - Python packages contained by this package.
PYTHON_PACKAGES     = ['mMecoPackage']
