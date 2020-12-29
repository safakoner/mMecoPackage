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
## @file    mMecoPackage/packageCmd.py @brief [ FILE   ] - Command module.
## @package mMecoPackage.packageCmd    @brief [ MODULE ] - Command module.


#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import os
import argparse
import webbrowser

import mCore.displayLib

import mMecoPackage.packageLib
import mMecoSettings.envVariablesLib


#
#-----------------------------------------------------------------------------------------------------
# CODE
#-----------------------------------------------------------------------------------------------------
#
## @brief Create a package.
#
#  @exception N/A
#
#  @return None - None.
def create():

    developmentPackagesPath = os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPMENT_PACKAGES_PATH)
    if not developmentPackagesPath:
        mCore.displayLib.Display.displayFailure('You must initialize a development environment to create a package.')
        return

    validPaths = [developmentPackagesPath]

    reservedPackagesPath = os.environ.get(mMecoSettings.envVariablesLib.MECO_RESERVED_PACKAGES_PATH)
    if reservedPackagesPath:
        validPaths.append(reservedPackagesPath)

    currentDirectory = os.getcwd()
    if currentDirectory not in validPaths:
        mCore.displayLib.Display.displayFailure('You must be in one of the following valid paths to create a package:')
        for path in validPaths:
            mCore.displayLib.Display.displayFailure(path, endNewLine=False)
        mCore.displayLib.Display.displayBlankLine()
        return

    parser = argparse.ArgumentParser(description='Create a package')

    parser.add_argument('name',
                        type=str,
                        help='Name of the package')

    parser.add_argument('-e',
                        '--external',
                        action='store_true',
                        help='Whether the package will be marked as external')

    args = parser.parse_args()

    package = None

    try:
        package = mMecoPackage.packageLib.Package.create(name=args.name,
                                                         path=currentDirectory,
                                                         external=args.external)
    except Exception as error:
        mCore.displayLib.Display.displayFailure(str(error))
        mCore.displayLib.Display.displayBlankLine()
        return

    mCore.displayLib.Display.displaySuccess('Package has been created: {}'.format(package.path()))
    mCore.displayLib.Display.displayBlankLine()

#
## @brief Create a python module for a package.
#
#  @exception N/A
#
#  @return None - None.
def createPythonModule():

    developmentPackagesPath = os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPMENT_PACKAGES_PATH)
    if not developmentPackagesPath:
        mCore.displayLib.Display.displayBlankLine()
        mCore.displayLib.Display.displayFailure('You must initialize a development environment to create a Python module.')
        mCore.displayLib.Display.displayBlankLine()
        return

    currentPath = os.getcwd()

    package = mMecoPackage.packageLib.Package()

    if not package.setPackage(path=currentPath):
        mCore.displayLib.Display.displayFailure('Path doesn\'t seem to be a root of a package: {}'.format(currentPath))
        mCore.displayLib.Display.displayBlankLine()
        return

    if package.isVersioned():
        mCore.displayLib.Display.displayFailure('You can\'t create a Python module for a versioned (released) package: {}'.format(currentPath))
        mCore.displayLib.Display.displayFailure('The package must be under your development environment.')
        mCore.displayLib.Display.displayBlankLine()
        return

    parser = argparse.ArgumentParser(description='Create a Python module for a package')

    parser.add_argument('name',
                        type=str,
                        help='Name of the module')

    _args = parser.parse_args()

    pythonPackageList  = package.getPythonPackages()
    pythonPackageToUse = pythonPackageList[0]

    if len(pythonPackageList) > 1:

        packageDict = {}
        packageStr  = ''

        for index, value in enumerate(pythonPackageList):
            packageDict[str(index+1)] = value
            packageStr += '\n    {} - {}'.format(index+1, value)
        packageStr += '\n\n'

        mCore.displayLib.Display.displayInfo('Available Python Packages for "{}" package:'.format(package.name()))
        mCore.displayLib.Display.displayInfo(packageStr, startNewLine=False, endNewLine=False)

        selectedPackageIndex = -1
        while selectedPackageIndex == -1:
            try:
                mCore.displayLib.Display.displayInfo('Select a Python Package by entering integer value: ', startNewLine=False, endNewLine=False)
                selectedPackageIndex = input()
            except Exception as error:
                mCore.displayLib.Display.displayFailure('Entered value is not an integer.')
                return

        pythonPackageToUse = packageDict.get(str(selectedPackageIndex), None)
        if not pythonPackageToUse:
            mCore.displayLib.Display.displayFailure('Selection wasn\'t valid.')
            mCore.displayLib.Display.displayBlankLine()
            return

    createdFileList = package.createPythonModule(pythonModuleName=_args.name, pythonPackageName=pythonPackageToUse)

    mCore.displayLib.Display.displayInfo('Created Python modules (Existing modules are untouched):')
    mCore.displayLib.Display.displayBlankLine()

    for i in createdFileList:
        mCore.displayLib.Display.displaySuccess(i, startNewLine=False)

    mCore.displayLib.Display.displayInfo('Done.')
    mCore.displayLib.Display.displayBlankLine()

