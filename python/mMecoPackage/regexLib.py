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
## @file    mMecoPackage/regexLib.py @brief [ FILE   ] - Regex.
## @package mMecoPackage.regexLib    @brief [ MODULE ] - Regex.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import mMecoPackage.enumLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
## [ str ] - Package info module regex (path/PACKAGE_NAME)/python/(PACKAGE_NAME)/packageInfoLib.py
PACKAGE_INFO_MODULE = r'(\S+[\\\\|\\|\/]\w+)[\\\\|\\|\/]python[\\\\|\\|\/](\w+)[\\\\|\\|\/]{}.\w+'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName)

## [ str ] - Version.
VERSION             = r'((\d+)\.(\d+)\.(\d+))'

## [ str ] - Versioned package root with empty package name to be formatted with `PACKAGE_NAME`.
VERSIONED_PACKAGE_ROOT_PATH_EMPTY_NAME = r'\S*[\/|\\+]{PACKAGE_NAME}[\/|\\+]((\d+)\.(\d+)\.(\d+))[\/|\\+]{PACKAGE_NAME}[\/|\\+]?'