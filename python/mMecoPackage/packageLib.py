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
## @file    mMecoPackage/packageLib.py @brief [ FILE   ] - Package.
## @package mMecoPackage.packageLib    @brief [ MODULE ] - Package.

#
# ----------------------------------------------------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------------------------------------------------
import      os
import      sys
import      re
import      collections
import      inspect
import      shutil
import      unittest

try:
    from    StringIO        import StringIO
except ImportError as error:
    from    io              import StringIO

from        types           import ModuleType
from        importlib       import import_module

import      mCore.pythonUtilsLib

import      mFileSystem.directoryLib
import      mFileSystem.fileLib
import      mFileSystem.templateFileLib

import      mMecoPackage.enumLib
import      mMecoPackage.exceptionLib
import      mMecoPackage.regexLib


#
# ----------------------------------------------------------------------------------------------------
# CODE
# ----------------------------------------------------------------------------------------------------
#
## @brief [ CLASS ] - Class to operate on Meco packages.
class Package(object):
    #
    # ------------------------------------------------------------------------------------------------
    # PROTECTED METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Constructor.
    #
    #  @param path [ str | None | in  ] - Absolute path of an package info module.
    #
    #  @exception N/A
    #
    #  @return None - None.
    def __init__(self, path=None):

        ## [ str ] - Name.
        self._name              = ''

        ## [ str ] - Version.
        self._version           = ''

        ## [ str ] - Description.
        self._description       = ''

        ## [ list of str ] - Keywords.
        self._keywords          = []

        ## [ list of str ] - Platforms.
        self._platforms         = []

        ## [ list of dict ] - Documents.
        self._documents         = []

        ## [ list of str ] - Applications.
        self._applications      = []

        ## [ list of str ] - Python versions.
        self._pythonVersions    = []

        ## [ bool ] - Whether this package is active (in use).
        self._isActive          = True

        ## [ bool ] - Whether this package is external.
        self._isExternal        = False

        ## [ list of str ] - Developers.
        self._developers        = []

        ## [ list of str ] - Dependent packages.
        self._dependentPackages = []

        ## [ list of str ] - Python packages contained by this package.
        self._pythonPackages    = []

        ## [ bool ] - Whether this package is versioned, meaning that its under version folder.
        self._isVersioned       = False

        ## [ str ] - Path.
        self._path              = ''

        ## [ list of str ] - All dependencies.
        self._allDependencies   = []

        if path:
            self.setPackage(path)

    #
    ## @brief String representation.
    #
    #  @exception N/A
    #
    #  @return str - String representation.
    def __str__(self):

        return self.asStr()

    #
    # ------------------------------------------------------------------------------------------------
    # PROPERTY METHODS
    # ------------------------------------------------------------------------------------------------
    ## @name PROPERTIES

    ## @{
    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Name.
    def name(self):

        return self._name

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Version.
    def version(self):

        return self._version

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Description.
    def description(self):

        return self._description

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of str - Keywords.
    def keywords(self):

        return self._keywords

    #
    ## @brief Platforms.
    #
    #  @exception N/A
    #
    #  @return list of str - Platforms.
    def platforms(self):

        return self._platforms

    #
    ## @brief Documents.
    #
    #  @exception N/A
    #
    #  @return list of dict - Keys of dict instances are: title, url.
    def documents(self):

        return self._documents

    #
    ## @brief Applications.
    #
    #  @exception N/A
    #
    #  @return list of str - Applications.
    def applications(self):

        return self._applications

    #
    ## @brief Python versions.
    #
    #  @exception N/A
    #
    #  @return list of str - Python versions.
    def pythonVersions(self):

        return self._pythonVersions

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Whether this package is active (in use).
    def isActive(self):

        return self._isActive

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Whether this package is external.
    def isExternal(self):

        return self._isExternal

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of str - Developers.
    def developers(self):

        return self._developers

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of str - Dependent packages.
    def dependentPackages(self):

        return self._dependentPackages

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return list of str - Python packages contained by this package.
    def pythonPackages(self):

        return self._pythonPackages

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    def isVersioned(self):

        return self._isVersioned

    #
    ## @brief Property.
    #
    #  @exception N/A
    #
    #  @return str - Path.
    def path(self):

        return self._path

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Set a package.
    #
    #  @param path [ str | None | in  ] - Absolute path of an package info module.
    #
    #  @exception AttributeError - If package info module doesn't have a required attribute.
    #
    #  @return None - None.
    def setPackage(self, path):

        packageModule = None

        if isinstance(path, ModuleType):
            # Given path is a Python module
            # Check whether its a package info module, if so, use it
            packageRootPath = Package.isInfoModuleFile(path.__file__)

            if packageRootPath:
                packageModule = path

        elif isinstance(path, str):
            # Given path is a str
            # Check whether its an absolute path of the package info module file
            packageModule = Package.getInfoModule(path)

        if not packageModule:
            return False

        # Check the module whether it has all the required attributes
        for attr in mMecoPackage.enumLib.PackageInfoModuleAttribute.listAttributes(stringOnly=True,
                                                              getValues=True,
                                                              removeK=True):
            if not hasattr(packageModule, attr):
                raise AttributeError('Package info module does not have "{}" attribute: {}'.format(attr, packageModule.__file__))

        self._name              = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kName)
        self._version           = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kVersion)
        self._description       = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kDescription)
        self._keywords          = [x.lower() for x in getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kKeywords)]
        self._platforms         = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kPlatforms)
        self._documents         = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kDocuments)
        self._applications      = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kApplications)
        self._pythonVersions    = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kPythonVersions)
        self._isActive          = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kIsActive)
        self._isExternal        = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kIsExternal)
        self._developers        = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kDevelopers)
        self._dependentPackages = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kDependentPackages)
        self._pythonPackages    = getattr(packageModule, mMecoPackage.enumLib.PackageInfoModuleAttribute.kPythonPackages)

        self._path = Package.isInfoModuleFile(packageModule.__file__)

        # Check whether local document provided
        for item in self._documents:
            url = item['url']
            localFile = mFileSystem.directoryLib.Directory.join(self._path, url)
            if os.path.isfile(localFile):
                item['url'] = 'file://{}'.format(localFile)

        # Add API References
        for doc in [['C++ API Reference'   , self.getLocalDocument(mMecoPackage.enumLib.PackageFolderStructure.kDocDeveloperCPPAPIReference)],
                    ['Python API Reference', self.getLocalDocument(mMecoPackage.enumLib.PackageFolderStructure.kDocDeveloperPythonAPIReference)],
                    ['Reference'           , self.getLocalDocument(mMecoPackage.enumLib.PackageFolderStructure.kDocDeveloperReference)]
                    ]:
            if doc[1]:
                self._documents.append({'title':doc[0], 'url':'file://{}'.format(doc[1])})

        if re.match(mMecoPackage.regexLib.VERSIONED_PACKAGE_ROOT_PATH_EMPTY_NAME.format(PACKAGE_NAME=self._name),
                    self._path):
            self._isVersioned = True
        else:
            self._isVersioned = False

        return True

    #
    # ----------------------------------------------------------------------------------------------------
    # REPRESENTATION
    # ----------------------------------------------------------------------------------------------------
    ## @name REPRESENTATION

    ## @{
    #
    ## @brief Get string representation of the class.
    #
    #  @exception N/A
    #
    #  @return str - Information about the package in human readable form.
    def asStr(self):

        documents = ''
        if self._documents:
            for d in self._documents:
                documents += '\n                      {} : {}'.format(d['title'].ljust(20), d['url'])

        if not documents:
            documents = 'N/A'

        data = ''
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kName.ljust(20)             ,      self._name)
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kVersion.ljust(20)          ,      self._version)
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kDescription.ljust(20)      ,      self._description)
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kKeywords.ljust(20)         , ', '.join(self._keywords))
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kPlatforms.ljust(20)        , ', '.join(self._platforms))
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kDocuments.ljust(20)        ,      documents)
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kApplications.ljust(20)     , ', '.join(self._applications))
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kPythonVersions.ljust(20)   , ', '.join(self._pythonVersions))
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kIsActive.ljust(20)         ,      self._isActive)
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kIsExternal.ljust(20)       ,      self._isExternal)
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kDevelopers.ljust(20)       , ', '.join(self._developers))
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kDependentPackages.ljust(20), ', '.join(self._dependentPackages))
        data += '\n{}: {}'.format(mMecoPackage.enumLib.PackageInfoModuleAttribute.kPythonPackages.ljust(20)   , ', '.join(self._pythonPackages))
        data += '\n{}: {}'.format('IS_VERSIONED'.ljust(20)                                                    ,      self._isVersioned)
        data += '\n{}: {}'.format('PATH'.ljust(20)                                                            ,      self._path)

        return data

    #
    ## @brief Get package information as a dict instance.
    #
    #  Keys of the returned dict instance are available in mMecoPackage.enumLib.PackageInfoModuleAttribute enum class.
    #  Additionally `PATH` and `IS_VERSIONED` keys are dynamically added to the returned dict instance.
    #
    #  @exception N/A
    #
    #  @return dict - Package information.
    def asDict(self):

        data = {mMecoPackage.enumLib.PackageInfoModuleAttribute.kName: self._name,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kVersion: self._version,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kDescription: self._description,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kKeywords: self._keywords,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kPlatforms: self._platforms,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kDocuments: self._documents,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kApplications: self._applications,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kPythonVersions: self._pythonVersions,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kIsActive: self._isActive,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kIsExternal: self._isExternal,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kDevelopers: self._developers,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kDependentPackages: self._dependentPackages,
                mMecoPackage.enumLib.PackageInfoModuleAttribute.kPythonPackages: self._pythonPackages,
                'IS_VERSIONED': self._isVersioned, 'PATH': self._path}

        return collections.OrderedDict(sorted(data.items()))

    #
    ## @brief Get HTML representation of the package.
    #
    #  This method provides information so it can be used on a GUI such as about dialog.
    #
    #  @exception N/A
    #
    #  @return str - Information about the package in human readable form in HTML format.
    def asHTML(self):

        htmlStr = '''<head><style>span{margin-left:4px}</style>'''

        dataDict = self.asDict()

        for i in dataDict:

            key   = i.lower().title().replace('_', ' ')
            value = dataDict[i]

            if value and isinstance(value, list) and isinstance(value[0], dict):
                pass

            elif isinstance(value, list) or isinstance(value, tuple):
                if value:
                    value = ', '.join(value)
                else:
                    value = 'N/A'

            if value is None:
                value = 'N/A'

            htmlStr += '<b>{}</b>: <span>{}</span><br><br>'.format(key.ljust(15), value)

        htmlStr += '</head>'

        return htmlStr

    #
    ## @}

    #
    # ----------------------------------------------------------------------------------------------------
    # CREATE
    # ----------------------------------------------------------------------------------------------------
    ## @name CREATE

    ## @{
    #
    ## @brief Create a Python module for the given Python package.
    #
    #  @param pythonPackageName [ str | None | in  ] - Name of the Python package under this package, which the Python module will be created for.
    #
    #  @exception mMecoPackage.exceptionLib.PackageLocationError   - If this package is versioned.
    #  @exception mMecoPackage.exceptionLib.PythonPackageNameError - If a Python package with given name already exists under this package.
    #
    #  @return str  - Absolute path of the created Python package in `PATH/PACKAGE_NAME/python/PYTHON_PACKAGE_NAME` format.
    #  @return None - If no package has been set.
    def createPythonPackage(self, pythonPackageName):

        if not self._path:
            return None

        if self._isVersioned:
            message = 'The package is not under a development environment.' \
                      'You can\'t create a Python package for a versioned (released) package: {}'.format(self._path)
            raise mMecoPackage.exceptionLib.PackageLocationError(message)

        if pythonPackageName in self.getPythonPackages():
            raise mMecoPackage.exceptionLib.PythonPackageNameError('A Python package with given name already exists under this package: {}'.format(pythonPackageName))

        return mCore.pythonUtilsLib.createPythonPackage(self.getPythonPath(), pythonPackageName)

    #
    ## @brief Create a Python module for the given Python package of the package.
    #
    #  @param pythonModuleName  [ str | None | in  ] - Name of the Python module to be created.
    #  @param pythonPackageName [ str | None | in  ] - Name of the Python package under this package, which the Python module will be created in.
    #
    #  @exception mMecoPackage.exceptionLib.PackageLocationError      - If this package is versioned.
    #  @exception mMecoPackage.exceptionLib.PythonPackageDoesNotExist - If no relevant Python package found for Python module creation.
    #
    #  @return list of str - Absolute path of the created Python modules, first one is the module, second one is the unit test module.
    #  @return None        - If no package has been set.
    def createPythonModule(self, pythonModuleName, pythonPackageName=None):

        if not self._path:
            return None

        if self._isVersioned:
            message = 'The package is not under a development environment.' \
                      'You can\'t create a Python module for a versioned (released) package: {}'.format(self._path)
            raise mMecoPackage.exceptionLib.PackageLocationError(message)

        if not pythonPackageName:
            pythonPackageName = self._name

        pythonPackagePath = self.getPythonPackagePath(pythonPackageName)

        if not pythonPackagePath or not os.path.isdir(pythonPackagePath):
            raise mMecoPackage.exceptionLib.PythonPackageDoesNotExist('Package has no such Python package: {}.{}'.format(self._name,
                                                                                                                         pythonPackageName))

        #

        settingsPackage = Package.getPackageByImport('mMecoSettings.{}'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))

        #

        pythonFile = mFileSystem.directoryLib.Directory.join(pythonPackagePath, '{}.py'.format(pythonModuleName))
        if not os.path.isfile(pythonFile):

            templateFile = mFileSystem.templateFileLib.TemplateFile()
            templateFile.setFile(mFileSystem.directoryLib.Directory.join(settingsPackage.path(),
                                                                         mMecoPackage.enumLib.PackageFolderStructure.kResources,
                                                                         'templates',
                                                                         'package',
                                                                         'pythonModuleLib.py'))

            replaceData = {'PACKAGE_NAME'       : pythonPackageName,
                           'PYTHON_MODULE_NAME' : pythonModuleName}

            templateFile.replace(replaceData)
            templateFile.write(pythonFile)

        #

        pythonTestFile = mFileSystem.directoryLib.Directory.join(pythonPackagePath,
                                                                 mMecoPackage.enumLib.PackageFolderName.kPythonUnitTestFolderName,
                                                                 '{}{}.py'.format(pythonModuleName, mMecoPackage.enumLib.PackagePythonFileSuffix.kTest))
        if not os.path.isfile(pythonTestFile):

            templateFile = mFileSystem.templateFileLib.TemplateFile()
            templateFile.setFile(mFileSystem.directoryLib.Directory.join(settingsPackage.path(),
                                                                         mMecoPackage.enumLib.PackageFolderStructure.kResources,
                                                                         'templates',
                                                                         'package',
                                                                         'pythonModuleLibTest.py'))

            replaceData = {'PACKAGE_NAME'       : pythonPackageName,
                           'PYTHON_MODULE_NAME' : pythonModuleName}

            templateFile.replace(replaceData)
            templateFile.write(pythonTestFile)

        #

        return [pythonFile, pythonTestFile]

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # RELEASE
    # ------------------------------------------------------------------------------------------------
    ## @name RELEASE

    ## @{
    #
    ## @brief Get relative release path of the package.
    #
    # This is the release destination path that includes the version.
    #
    #  Return format: `PACKAGE_NAME/VERSION/PACKAGE_NAME` (i.e. `mQtWidgets/1.4.8/mQtWidgets`)
    #
    #  @exception N/A
    #
    #  @return str - Relative path.
    def getPackageReleaseRelativePath(self):

        return mFileSystem.directoryLib.Directory.joinRelative(self._name, self._version, self._name)

    #
    ## @brief Get files to be released.
    #
    #  @param relative [ bool | True | in  ] - Whether the file paths should be relative to root of the package.
    #
    #  @exception N/A
    #
    #  @return list of str - Path of the files.
    #  @return None        - If no package has been set.
    def getReleaseFiles(self, relative=True):

        if not self._path:
            return None

        directory = mFileSystem.directoryLib.Directory(directory=self._path)
        fileList  = directory.listFilesRecursively(relative=relative)

        if not fileList:
            return None

        fileList.sort()

        return fileList

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # CONTENT
    # ------------------------------------------------------------------------------------------------
    ## @name CONTENT

    ## @{
    #
    ## @brief Get Python package names contained by this package.
    #
    #  Python packages are located in `PATH/PACKAGE_NAME/python` folder.
    #
    #  @param ignoreDefault [ bool | False | in ] - Whether to ignore default package, which is the package with the same name as this package.
    #
    #  @exception N/A
    #
    #  @return list of str - Package names, empty if no package has been set.
    def getPythonPackages(self, ignoreDefault=False):

        pythonPackageList = []

        if not self._path:
            return pythonPackageList

        _directory = mFileSystem.directoryLib.Directory(self.getPythonPath())

        folderList = _directory.listFolders()
        if not folderList:
            return pythonPackageList

        for folder in folderList:

            if ignoreDefault and self._name == folder:
                continue

            initFile = os.path.join(_directory.directory(), folder, '__init__.py')
            if not os.path.isfile(initFile):
                continue

            pythonPackageList.append(folder)

        return pythonPackageList

    #
    ## @brief Get absolute path of the requested local document.
    #
    #  The following values can be provided as `folder`.
    #
    #  - mMecoPackage.enumLib.FolderStructure.kDocCPPAPIReference
    #  - mMecoPackage.enumLib.FolderStructure.kDocPythonAPIReference
    #
    #  @param folder [ str | None | in  ] - Document folder.
    #
    #  @exception N/A
    #
    #  @return str  - Absolute path of the help file.
    #  @return None - If help file doesn't exist.
    #  @return None - If no package has been set.
    def getLocalDocument(self, folder):

        if not self._path:
            return None

        path = self.getLocalPath(folder)
        if not path:
            return None

        localHelpFile = mFileSystem.directoryLib.Directory.join(path, 'html', 'index.html')

        if os.path.isfile(localHelpFile):
            return localHelpFile

        return None

    #
    ## @brief Get line of code contained by this package.
    #
    #  @exception N/A
    #
    #  @return dict - Keys are, python and cpp.
    #  @return None - If no package has been set.
    def getLineOfCode(self):

        if not self._path:
            return None

        lineOfCode = {'python':0, 'cpp':0}

        _dir  = mFileSystem.directoryLib.Directory(directory=self._path)
        _file = mFileSystem.fileLib.File()

        fileList = _dir.listFilesRecursively(extension='py')
        if fileList:
            for i in fileList:
                if not _file.setFile(i):
                    continue
                lineOfCode['python'] += _file.lineCount()

        fileList = _dir.listFilesRecursively(extension='h')
        if fileList:
            for i in fileList:
                if not _file.setFile(i):
                    continue
                lineOfCode['cpp'] += _file.lineCount()

        fileList = _dir.listFilesRecursively(extension='cpp')
        if fileList:
            for i in fileList:
                if not _file.setFile(i):
                    continue
                lineOfCode['cpp'] += _file.lineCount()

        return lineOfCode

    #
    ## @brief Get files for the requested local folder of the package.
    #
    #  If mMecoPackage.enumLib.FolderStructure.kPython is provided for `folder` argument, folder will be set as
    #  `PATH/PACKAGE_NAME/python/PYTHON_PACKAGE_NAME`.
    #
    #  If no value provided for `pythonPackageName` argument, name of the package will be used.
    #
    #  @param folder            [ str  | None | in  ] - Enum value from mMecoPackage.enumLib.FolderStructure.
    #  @param pythonPackageName [ str  | None | in  ] - Name of the Python package.
    #  @param absPath           [ bool | True | in  ] - Whether to list files with absolute path.
    #  @param extension         [ str  | None | in  ] - List files only with given extension.
    #  @param suffix            [ str  | None | in  ] - List files only with given suffix.
    #
    #  @exception IOError - If requested local folder doesn't exist.
    #
    #  @return list of str - Files.
    #  @return None        - If no package has been set.
    #  @return None        - If no file is found.
    def getFiles(self, folder, pythonPackageName=None, absPath=True, extension=None, suffix=None):

        if not self._path:
            return None

        localFolder = folder

        if not pythonPackageName:
            pythonPackageName = self._name

        if folder == mMecoPackage.enumLib.PackageFolderStructure.kPython:
            localFolder = mFileSystem.directoryLib.Directory.joinRelative(folder, pythonPackageName)

        localFolder = self.getLocalPath(localFolder)

        _directory  = mFileSystem.directoryLib.Directory()
        if not _directory.setDirectory(localFolder):
            raise IOError('Local folder of the package doesn\'t exist: {} {}'.format(pythonPackageName, localFolder))

        fileList = _directory.listFilesWithAbsolutePath(directory=None,
                                                        ignoreDot=True,
                                                        extension=extension)
        if not fileList:
            return None

        # Extension
        if folder == mMecoPackage.enumLib.PackageFolderStructure.kPython and not extension:
            fileList = [x for x in fileList if os.path.splitext(x)[1] == '.py']

        if suffix:

            _file = mFileSystem.fileLib.File()
            newFileList = []
            for i in fileList:
                if not _file.setFile(path=i):
                    continue

                if _file.baseName().endswith(suffix):
                    newFileList.append(i)

            fileList = newFileList

        if not absPath:
            fileList = [os.path.basename(x) for x in fileList]

        return fileList

    #
    ## @brief Run unit tests of the package.
    #
    #  Return list contains a dict object for each unit test class. The dict instances
    #  contain the following data:
    #
    #  Key      | Data Type | Description                                                            |
    #  :------- |:--------- |:---------------------------------------------------------------------- |
    #  module   | str       | Absolute import path of the Python test module.                        |
    #  class    | str       | Name of the unit test class.                                           |
    #  count    | int       | How many tests have been run.                                          |
    #  errors   | list      | Errors.                                                                |
    #  failures | list      | Failures.                                                              |
    #  output   | str       | Output.                                                                |
    #
    #  If no value provided for `pythonPackageName` argument, Python package with the same name as the package will be used.
    #
    #  @param pythonPackageName [ str | None | in  ] - Name of the Python package, which the tests will be run for.
    #
    #  @exception N/A
    #
    #  @return list of dict - Result.
    #  @return None         - If no package has been set.
    def runUnitTests(self, pythonPackageName=None):

        if not self._path:
            return None

        pythonPackageNameList = []

        if pythonPackageName:
            pythonPackageNameList.append(pythonPackageName)
        else:
            pythonPackageNameList.extend(self.getPythonPackages(ignoreDefault=False))

        resultList = []

        packagePythonPackageList = self.getPythonPackages()

        for pythonPackage in pythonPackageNameList:

            if not pythonPackage in packagePythonPackageList:
                raise mMecoPackage.exceptionLib.PythonPackageDoesNotExist('Package does not have a Python package named: {}'.format(pythonPackage))

            try:
                unitTestModuleList = self.getFiles(mFileSystem.directoryLib.Directory.joinRelative(mMecoPackage.enumLib.PackageFolderStructure.kPython,
                                                                                                   pythonPackage,
                                                                                                   mMecoPackage.enumLib.PackageFolderName.kPythonUnitTestFolderName),
                                                   pythonPackage,
                                                   False,
                                                   'py',
                                                   mMecoPackage.enumLib.PackagePythonFileSuffix.kTest)
            except IOError as error:
                continue

            if not unitTestModuleList:
                continue

            for unitTestFile in unitTestModuleList:

                moduleName = '{}.{}.{}'.format(pythonPackage,
                                               mMecoPackage.enumLib.PackageFolderName.kPythonUnitTestFolderName,
                                               os.path.splitext(unitTestFile)[0])

                unitTestModuleDict = {'module':moduleName}

                _unitTestModule = import_module(moduleName)

                for name, _obj in inspect.getmembers(_unitTestModule):

                    if not inspect.isclass(_obj):
                        continue

                    if not issubclass(_obj, unittest.TestCase):
                        continue

                    _stream = StringIO()
                    _runner = unittest.TextTestRunner(stream=_stream)
                    _result = _runner.run(unittest.makeSuite(_obj))

                    unitTestModuleDict['class']    = _obj.__name__
                    unitTestModuleDict['count']    = _result.testsRun
                    unitTestModuleDict['errors']   = _result.errors
                    unitTestModuleDict['failures'] = _result.failures
                    _stream.seek(0)
                    unitTestModuleDict['output']   = _stream.read()
                    resultList.append(unitTestModuleDict)

        return resultList if resultList else None

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # LOCATION
    # ------------------------------------------------------------------------------------------------
    ## @name LOCATION

    ## @{
    #
    ## @brief Get location of the packages, where this package belongs to.
    #
    #  Since released packages have different path, this method can be used to get the packages path of the package.
    #  This is the path where all the packages will be under for any given environment.
    #
    #  @exception N/A
    #
    #  @return str  - Absolute path of the location of the package.
    #  @return None - If no package has been set.
    def getLocation(self):

        if not self._path:
            return None

        if self._isVersioned:
            return mFileSystem.directoryLib.Directory.navigateUp(directory=self._path, level=3)
        else:
            return mFileSystem.directoryLib.Directory.navigateUp(directory=self._path, level=1)

    #
    ## @brief Get the Python path of the package in `PATH/PACKAGE_NAME/python` format.
    #
    #  @exception N/A
    #
    #  @return str  - Absolute path.
    #  @return None - If no package has been set.
    def getPythonPath(self):

        if not self._path:
            return None

        return mFileSystem.directoryLib.Directory.join(self._path,
                                                       mMecoPackage.enumLib.PackageFolderStructure.kPython)

    #
    ## @brief Get the Python package path for given `pythonPackageName` in `PATH/PACKAGE_NAME/python/PACKAGE_NAME` format.
    #
    #  If `pythonPackageName` argument is not provided, name of the package will be used as Python package name.
    #
    #  @param pythonPackageName [ str | None | in  ] - Name of the Python package.
    #
    #  @exception N/A
    #
    #  @return str  - Absolute path.
    #  @return None - If no package has been set.
    #  @return None - If no Python package with given name contained by this package.
    def getPythonPackagePath(self, pythonPackageName=None):

        if not self._path:
            return None

        if not pythonPackageName:
            pythonPackageName = self._name

        if not pythonPackageName in self.getPythonPackages():
            return None

        return mFileSystem.directoryLib.Directory.join(self._path,
                                                       mMecoPackage.enumLib.PackageFolderStructure.kPython,
                                                       pythonPackageName)

    #
    ## @brief Get absolute path of given `relativePath` of the package.
    #
    #  Method doesn't check whether the returned path exists.
    #
    #  @param relativePath [ str | None | in  ] - Relative path.
    #
    #  @exception N/A
    #
    #  @return str  - Absolute path of the requested folder.
    #  @return None - If no package has been set.
    def getLocalPath(self, relativePath):

        if not self._path:
            return None

        return mFileSystem.directoryLib.Directory.join(self._path, relativePath)

    #
    ## @}

    #
    # ------------------------------------------------------------------------------------------------
    # STATIC METHODS
    # ------------------------------------------------------------------------------------------------
    #
    ## @brief Get the root of this particular package.
    #
    #  @exception N/A
    #
    #  @return str - Absolute path of the root of this package.
    @staticmethod
    def getRootOfThisPackage():

        return os.path.abspath(mFileSystem.directoryLib.Directory.join(os.path.dirname(__file__), '..', '..'))

    #
    # ----------------------------------------------------------------------------------------------------
    # QUERY
    # ----------------------------------------------------------------------------------------------------
    ## @name QUERY

    ## @{
    #
    ## @brief Check whether the given path is root of a package.
    #
    #  Following pattern will be checked: `path/PACKAGE_NAME/python/PACKAGE_NAME/packageInfoLib.py`
    #  against given `path`.
    #
    #  @param path [ str | None | in  ] - Path.
    #
    #  @exception N/A
    #
    #  @return bool - Result.
    @staticmethod
    def isRootOfAPackage(path):

        if Package.isInfoModuleFile(os.path.join(path,
                                                 mMecoPackage.enumLib.PackageFolderName.kPython,
                                                 os.path.basename(path),
                                                 '{}.py'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))):
            return True

        return False

    #
    ## @brief Check whether given path is a package info module file.
    #
    #  Method first checks whether given `path` exists.
    #
    #  @param path [ str | None | in  ] - Path.
    #
    #  @exception N/A
    #
    #  @return str  - Root path of the package, which given `path` (package info module file) belongs to.
    #  @return None - If given `path` is not a package info module file or it doesn't exist.
    @staticmethod
    def isInfoModuleFile(path):

        if not os.path.isfile(path):
            return None

        match = re.search(mMecoPackage.regexLib.PACKAGE_INFO_MODULE, path)
        if not match:
            return None

        return match.groups()[0]

    #
    ## @}

    #
    # ----------------------------------------------------------------------------------------------------
    # DISCOVER
    # ----------------------------------------------------------------------------------------------------
    ## @name DISCOVER

    ## @{
    #
    ## @brief Get package name from given package info module file path.
    #
    #  @param path [ str | None | in  ] - Package info module file path.
    #
    #  @exception N/A
    #
    #  @return str  - Name of the package.
    #  @return None - If `path` doesn't belong to any package or `path` doesn't exist.
    @staticmethod
    def getPackageName(path):

        packageRootPath = Package.isInfoModuleFile(path)
        if not packageRootPath:
            return None

        return os.path.basename(packageRootPath)

    #
    ## @brief Get package info module file path from given path.
    #
    #  @param path [ str | None | in  ] - Path, directory or file.
    #
    #  @exception N/A
    #
    #  @return str  - Absolute path of the package info module file.
    #  @return None - If package info module file couldn't be found.
    @staticmethod
    def getInfoModuleFile(path):

        if os.path.isfile(path):

            packageRootPath = Package.isInfoModuleFile(path)
            if packageRootPath:
                # Package info module file path is given
                # So return the path
                return path

            # Even though a file provided, its not a package info module file
            # so get the path of it to use it
            path = os.path.dirname(path)

        #

        infoModuleFile = os.path.join(path,
                                      mMecoPackage.enumLib.PackageFolderName.kPython,
                                      os.path.basename(path),
                                      '{}.py'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))

        if Package.isInfoModuleFile(infoModuleFile):
            # Given path is root path of a package
            # So we checked package info module file and found it
            return infoModuleFile

        #

        # Traverse the path and try to find the info module
        infoModuleFile = os.path.join(path, '{}.py'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))
        if os.path.isfile(infoModuleFile):
            return infoModuleFile

        while not os.path.isfile(infoModuleFile):

            path = os.path.abspath(os.path.join(path, '..'))
            if re.match(r'(^\/+$)|(^\S\:\/+)$|(^\S\:\\+)$', path):
                break

            if not os.path.isdir(path):
                break

            # Path might be belong to a Python package in the package so check for it
            if os.path.basename(path) == mMecoPackage.enumLib.PackageFolderName.kPython:
                possiblePackageName = os.path.basename((os.path.dirname(path)))
                infoModuleFile = os.path.join(path, possiblePackageName, '{}.py'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))
                if Package.isInfoModuleFile(infoModuleFile):
                    return infoModuleFile

            infoModuleFile = os.path.join(path, '{}.py'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))
            if Package.isInfoModuleFile(infoModuleFile):
                return infoModuleFile

        return None

    #
    ## @brief Get package info module from given path.
    #
    #  @param path [ str | None | in  ] - Path, directory or file.
    #
    #  @exception N/A
    #
    #  @return str    - Absolute path of the package info module file.
    #  @return module - Imported package info module.
    @staticmethod
    def getInfoModule(path):

        packageInfoFile = Package.getInfoModuleFile(path)
        if not packageInfoFile:
            return None

        compiledPackageInfoFile = '{}c'.format(packageInfoFile)
        if os.path.isfile(compiledPackageInfoFile):
            os.remove(compiledPackageInfoFile)

        packageName = Package.getPackageName(packageInfoFile)

        pythonPath = os.path.dirname(os.path.dirname(packageInfoFile))

        pathAdded = False
        if not pythonPath in sys.path:
            sys.path.insert(0, pythonPath)
            pathAdded = True

        module = import_module('{}.{}'.format(packageName, mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))

        if pathAdded:
            sys.path.pop(0)

        return module

    #
    ## @brief Import package and get `Package` class instance that represents it.
    #
    #  @param name [ str | None | in  ] - Import name of the package.
    #
    #  @exception N/A
    #
    #  @return mMecoPackage.packageLib.Package  - Package class instance.
    #  @return None                             - If no package with `name` available .
    @staticmethod
    def getPackageByImport(name):

        try:
            module = import_module(name)
            return Package(path=module.__file__)
        except:
            return None

    #
    ## @brief List all packages.
    #
    #  Method searches packages by using `sys.path`.
    #
    #  @exception N/A
    #
    #  @return list of module - Imported package info Python modules.
    @staticmethod
    def list():

        packageList = []

        for path in sys.path:

            if not path.endswith(mMecoPackage.enumLib.PackageFolderName.kPython):
                continue

            packageName = os.path.basename(os.path.dirname(path))

            if not os.path.isfile(os.path.join(path,
                                               packageName,
                                               '{}.py'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))):
                continue

            packageInfoModule = import_module('{}.{}'.format(packageName, mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))

            if not packageInfoModule in packageList:
                packageList.append(packageInfoModule)

        packageList.sort(key=lambda x: x.NAME)

        return packageList

    #
    ## @}

    ## @name CREATE A PACKAGE

    ## @{
    #
    ## @brief Create a package.
    #
    #  Method doesn't touch existing files.
    #
    #  @param name          [ str | None | in  ] - Name of the package.
    #  @param description   [ str | None | in  ] - Description about the package.
    #  @param path          [ str | None | in  ] - Path, where the package will be created.
    #  @param external      [ bool | None | in  ] - Whether this package should be marked external.
    #
    #  @exception N/A
    #
    #  @return mMecoPackage.packageLib.Package - Package class instance.
    @staticmethod
    def create(name,
               description='',
               path=os.getcwd(),
               external=False):

        if not os.path.isdir(path):
            os.makedirs(path)

        packageRoot = mFileSystem.directoryLib.Directory.join(path, name)

        for folder in mMecoPackage.enumLib.PackageFolderStructure.listAttributes():

            folder = mFileSystem.directoryLib.Directory.join(packageRoot, folder)
            if not os.path.isdir(folder):
                os.makedirs(folder)

        pythonPackagePath = mCore.pythonUtilsLib.createPythonPackage(mFileSystem.directoryLib.Directory.join(packageRoot,
                                                                                                             mMecoPackage.enumLib.PackageFolderStructure.kPython),
                                                                     name)

        mCore.pythonUtilsLib.createPythonPackage(pythonPackagePath, 'tests')

        settingsPackage = Package.getPackageByImport('mMecoSettings.{}'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))

        #

        # Package Info Module
        packageInfoModuleFilePath = mFileSystem.directoryLib.Directory.join(packageRoot,
                                                                            mMecoPackage.enumLib.PackageFolderStructure.kPython,
                                                                            name,
                                                                            '{}.py'.format(mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))
        if not os.path.isfile(packageInfoModuleFilePath):

            templateFile = mFileSystem.templateFileLib.TemplateFile()
            templateFile.setFile(mFileSystem.directoryLib.Directory.join(settingsPackage.path(),
                                                                         mMecoPackage.enumLib.PackageFolderStructure.kResources,
                                                                         'templates',
                                                                         'package',
                                                                         mMecoPackage.enumLib.PackageFile.kInfoModuleFileBaseName))

            replaceData = {'PACKAGE_NAME'           : name,
                           'PACKAGE_VERSION'        : '1.0.0',
                           'PACKAGE_DESCRIPTION'    : description,
                           'IS_PACKAGE_EXTERNAL'    : 'True' if external else 'False',
                           'DEVELOPER_EMAIL_ADDRESS': 'DEVELOPER_EMAIL_ADDRESS'}

            templateFile.replace(replaceData)
            templateFile.write(packageInfoModuleFilePath)

        #

        # Git Ignore File
        gitIgnoreFilePath = mFileSystem.directoryLib.Directory.join(packageRoot,
                                                                    '.{}'.format(mMecoPackage.enumLib.PackageFile.kGitIgnoreFileBaseName))
        if not os.path.isfile(gitIgnoreFilePath):
            gitIgnoreTemplateFile = mFileSystem.directoryLib.Directory.join(settingsPackage.path(),
                                                                            mMecoPackage.enumLib.PackageFolderStructure.kResources,
                                                                            'templates',
                                                                            'package',
                                                                            mMecoPackage.enumLib.PackageFile.kGitIgnoreFileBaseName)
            shutil.copy2(gitIgnoreTemplateFile, gitIgnoreFilePath)

        #

        # Readme File
        readmeFilePath = mFileSystem.directoryLib.Directory.join(packageRoot,
                                                                 mMecoPackage.enumLib.PackageFile.kReadMeMarkdownFileName)
        if not os.path.isfile(readmeFilePath):

            templateFile = mFileSystem.templateFileLib.TemplateFile()
            templateFile.setFile(mFileSystem.directoryLib.Directory.join(settingsPackage.path(),
                                                                         mMecoPackage.enumLib.PackageFolderStructure.kResources,
                                                                         'templates',
                                                                         'package',
                                                                         mMecoPackage.enumLib.PackageFile.kReadMeMarkdownFileName))

            replaceData = {'PACKAGE_NAME'           : name,
                           'PACKAGE_DESCRIPTION'    : description}

            templateFile.replace(replaceData)
            templateFile.write(readmeFilePath)

        #

        # Package Env Module
        packageEnvModuleFilePath = mFileSystem.directoryLib.Directory.join(packageRoot,
                                                                           mMecoPackage.enumLib.PackageFolderStructure.kPython,
                                                                           name,
                                                                           '{}.py'.format(mMecoPackage.enumLib.PackageFile.kEnvModuleFileBaseName))
        if not os.path.isfile(packageEnvModuleFilePath):

            templateFile = mFileSystem.templateFileLib.TemplateFile()
            templateFile.setFile(mFileSystem.directoryLib.Directory.join(settingsPackage.path(),
                                                                         mMecoPackage.enumLib.PackageFolderStructure.kResources,
                                                                         'templates',
                                                                         'package',
                                                                         mMecoPackage.enumLib.PackageFile.kEnvModuleFileBaseName))

            replaceData = {'PACKAGE_NAME' : name}

            templateFile.replace(replaceData)
            templateFile.write(packageEnvModuleFilePath)

        return Package(packageRoot)

    #
    ## @}