#
## @brief Create a python package for a package.
#
#  @exception N/A
#
#  @return None - None.
def createPythonPackage():

    developmentPackagesPath = os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPMENT_PACKAGES_PATH)
    if not developmentPackagesPath:
        mCore.displayLib.Display.displayBlankLine()
        mCore.displayLib.Display.displayFailure('You must initialize a development environment to create a Python package.')
        mCore.displayLib.Display.displayBlankLine()
        return

    currentPath = os.getcwd()

    package = mMecoPackage.packageLib.Package()

    if not package.setPackage(path=currentPath):
        mCore.displayLib.Display.displayFailure('Path doesn\'t seem to be a root of a package: {}'.format(currentPath))
        mCore.displayLib.Display.displayBlankLine()
        return

    parser = argparse.ArgumentParser(description='Create a Python package for a package')

    parser.add_argument('name',
                        type=str,
                        help='Name of the module')

    _args = parser.parse_args()

    pythonPackageName = _args.name

    pythonPackagePath = None

    try:
        pythonPackagePath = package.createPythonPackage(pythonPackageName=pythonPackageName)
    except Exception as error:
        mCore.displayLib.Display.displayFailure(str(error))
        mCore.displayLib.Display.displayBlankLine()
        return

    mCore.displayLib.Display.displayInfo('Python package has been created: {}'.format(pythonPackagePath))
    mCore.displayLib.Display.displayBlankLine()


#
## @brief Display documentation on web browser.
#
#  @exception N/A
#
#  @return None - None.
def displayDoc():

    parser = argparse.ArgumentParser(description='Open documents on web browser')

    parser.add_argument('-n',
                        '--name',
                        type=str,
                        default='',
                        help='Name of the package',
                        required=False)

    parser.add_argument('-a',
                        '--all',
                        action='store_true',
                        help='Open all available documents on web browser')

    _args       = parser.parse_args()
    packageName = _args.name
    all         = _args.all

    _package    = None

    if packageName:
        try:
            _package = mMecoPackage.packageLib.Package.getPackageByImport(name=packageName)
        except Exception as error:
            mCore.displayLib.Display.displayFailure(str(error))
            return

        if not _package:
            mCore.displayLib.Display.displayFailure('No package found with given name: {}'.format(packageName))
            mCore.displayLib.Display.displayBlankLine()
            return

    #

    if not _package:
        currentPath = os.getcwd()
        _package    = mMecoPackage.packageLib.Package()

        try:
            if not _package.setPackage(path=currentPath):
                mCore.displayLib.Display.displayFailure('Path doesn\'t seem to be a root of a package: {}'.format(currentPath))
                mCore.displayLib.Display.displayBlankLine()
                return
        except Exception as error:
            mCore.displayLib.Display.displayFailure(str(error))
            mCore.displayLib.Display.displayBlankLine()
            return


    documents = _package.documents()
    if not documents:
        mCore.displayLib.Display.displayFailure('No documents found for: {}'.format(_package.name()))
        mCore.displayLib.Display.displayBlankLine()
        return

    #
    if all:
        message   = ''
        for index, item in enumerate(documents, start=1):
            webbrowser.open_new_tab(item['url'])
            message += '\n    {} - {} : {}'.format(index, item['title'].ljust(30), item['url'])
        message += '\n\n'

        mCore.displayLib.Display.displayInfo('Available documents for "{}" package:'.format(_package.name()))
        mCore.displayLib.Display.displayInfo(message, startNewLine=False, endNewLine=False)

        mCore.displayLib.Display.displaySuccess('All documents listed above have been opened.', startNewLine=False)

        return

    #

    if len(documents) == 1:

        title = documents[0]['title']
        url   = documents[0]['url']

        if not url:
            mCore.displayLib.Display.displayFailure('Documentation titled "{}" has no URL.'.format(title))
            mCore.displayLib.Display.displayBlankLine()
            return

        webbrowser.open_new_tab(url)

        mCore.displayLib.Display.displayBlankLine()
        mCore.displayLib.Display.displaySuccess('Document with the following URL has been opened: {}'.format(url), startNewLine=False, endNewLine=False)
        mCore.displayLib.Display.displayBlankLine()
        return

    #

    docValues = {}
    message   = ''

    for index, item in enumerate(documents, start=1):
        docValues[str(index)] = item['title']
        message += '\n    {} - {} : {}'.format(index, item['title'].ljust(30), item['url'])
    message += '\n\n'

    mCore.displayLib.Display.displayInfo('Available documents for "{}" package:'.format(_package.name()))
    mCore.displayLib.Display.displayInfo(message, startNewLine=False, endNewLine=False)

    selectedIndex = -1
    while selectedIndex == -1:
        try:
            mCore.displayLib.Display.displayInfo('Select a documentation by entering integer value: ', startNewLine=False, endNewLine=False)
            selectedIndex = input()
        except Exception as error:
            mCore.displayLib.Display.displayFailure('Entered value is not an integer.')
            return

    selectedTitle = docValues.get(str(selectedIndex), None)
    if not selectedTitle:
        mCore.displayLib.Display.displayFailure('Selection wasn\'t valid.')
        mCore.displayLib.Display.displayBlankLine()
        return

    for item in documents:
        if selectedTitle == item['title']:
            url = item['url']
            webbrowser.open_new_tab(url)
            mCore.displayLib.Display.displayBlankLine()
            mCore.displayLib.Display.displaySuccess('Document with the following URL has been opened: {}'.format(url), startNewLine=False, endNewLine=False)
            mCore.displayLib.Display.displayBlankLine()
            break

