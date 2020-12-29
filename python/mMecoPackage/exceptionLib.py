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
## @file    mMecoPackage/exceptionLib.py @brief [ FILE   ] - Exceptions.
## @package mMecoPackage.exceptionLib    @brief [ MODULE ] - Exceptions.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ EXCEPTION CLASS ] - Package name error.
class PackageNameError(Exception):

    pass

#
## @brief [ EXCEPTION CLASS ] - Package location error.
class PackageLocationError(Exception):

    pass

#
## @brief [ EXCEPTION CLASS ] - Python package name error.
class PythonPackageNameError(Exception):

    pass

#
## @brief [ EXCEPTION CLASS ] - Python package doesn't exist.
class PythonPackageDoesNotExist(Exception):

    pass