#
## @brief Display info about the current package.
#
#  @exception N/A
#
#  @return None - None.
def displayInfo():

    parser = argparse.ArgumentParser(description='Display information about a package')

    parser.add_argument('-n',
                        '--name',
                        type=str,
                        default='',
                        help='Name of the package',
                        required=False)

    _args       = parser.parse_args()
    packageName = _args.name


    if packageName:
        try:
            _package = mMecoPackage.packageLib.Package.getPackageByImport(name=packageName)
        except Exception as error:
            mCore.displayLib.Display.displayFailure(str(error))
            return

        if not _package:
            mCore.displayLib.Display.displayFailure('No package found with given name: {}'.format(packageName))
            mCore.displayLib.Display.displayBlankLine()
            return
        else:
            mCore.displayLib.Display.displayInfo(_package, startNewLine=False)
            _displayStats(_package)
            return

    #

    currentPath = os.getcwd()
    _package    = mMecoPackage.packageLib.Package()

    try:
        if not _package.setPackage(path=currentPath):
            mCore.displayLib.Display.displayFailure('Path doesn\'t seem to be a root of a package: {}'.format(currentPath))
            mCore.displayLib.Display.displayBlankLine()
            return
    except Exception as error:
        mCore.displayLib.Display.displayFailure(str(error))
        mCore.displayLib.Display.displayBlankLine()
        return

    mCore.displayLib.Display.displayInfo(_package, startNewLine=False)

    _displayStats(_package)

#
## @brief Find python package.
#
#  @exception N/A
#
#  @return None - None.
def findPythonPackage():

    parser = argparse.ArgumentParser(description='Create a Python module for a package')

    parser.add_argument('name',
                        type=str,
                        help='Name of the Python package that needs to be found')

    _args = parser.parse_args()

    pythonPackageName = _args.name

    package = mMecoPackage.packageLib.Package.getPackageByImport(pythonPackageName)

    if not package:
        mCore.displayLib.Display.displayFailure('No Python package named "{}" found under any Meco package.'.format(pythonPackageName))
        mCore.displayLib.Display.displayBlankLine()
        return

    mCore.displayLib.Display.displaySuccess('Python package "{}" is contained by the following Meco package:'.format(pythonPackageName))

    mCore.displayLib.Display.displayInfo(package, startNewLine=False)
    mCore.displayLib.Display.displayBlankLine()

#
## @brief Run all unit tests in the package.
#
#  @exception N/A
#
#  @return None - None.
def runUnitTest():

    developmentPackagesPath = os.environ.get(mMecoSettings.envVariablesLib.MECO_DEVELOPMENT_PACKAGES_PATH)
    if not developmentPackagesPath:
        mCore.displayLib.Display.displayFailure('You must initialize development environment to run unittests of a package.')
        mCore.displayLib.Display.displayBlankLine()
        return

    currentPath = os.getcwd()

    package = mMecoPackage.packageLib.Package()

    if not package.setPackage(path=currentPath):
        mCore.displayLib.Display.displayFailure('Path doesn\'t seem to be a root of a package: {}'.format(currentPath))
        mCore.displayLib.Display.displayBlankLine()
        return

    parser = argparse.ArgumentParser(description='Run unit tests of Python package(s) under a package.')

    parser.add_argument('-n',
                        '--name',
                        type=str,
                        default=None,
                        help='Name of the Python package, which the tests will be run for.',
                        required=False)

    _args             = parser.parse_args()
    pythonPackageName = _args.name

    resultList = []

    try:
        resultList = package.runUnitTests(pythonPackageName=pythonPackageName)
    except Exception as error:
        mCore.displayLib.Display.displayFailure('{}'.format(str(error)))
        mCore.displayLib.Display.displayBlankLine()
        return

    if not resultList:
        mCore.displayLib.Display.displayInfo('No unit test found in this package: {}'.format(package.name()))
        mCore.displayLib.Display.displayBlankLine()
        return

    hasFailure = False

    for result in resultList:
        mCore.displayLib.Display.displayInfo('{}.{} {} Tests'.format(result['module'],
                                                                     result['class'],
                                                                     result['count']),
                                             endNewLine=False)

        if result['errors']:
            hasFailure = True
            mCore.displayLib.Display.displayBlankLine()
            # mCore.displayLib.Display.displayInfo('\nErrors:')
            for f in result['errors']:
                 for line in f:
                     mCore.displayLib.Display.displayFailure(line, endNewLine=False)

        if result['failures']:
            hasFailure = True
            mCore.displayLib.Display.displayBlankLine()
            # mCore.displayLib.Display.displayInfo('\nFailures:')
            for f in result['failures']:
                 for line in f:
                     mCore.displayLib.Display.displayFailure(line, endNewLine=False)

    if hasFailure:
        mCore.displayLib.Display.displayFailure('\n\nFailures occurred in unit test.\n')
        return

    mCore.displayLib.Display.displaySuccess('\n\nSuccess.\n')

#
## @brief Search packages.
#
#  @exception N/A
#
#  @return None - None.
def search():

    packageList = mMecoPackage.packageLib.Package.list()

    if not packageList:
        return

    parser = argparse.ArgumentParser(description='Search packages')

    parser.add_argument('keyword',
                        type=str,
                        help='Keyword to be searched')

    parser.add_argument('-d',
                        '--detail',
                        action='store_true',
                        help='Display details about the packages')

    _args   = parser.parse_args()

    keyword = _args.keyword.lower()
    detail  = _args.detail

    packageCount = 0

    for packageModule in packageList:

        package = mMecoPackage.packageLib.Package(path=packageModule)

        if keyword in package.name().lower()        or \
           keyword in package.description().lower() or \
           keyword in package.keywords():

            packageCount += 1

            if detail:
                mCore.displayLib.Display.displayInfo(package, startNewLine=False)
            else:
                mCore.displayLib.Display.displayInfo('{}{}{}'.format(package.name().ljust(30),
                                                                     package.version().ljust(8),
                                                                     package.path()),
                                                     endNewLine=False)

    if packageCount:
        mCore.displayLib.Display.displayInfo('\n\n{} packages found.\n'.format(packageCount))
    else:
        mCore.displayLib.Display.displayInfo('No packages found.')
        mCore.displayLib.Display.displayBlankLine()

#
## @brief Display stats about given package.
#
#  @param package [ mMecoPackage.packageLib.Package | None | in  ] - Package class instance.
#
#  @exception N/A
#
#  @return None - None.
def _displayStats(package):

    mCore.displayLib.Display.displayInfo('Stats', endNewLine=False)

    lineOfCodeList = package.getLineOfCode()
    if lineOfCodeList:
        for i in lineOfCodeList:
            languageName = '({})'.format(i).ljust(9)
            mCore.displayLib.Display.displayInfo('Line of code {}: {}'.format(languageName, lineOfCodeList[i]), endNewLine=False)

    mCore.displayLib.Display.displayBlankLine(2)